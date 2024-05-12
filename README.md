# Project: Vendor Management System with Performance Metrics

# Author: KMS Veronica

## Admin Credentials 
```bash
Username: vendor
Password: vendor
```
## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <project_folder>
```

## 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run Migrations

```bash
python manage.py migrate
```
## 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```
## 6. Start the Development Server

```bash
python manage.py runserver
```

# API Endpoints

# 1. Vendors
## GET /api/vendors/<br />
Description: Retrieve a list of all vendors.<br />
Authentication Required: Yes<br />
Example Response:<br />

```bash
[
  {
    "id": 1,
    "name": "Vendor 1",
    ...
  },
  ...
]
```

## POST /api/vendors/
Description: Create a new vendor.<br />
Authentication Required: Yes<br />
Example Request Body:<br />


```bash
{
  "name": "New Vendor",
  ...
}
```

# 2. Vendor Details

## GET /api/vendors/<vendor_id>/
Description: Retrieve details of a specific vendor.<br />
Authentication Required: Yes<br />
Example Response:<br /> 

```bash
{
  "id": 1,
  "name": "Vendor 1",
  ...
}
```

## PUT /api/vendors/<vendor_id>/
Description: Update details of a specific vendor.<br />
Authentication Required: Yes<br />
Example Request Body:<br />


```bash
{
  "name": "Updated Vendor Name",
  ...
}
```

## DELETE /api/vendors/<vendor_id>/
Description: Delete a specific vendor.<br />
Authentication Required: Yes

# 3. Purchase Orders

## GET /api/purchase_orders/
Description: Retrieve a list of all purchase orders.<br />
Authentication Required: Yes<br />

## POST /api/purchase_orders/
Description: Create a new purchase order.<br />
Authentication Required: Yes<br />
Example Request Body:<br />


```bash
{
  "vendor": 1,
  ...
}
```

# 5. Vendor Performance

## GET /api/vendors/performance/
Description: Retrieve performance metrics for all vendors.<br />
Authentication Required: Yes<br />

# 6. Acknowledge Purchase Order

## POST /api/purchase_orders/<po_id>/acknowledge/
Description: Acknowledge a specific purchase order.<br />
Authentication Required: Yes<br />

