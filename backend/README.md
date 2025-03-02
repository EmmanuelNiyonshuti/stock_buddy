# stock_buddy

## Overview
This is the backend of stock_buddy, a RESTful API for managing inventory, tracking stock levels, and recording transactions. Built with Flask, it provides secure and efficient handling of product and inventory data.

## Features
- **User Authentication** – Secure login and registration with JWT authentication.
- **Product Management** – CRUD operations for products.
- **Inventory Tracking** – Updates stock levels based on transactions.
- **Transaction Logging** – Records all product purchases and sales.
- **Low-Stock Alerts** – Notifies users when stock reaches a critical level.

## Tech Stack
- **Framework**: Flask
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT for secure user access

## Setup Guide

### Prerequisites
Make sure you have the following installed:
- Python 3.8+
- MySQL
- Virtualenv (optional but recommended)

### Installation Steps

1. **Clone the repository**
   ```sh
   git clone git@github.com:EmmanuelNiyonshuti/stock_buddy.git
   cd stock-buddy/backend
   ```

2. **Create a virtual environment and activate it**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `backend/` directory and add the required configurations:
   ```sh
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URL=mysql+pymysql://user:password@localhost/stock_buddy
   ```

5. **Run database migrations**
   ```sh
   flask db upgrade
   ```

6. **Start the server**
   ```sh
   python3 run.py
   ```

The API should now be running on `http://127.0.0.1:5000/`.

## API Endpoints

### Authentication
- `POST /api/v1/users` – Register a new user
- `POST /api/v1/users/auth` – Authenticate user and return JWT

### Products
- `GET /api/v1/products` – Retrieve all products (with pagination support)
- `POST /api/v1/products` – Create a new product
- `GET /api/v1/products/<id>` – Retrieve a specific product
- `PUT /api/v1/products/<id>` – Update product details
- `DELETE /api/v1/products/<id>` – Remove a product

### Transactions
- `GET /api/v1/transactions` – Retrieve all transactions
- `POST /api/v1/transactions` – Log a new transaction
- `GET /api/v1/transactions/<id>` – Retrieve a specific transaction

### Inventory

- `GET /products/<product_id>/inventory` – Get inventory status for a product.

