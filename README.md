# product-management


### Run Ansible Playbook

```bash
ansible-playbook my-test.yaml
```

### Run Ansible AdHoc command 

To Test ansible module using addHoc command
```bash
     ANSIBLE_LIBRARY=./library ansible -m products_management -a 'method=GET id=23' localhost
```  
