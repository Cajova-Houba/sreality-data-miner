# About

Scripts to pull data from sreality.cz and store them in DB.

# Secrets

## Init
 - git secret init
 - git secret tell <email>

## Add files
 - git secret add deployment/pwd_env
 - git secret add deployment/ansible_id_rsa
 - git secret hide

## Reveal files
 - gpg --import <key>
 - git secret reveal

# Installing server

 - first time: `ansible-playbook --vault-password-file pwd_env --extra-vars="ansible_user=root" -i ./inventories/chunkhost ansible-init.yml`
 - install server:  `ansible-playbook --vault-password-file pwd_env  -i ./inventories/chunkhost install-server.yml`
 - deploy app: `ansible-playbook --vault-password-file pwd_env  -i ./inventories/chunkhost deploy-app.yml`