#!/usr/bin/env python

import sys
import yaml
import os.path
import shutil
import argparse
import subprocess
import tempfile
import atexit

desc = ('Apply a role to a hosts from ansible inventory')

class AnsibleWrapperError(Exception):
    pass

def callCheck(command, env=None, stdin=None):
    print "about to run \"%s\"" % command
    if subprocess.call(command.split(), env=env, stdin=stdin):
        raise AnsibleWrapperError("%s failed." % command)

def remove_tmp_dir(d):
    print "removing %s" % d
    shutil.rmtree(d)

def main(args_list):
    args, unparsed_args_list = get_args(args_list)

    tmp_dir = tempfile.mkdtemp()
    print "created temporary dir %s" % tmp_dir
    if not args.debug:
        atexit.register(remove_tmp_dir, tmp_dir)
    cwd = os.getcwd()
    os.chdir(tmp_dir)
    os.mkdir(os.path.join(tmp_dir, 'roles'))
    role_dir = os.path.join(cwd, args.role)

    if os.path.isdir(role_dir):
        role_name = os.path.basename(role_dir)
        dest_dir = os.path.join(tmp_dir, 'roles', role_name)
        shutil.copytree(role_dir, dest_dir)
        print "copied role %s" % args.role

    elif args.role.endswith('.git'):
        role_name = args.role.split('/')[-1].split('.')[0]
        os.chdir(os.path.join(tmp_dir, 'roles'))
        callCheck("git clone %s" % args.role)
        print "cloned role %s" % args.role
        os.chdir(tmp_dir)
    else:
        raise AnsibleWrapperError("Given role doesn't exist")

    # cur dir is tmp_dir
    # desired role is in role_name
    # desired hosts are in args.hosts
    role_dict = {'role': role_name}
    if args.params:
        params_dict = yaml.load(args.params)
        if type(params_dict) != dict:
            raise AnsibleWrapperError("params must be a dict")
        role_dict.update(params_dict)

    playbook = [{
      'hosts': ":".join(args.hosts),
      'roles': [role_dict],
    }]

    with open ('i.yml', 'w') as playbook_file:
        playbook_file.write(yaml.dump(playbook))

    callCheck("cat i.yml")

    callCheck("ansible-playbook --syntax-check i.yml")

    if not args.test:
        ansible_cmd = ( "ansible-playbook -v -s i.yml " +
                        " ".join(unparsed_args_list))
        callCheck(ansible_cmd)
    else:
        print 'A test run, _NOT_ running ansible-playbook'


def get_args(args_list):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='ansible-apply-role-to-host',
        description=desc)

    help_role = ("ansible role. Must be a direcoty with the role, or url of "
                "remote git repo.")
    help_test = 'test - dont run ansible-playbook'
    help_hosts = ('host aliases present in ansible inventory, '
                  'separated by space')
    help_params = 'parameters for the role in file'
    help_debug = 'dont remove temporary dir'

    parser.add_argument('hosts', metavar='HOST', help=help_hosts, nargs='+')
    parser.add_argument('-r', '--role', help=help_role, required=True)
    parser.add_argument('-p', '--params', help=help_params,
                        type=argparse.FileType('r'))
    parser.add_argument('-t', '--test', help=help_test, action='store_true')
    parser.add_argument('-d', '--debug', help=help_debug, action='store_true')

    # returns tupe (args with populated namespace, remaining unparsed opts)
    return parser.parse_known_args(args_list)


if __name__ == '__main__':
    main(sys.argv[1:])

