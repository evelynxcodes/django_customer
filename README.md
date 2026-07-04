# Django Customers

A small Django project for managing customers, with two zip-download features.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Features

- Customer CRUD (list, add, edit, delete) at `/`
- **Download customers.zip** — exports all customers as a CSV bundled in a zip file (`/export/customers.zip`)
- **Download project.zip** — downloads the entire project source code as a zip file (`/export/project.zip`)

## Admin

Create a superuser to use the Django admin at `/admin/`:

```bash
python manage.py createsuperuser
```
