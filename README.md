# Remarcable Django Take-Home Assignment

A Django application that models products, categories, and tags, with search and filtering functionality.

## Features

- Product, Category, and Tag models
- Category-to-product relationship
- Product-to-tag many-to-many relationship
- Django admin data management
- Search by product name and description
- Filter by category
- Filter by multiple tags
- Combined search and filtering
- Basic Django template UI
- Query optimization using `select_related` and `prefetch_related`
- Tests

## Tech Stack

- Python
- Django
- SQLite
- Django Templates

## Setup

1. Clone the repository:

```bash
git clone <repo-url>
cd django-take-home-assignment
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Optionally seed sample data for review:

```bash
python manage.py seed_sample_data
```

8. Run the development server:

```bash
python manage.py runserver
```

9. Open the application homepage:

- `http://127.0.0.1:8000/`

10. Open Django admin:

- `http://127.0.0.1:8000/admin/`

## Data Population

This assignment is designed with Django admin as the primary interface for managing catalog data. Reviewers can create and edit categories, tags, and products directly in the admin panel.

For convenience, the project also includes a `seed_sample_data` management command to quickly populate realistic review data. This command exists to make evaluation easier and is not required for the core assignment workflow.

## Minimum Sample Data

The assignment expects at least:

- 5 categories
- 10 tags
- 20 products

The included `seed_sample_data` command exceeds that minimum and currently creates 6 categories, 13 tags, and 22 products.

## Search and Filter Examples

The catalog homepage supports the following query parameters:

- Search by keyword: `/?q=gloves`
- Search by description text: `/?q=warehouse`
- Filter by category: `/?category=safety-equipment`
- Filter by one tag: `/?tags=ppe`
- Filter by multiple tags: `/?tags=ppe&tags=jobsite-ready`
- Combine search and category: `/?q=light&category=electrical-supplies`
- Combine search, category, and tags: `/?q=warehouse&category=safety-equipment&tags=ppe&tags=warehouse-stock`

## Running Tests

```bash
python manage.py test
```

## AI-Assistence

All AI-generated output was reviewed, modified, and expanded before being incorporated into the project.

AI was used in the following limited ways:

- To generate ideas for possible edge cases to cover in the test suite
- To help draft the `seed_sample_data` management command

All AI-assisted output was reviewed and adapted to fit the project requirements. This repository was not submitted as raw AI-generated work.

## Assumptions

- SQLite is used for local development.
- Products include `price` and `is_active` fields for realistic catalog behavior.
- The seed command is included only to make review easier.
