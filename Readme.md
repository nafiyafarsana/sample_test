Vendor Management System

A Vendor Management System to handle vendor profiles, track purchase orders, and calculate vendor performance metrics.
Table of Contents

    Introduction
    Features
    Installation
    Usage
    API Endpoints
    Contributing

Introduction

The Vendor Management System (VMS) is a web application designed to manage vendor information, track purchase orders, and evaluate vendor performance metrics.
Features

    Vendor Profile Management:
        Create, update, retrieve, and delete vendor profiles.

    Purchase Order Tracking:
        Create, update, retrieve, and delete purchase orders.

    Vendor Performance Evaluation:
        Calculate and retrieve performance metrics for vendors.
    Installation

Clone the repository and set up the project locally.

# Clone the repository
git clone https://github.com/yourusername/vendor-management-system.git

# Change into the project directory
cd vendor-management-system

# Install dependencies
pip install -r requirements.txt


## Usage

Run migrations: python manage.py migrate
Create a superuser: python manage.py createsuperuser
Start the development server: python manage.py runserver
Visit http://localhost:8000/admin/ to log in with the superuser credentials and manage the data.

## API Endpoints

#### Get all items

Vendor Profile:

POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve a specific vendor.
PUT /api/vendors/{vendor_id}/: Update a vendor.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.
Purchase Order:

POST /api/purchase_orders/: Create a new purchase order.
GET /api/purchase_orders/: List all purchase orders.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
Vendor Performance Evaluation:

GET /api/vendors/{vendor_id}/performance/: Retrieve a vendor's performance metrics.


## Contributing

If you want to contribute to the Vendor Management System, follow these steps:

Fork the project.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.
