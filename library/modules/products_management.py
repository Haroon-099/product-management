#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
import json
import http.client as http
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.my_http_utils import get_products, get_product_by_id, create_product, update_product, delete_product_by_id


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

BASE_URL = 'dummyjson.com'

REQUIRED_KEYS = ['title', 'price',
                 'discountPercentage', 'stock', 'brand', 'category']
ALL_Keys = ['title', 'price', 'discountPercentage', 'stock',
            'brand', 'category', 'thumbnail', 'description', 'images']
ROUTS = ['add']

path = '/products'
HEADERS = {'Content-type': 'application/json', 'Accept': '*/*'}


def get_module_spec():
    api_spec = dict(
        route=dict(type='str', choices=['add'], required=False),
        method=dict(type='str', choices=[
                    'GET', 'POST', 'PUT', 'DELETE'], required=True),
        id=dict(type='int', required=False),
        json_data=dict(type='str', required=False)
    )
    return api_spec


def run_module():

    # seed the result dict in the object
    result = dict(
        changed=False,
        status='',
        reason='',
        data=''
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
    route = module.params['route']
    product_id = module.params['id']
    input_json = module.params['json_data']
    try:
        if method == 'GET' and product_id is None:
            get_products(result)

        elif method == 'GET' and product_id is not None:
            get_product_by_id(product_id, result)

        elif method == 'POST':
            create_product(route, input_json, result)

        elif method == 'PUT':
            update_product(product_id, input_json, result)

        elif method == 'DELETE':
            delete_product_by_id(product_id, result)
    except Exception as e:
        module.fail_json(msg=str(e))

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
