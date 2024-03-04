# product-management

To run the ansible-playbook to test my module 
  ```bash
     ansible-playbook my-test.yaml
    ```

To Test ansible module using addHoc command
  ```bash
     ANSIBLE_LIBRARY=./library ansible -m products_management -a 'method=GET id=23' localhost
    ```  
