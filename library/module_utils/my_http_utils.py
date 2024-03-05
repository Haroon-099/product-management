#!/usr/bin/python

import json
import http.client as http
from ansible.module_utils.ValidationException import ValidationException

BASE_URL = 'dummyjson.com'


REQUIRED_KEYS = ['title', 'price',
                 'discountPercentage', 'stock', 'brand', 'category']
ALL_Keys = ['title', 'price', 'discountPercentage', 'stock',
            'brand', 'category', 'thumbnail', 'description', 'images']
ROUTS = ['add']

path = '/products'
HEADERS = {'Content-type': 'application/json', 'Accept': '*/*'}


def send_http_request(method, path, body, result):
    conn = http.HTTPSConnection(BASE_URL)
    conn.request(method, path, body, HEADERS)
    response = conn.getresponse()
    if response.status >= 200 and response.status <= 299:
        result['changed'] = True
        result['status'] = response.status
        result['reason'] = response.reason
        result['data'] = json.loads(response.read().decode())
        conn.close()
    else:
        conn.close()
        raise Exception(
            f'The request fail with reson: {response.reason} and status : {response.status}')


def validat_request_body(body):
    try:
        json_data = json.loads(body)
    except json.JSONDecodeError as e:
        raise ValidationException(f'fail to parse "json_data" : {str(e)}')

    missing_keys = [key for key in REQUIRED_KEYS if key not in json_data]

    if missing_keys:
        raise ValidationException(
            f"Missing Required Keys in 'json_data' : {', '.join(missing_keys)}")

    extra_keys = [key for key in json_data if key not in ALL_Keys]

    if extra_keys:
        raise ValidationException(
            f"Unexpected Keys in 'json_data' : {', '.join(extra_keys)} The keys should be in: {ALL_Keys}")


def get_products(result):
    try:
        send_http_request('GET', path, None, result)
    except Exception as e:
        raise e


def get_product_by_id(id, result):
    try:
        send_http_request('GET', f'{path}/{id}', None, result)
    except Exception as e:
        raise e


def create_product(route, json_body, result):
    try:
        validat_request_body(json_body)
        send_http_request('POST', f'{path}/{route}', json_body, result)
    except Exception as e:
        raise e


def update_product(product_id, json_body, result):
    try:
        validat_request_body(json_body)
        send_http_request('PUT', f'{path}/{product_id}', json_body, result)
    except Exception as e:
        raise e


def delete_product_by_id(product_id, result):
    try:
        send_http_request('DELETE', f'{path}/{product_id}', None, result)
    except Exception as e:
        raise e


if __name__ == '__main__':
    pass
