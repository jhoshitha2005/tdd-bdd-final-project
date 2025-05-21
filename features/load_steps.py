# features/steps/load_steps.py

from behave import given
import requests
from http import HTTPStatus

@given('the following products exist')
def step_impl(context):
    """Send product data from feature file to REST API via POST requests"""
    rest_endpoint = "http://localhost:5000/api/products"  # Change as per your API

    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTPStatus.CREATED
