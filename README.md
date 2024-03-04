# product-management

## Product Management Ansible Module 
[Products API Docs ](https://dummyjson.com/docs/products).

This product management module empowers you to:

        * Access products information: Easily retrieve data for all your products or obtain specific details for a single individual.
        * Streamline onboarding: Effortlessly create new product records within the database, simplifying the onboarding process.
        * Maintain data accuracy: Update existing product records promptly to ensure all information remains current and accurate.
        * Manage workforce changes: Efficiently delete product records when necessary, maintaining an up-to-date and organized system.
### Run Ansible Playbook

```bash
ansible-playbook my-test.yaml
```

### Run Ansible AdHoc command 

To Test ansible module using addHoc command
```bash
     ANSIBLE_LIBRARY=./library ansible -m products_management -a 'method=GET id=23' localhost
```  
