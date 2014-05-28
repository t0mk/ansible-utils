<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [ansible-utils](#ansible-utils)
  - [install](#install)
  - [ansible-get-roles](#ansible-get-roles)
  - [ansible-print-all-user-variables-in-role](#ansible-print-all-user-variables-in-role)
  - [ansible-apply-role-to-host](#ansible-apply-role-to-host)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# ansible-utils

Ansible wrappers

## install

```
$ cd ~/bin
$ git clone https://github.com/t0mk/ansible-utils
$ echo 'PATH=${PATH}:~/bin/ansible-utils' >> ~/.zshrc

# if you still use Bash I encourage you to check zsh and oh-my-zsh but anyway:
# echo 'PATH=${PATH}:~/bin/ansible-utils' >> ~/.bashrc
```

## ansible-get-roles

This is sth like librarian for ansible. It downloads all the roles from their
git repos. It takes the first playbook from a file and processes all the dicts
in the 'roles' item.

Use as

```
$ cd playbook_dir
$ ansible-get-roles -p playbook.yml
```

## ansible-print-all-user-variables-in-role

This prints all the variables used in a role. It prints it as a markdown
bulletpoints. It's useful when you are writing a role and want to start a
README.md. You can do sth like:

```
$ cd roles/redmine
$ ansible-print-all-used-variables-in-role
* `redmine_branch` -
* `redmine_db` -
[...]

$ ansible-print-all-used-variables-in-role >> README.md
```

It's not perfect yet.

## ansible-apply-role-to-host

This is for the case when you stumble upon an ansible role on github and you
would like to check how it works for you, or for your VM image, or OS version.

Let's stay you found a role, and you have a testing instance "testhost"
running somewhere (Openstack, Amazon, ...). The "testhost" is listed in your
inventory and ansible can run on it. In other words `ansible -m ping testhost`
succeeds.

(irrelevant note: If you use some IaaS, I advise to check the dynamic
inventory scripts shipped with ansible - ansible/plugins/inventory)

To try a role, normally you would have to create directory structure, clone
the role and write a playbook.
With the script, you can instead just do:

```
$ ansible-apply-role-to-host -r https://github.com/t0mk/dummy_ansible_role.git testhost
```

If the role has parameters, you can put them to a file as a yaml dict and pass
the filename to the script in the -p/--params argument:

```
$ echo "dummy_ansible_role_parameter: defined_in_params" > params.yml
$ ansible-apply-role-to-host -r https://github.com/t0mk/dummy_ansible_role.git -p params.yml testhost
```

You can also pass more than one host in positional arguments.

