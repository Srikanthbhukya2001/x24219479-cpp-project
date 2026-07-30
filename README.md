# Cloud-Based Inventory and Sales Management System

## Overview

The Cloud-Based Inventory and Sales Management System is a Django web application designed to help businesses manage products, inventory, sales transactions, reporting, and analytics through a cloud-native architecture.

The application integrates multiple AWS cloud services to provide scalable storage, notifications, serverless analytics, and automated reporting capabilities.

---

## Features

### Product Management

* Add new products
* Update product details
* Delete products
* Upload product images

### Inventory Management

* Track stock levels
* Manage product sizes
* Update inventory quantities
* Monitor available stock

### Sales Management

* Record sales transactions
* Calculate sales totals
* Maintain sales history
* Generate sales reports

### Analytics Dashboard

* View sales statistics
* Analyze product performance
* Monitor inventory trends
* Generate business insights

---

## Cloud Services Used

| AWS Service           | Purpose                  |
| --------------------- | ------------------------ |
| Amazon S3             | Store product images     |
| Amazon SNS            | Send sales notifications |
| AWS Lambda            | Process sales analytics  |
| Amazon API Gateway    | Invoke Lambda functions  |
| Amazon RDS PostgreSQL | Store application data   |
| AWS Elastic Beanstalk | Host the application     |
| AWS Cloud9            | Development environment  |

---

## Custom Python Library

### pdf-export-lib

A custom PyPI package developed for generating PDF reports.

Features:

* Generate sales reports in PDF format
* Export filtered sales data
* Create summary reports
* Custom PDF formatting and layout

---

## Technology Stack

* Python
* Django
* PostgreSQL
* AWS Cloud Services
* HTML
* CSS
* Bootstrap
* GitHub Actions
* Plotly

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd inventory-sales-management
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Application

```bash
python manage.py runserver
```

---

## Project Structure

```text
inventory-sales-management/
│
├── app/
├── templates/
├── static/
├── media/
├── pdf_export_lib/
├── requirements.txt
├── manage.py
└── README.md
```





