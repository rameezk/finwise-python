# Transaction Categories

Organize transactions with categories and subcategories.

## Create a Category

```python
from finwise import FinWise

client = FinWise(api_key="your-api-key")

category = client.transaction_categories.create(
    name="Groceries",
    color="#4CAF50",
    icon="shopping_cart",
)
```

## Create a Subcategory

```python
subcategory = client.transaction_categories.create(
    name="Organic Food",
    color="#8BC34A",
    parent_id=category.id,
)
```

## List Categories

```python
categories = client.transaction_categories.list()

for cat in categories.data:
    prefix = "  " if cat.is_subcategory else ""
    print(f"{prefix}{cat.name}")
```

To list only subcategories of a specific parent:

```python
subcategories = client.transaction_categories.list(
    parent_id="cat_groceries"
)
```

## Delete a Category

```python
client.transaction_categories.delete("cat_123")
```

!!! warning
    Deleting a category will remove it permanently. Transactions using this category will have their category reference cleared.
