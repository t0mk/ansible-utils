# ansible-utils

Ansible wrappers

## install

```
cd ~/bin
git clone https://github.com/t0mk/ansible-utils
echo 'PATH=${PATH}:~/bin/ansible-utils' >> ~/.zshrc

# if you still use Bash I encourage you to check zsh and oh-my-zsh but anyway:
# echo 'PATH=${PATH}:~/bin/ansible-utils' >> ~/.bashrc
```

## ansible-apply-role-to-host.py

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
ansible-apply-role-to-host -r https://github.com/t0mk/dummy_ansible_role.git testhost
```

If the role has parameters, you can put them to a file as a yaml dict and pass
the filename to the script in the -p/--params argument:

```
echo "dummy_ansible_role_parameter: defined_in_params" > params
ansible-apply-role-to-host -r https://github.com/t0mk/dummy_ansible_role.git -p params testhost
```

