#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
import http.client as http
from ansible.module_utils.basic import AnsibleModule
from ..module_utils.my_http_utils import create_product, update_product, delete_product_by_id


__metaclass__ = type

DOCUMENTATION = r'''
---
module: products_management

short_description: This is an employee management module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: 
    This product management module empowers you to:

        * Access products information: Easily retrieve data for all your products or obtain specific details for a single individual.
        * Streamline onboarding: Effortlessly create new product records within the database, simplifying the onboarding process.
        * Maintain data accuracy: Update existing product records promptly to ensure all information remains current and accurate.
        * Manage workforce changes: Efficiently delete product records when necessary, maintaining an up-to-date and organized system.
options:
    route:
        description: This is the route to send to the test module.
        required: true
        type: str

    Method:
        description: This is the HTTP Method  to send to the test module.
        required: true
        type: str
    
    id:
        description: product id to get a single employee data.
        required: false
        type: int

    json_data:
        description: product as a josn , for POST and PUT operations .
        required: false
        type: str

author:
    - Haroon Dweikat (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Test GET all products
  products_management:
    method: 'GET'
    route: 'products'

- name: Test GET single product
  products_management:
    method: 'GET'
    route: 'products'
    id: 23

- name: Create product record
      products_management:
        method: 'POST'
        route: 'add'
        json_data: '{"title": "BMW Pencil", "price": 14, "discountPercentage": 8.04, "stock": 26, "brand": "School Items", "category": "groceries"}'


- name: Update product record
      products_management:
        method: 'PUT'
        route: 'products'
        id: 1
        json_data: '{"title": "BMW Pencil", "price": 14, "discountPercentage": 8.04, "stock": 26, "brand": "School Items", "category": "groceries"}'


- name: Delete employee record
      products_management:
        method: 'DELETE'
        route: 'products'
        id: 1
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
data:
    description: The product data from API.
    type: json
    returned: always
    sample: "data": {
            "brand": "Apple",
            "category": "smartphones",
            "deletedOn": "2024-03-04T12:38:55.783Z",
            "description": "An apple mobile which is nothing like apple",
            "discountPercentage": 12.96,
            "id": 1,
            "images": [
                "https://cdn.dummyjson.com/product-images/1/1.jpg",
                "https://cdn.dummyjson.com/product-images/1/2.jpg",
                "https://cdn.dummyjson.com/product-images/1/3.jpg",
                "https://cdn.dummyjson.com/product-images/1/4.jpg",
                "https://cdn.dummyjson.com/product-images/1/thumbnail.jpg"
            ],
            "isDeleted": true,
            "price": 549,
            "rating": 4.69,
            "stock": 94,
            "thumbnail": "https://cdn.dummyjson.com/product-images/1/thumbnail.jpg",
            "title": "iPhone 9"
        },
reason:
    description: The response reson message that reterned from the API .
    type: str
    returned: always
    sample: 'OK'

status:
    description: The response status message that reterned from the API .
    type: int
    returned: always
    sample: 200
'''


def get_module_spec():
    module_args = dict(
        route=dict(type='str', choices=['add'], required=False),
        method=dict(type='str', choices=[
                    'GET', 'POST', 'PUT', 'DELETE'], required=True),
        id=dict(type='int', required=False),
        json_data=dict(type='str', required=False)
    )
    return module_args


def build_spec(params):
    spec = {
        'method': None,
        'route': None,
        'id': None,
        'json_data': None
    }

    for key in spec.copy().keys():
        if params.get(key):
            spec[key] = params[key]
        else:
            spec.pop(key)

    return spec


def post_product(module, result):
    spec = build_spec(module.params)
    return create_product(spec)



def run_module():

    # seed the result dict in the object
    result = dict(
        changed=False,
        response='',
        error=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ('method', 'POST', ('json_data', 'route')),
            ('method', 'PUT', ('id', 'json_data', )),
            ('method', 'DELETE', ('id',)),
        ],
    )

    method = module.params['method']
    product_id = module.params['id']
    response = None
    params = build_spec(module.params)
    try:
        # implement integration test 
        if method == 'POST':
            response =  post_product(module, result)
            if 'error' in response: 
                module.fail_json(msg="Failed Getting All products: ",**response)


        elif method == 'PUT':
            response = update_product(params)
            if 'error' in response: 
                module.fail_json(msg="Failed Getting All products: ",**response)


        elif method == 'DELETE':
            response = delete_product_by_id(params)
            if 'error' in response: 
                module.fail_json(msg="Failed Getting All products: ",**response)

    except Exception as e:
        module.fail_json(msg=f"Failed In Product Management Module : {e}")
        
    result['response'] = response
    result["changed"] = True
        
    

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
