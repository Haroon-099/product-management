#!/usr/bin/python

import json
import http.client as http
# from ansible.module_utils.ValidationException import ValidationException

BASE_URL = 'dummyjson.com'


REQUIRED_KEYS = ['title', 'price',
                 'discountPercentage', 'stock', 'brand', 'category']
ALL_Keys = ['title', 'price', 'discountPercentage', 'stock',
            'brand', 'category', 'thumbnail', 'description', 'images']
ROUTS = ['add']

path = '/products'
HEADERS = {'Content-type': 'application/json', 'Accept': '*/*'}


def send_http_request(method, path, body):
    conn = http.HTTPSConnection(BASE_URL)
    conn.request(method, path, body, HEADERS)
    resp = dict()
    response = conn.getresponse()
    if response.status >= 200 and response.status <= 299:
        resp['status'] = response.status
        resp['reason'] = response.reason
        resp['data'] = json.loads(response.read().decode())
        conn.close()
    else:
        conn.close()
        resp['status'] = response.status
        resp['reason'] = response.reason
        resp['error'] = f'The request fail with reson: {response.reason} and status : {response.status}'
    return resp


def validat_request_body(body):
    json_data = None
    resp = ''
    try:
        json_data = json.loads(body)
    except json.JSONDecodeError as e:
        resp = f'fail to parse "json_data" : {str(e)}'
    except Exception as e:
        resp= f'fail to validate "json_data" : {str(e)}'

    missing_keys = [key for key in REQUIRED_KEYS if key not in json_data]

    if missing_keys:
        resp =f"Missing Required Keys in 'json_data' : {', '.join(missing_keys)}"

    extra_keys = [key for key in json_data if key not in ALL_Keys]

    if extra_keys:
        resp =f"Unexpected Keys in 'json_data' : {', '.join(extra_keys)} The keys should be in: {ALL_Keys}"
        
    if resp == '':
        return None   
    return resp


def get_products(spec):
    resp =send_http_request(spec['method'], path, None)
    return resp


def get_product_by_id(spec):
    resp = send_http_request(spec['method'], f'{path}/{spec["id"]}', None)
    return resp



def create_product(spec):
    resp= dict()
    validation_msg = validat_request_body(spec['json_data'])
    if validation_msg:
        resp['error'] = validation_msg
        return resp
    resp = send_http_request(spec['method'], f'{path}/{spec["route"]}', spec["json_data"])
    return resp



def update_product(spec):
    resp= dict()
    validation_msg = validat_request_body(spec['json_data'])
    if validation_msg:
        resp['error'] = validation_msg
        return resp
    resp = send_http_request(spec['method'], f'{path}/{spec["id"]}', spec["json_data"])
    return resp


def delete_product_by_id(spec):
    resp = send_http_request(spec['method'], f'{path}/{spec["id"]}', None)
    return resp


if __name__ == '__main__':
    pass
