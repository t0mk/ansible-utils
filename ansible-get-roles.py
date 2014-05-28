#!/usr/bin/env python

import sys
import yaml
import os.path
import argparse
import subprocess

epilog = """
This is sth like librarian for ansible playbook. It clones roles based on
arbitrary _git_url and _git_branch parameters in roles.

Having following snippet in playbook.yml:

```
  roles:
    - role: timezone
      _git_url: https://git.forgeservicelab.fi/ansible-roles/timezone.git
    - role: mtpereira.passenger
      _git_url: https://github.com/mtpereira/ansible-passenger.git
```
then calling

$ ansible-get-roles -p playbook.yml

will download the listed roles to ./roles/.

"""

desc = "Download ansible roles listed in a playbook to ./roles/"

URL_PARAM = '_git_url'
BRANCH_PARAM = '_git_branch'

class AnsibleWrapperError(Exception):
    pass

def callCheck(command, env=None, stdin=None):
    print "about to run \"%s\" in %s" % (command, os.getcwd())
    if subprocess.call(command.split(), env=env, stdin=stdin):
        raise AnsibleWrapperError("%s failed." % command)

def fetch_role(name, git_url, git_branch=None):
    old_cwd = os.getcwd()
    os.chdir('roles')
    if os.path.isdir(name):
        os.chdir(name)
        # to check that the dir is a git repo
        callCheck("git status -s")
        callCheck("git pull")
        os.chdir(old_cwd)
        return
    clone_cmd = "git clone %s" % git_url
    if git_branch:
        clone_cmd += " -b %s" % git_branch
    clone_cmd += " " + name
    callCheck(clone_cmd)
    os.chdir(old_cwd)

def main(args_list):
    args, unparsed_args_list = get_args(args_list)

    playbook = yaml.load(args.playbook)

    cwd = os.getcwd()
    if not os.path.isdir('./roles'):
        print 'Creating the "roles/" directory'
        os.mkdir('roles')

    for r in playbook[0]['roles']:
        if URL_PARAM not in r:
            print ("Role %s does not have the _git_url parameter. "
                   "It's impossible to fetch it." % r['role'])
            continue
        print " * Fetching role %s from %s" % (r['role'], r[URL_PARAM])
        if args.test:
            print "   This is a test run, not fetching the role."
            continue
        fetch_role(r['role'], r[URL_PARAM], r.get(BRANCH_PARAM))

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass

def get_args(args_list):
    parser = argparse.ArgumentParser(
        formatter_class=CustomFormatter,
        prog='ansible-get-roles',
        epilog=epilog,
        description=desc)

    help_test = 'test - dont clone the roles'
    help_playbook = 'playbook for which you want to fetch the roles'

    parser.add_argument('-p', '--playbook', help=help_playbook,
                        type=argparse.FileType('r'), required=True)
    parser.add_argument('-t', '--test', help=help_test, action='store_true')

    # returns tupe (args with populated namespace, remaining unparsed opts)
    return parser.parse_known_args(args_list)


if __name__ == '__main__':
    main(sys.argv[1:])

