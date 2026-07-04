import csv
import io
import zipfile
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerForm
from .models import Customer

# Directories/files that should never end up in the project source zip.
EXCLUDED_DIR_NAMES = {'.git', '__pycache__', 'venv', '.venv', 'env', 'node_modules'}
EXCLUDED_FILE_NAMES = {'db.sqlite3'}


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add customer'})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated.')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Edit customer'})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted.')
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


def export_customers_zip(request):
    """Export all customers as a CSV, bundled into a downloadable zip file."""
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(['Name', 'Email', 'Phone', 'Address', 'Created at'])
    for customer in Customer.objects.all():
        writer.writerow([
            customer.name,
            customer.email,
            customer.phone,
            customer.address,
            customer.created_at,
        ])

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('customers.csv', csv_buffer.getvalue())

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="customers_export.zip"'
    return response


def download_project_zip(request):
    """Zip up the whole project source tree and return it for download."""
    base_dir = Path(settings.BASE_DIR)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for path in base_dir.rglob('*'):
            if path.is_dir():
                continue
            if any(part in EXCLUDED_DIR_NAMES for part in path.relative_to(base_dir).parts):
                continue
            if path.name in EXCLUDED_FILE_NAMES:
                continue
            zip_file.write(path, arcname=path.relative_to(base_dir))

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="django_customers_project.zip"'
    return response
