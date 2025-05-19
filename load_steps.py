# features/steps/load_steps.py
from behave import given
from service.models import Product, db

@given('the following products exist')
def step_impl(context):
    """Load background product data from the feature file into the database"""
    for row in context.table:
        product = Product(
            name=row['name'],
            description=row['description'],
            price=float(row['price']),
            available=(row['available'].lower() == 'true'),
            category=row['category']
        )
        db.session.add(product)
    db.session.commit()
