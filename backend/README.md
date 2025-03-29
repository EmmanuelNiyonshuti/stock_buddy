# stock_buddy - Small Business Stock Tracker

## Overview
This is the backend of **stock_buddy**, a simple yet scalable RESTful API designed for small businesses to efficiently manage their inventory, track stock levels, and record transactions. Built with **Flask**, this API provides secure handling of product data, stock tracking, and transaction management, offering a smart alternative to traditional pen/paper or Excel-based inventory systems.

## Features
- **User Authentication** – login and registration with Cookie-based JWT authentication.
- **Product Management** – CRUD operations for products.
- **Inventory Tracking** – Updates stock levels based on transactions.
- **Transaction Logging** – Records all product purchases and sales.
- **Low-Stock Alerts** – Notifies users when stock reaches a critical level.
- **Swagger API Documentation** - Interactive API docs available at /apidocs.

## Tech Stack
- **Framework**: Flask
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT for secure user access
- **API Documentation**: Swagger (via Flasgger)

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

The API will now be running at `http://127.0.0.1:5000/`.

## API Documentation

For a full list of available endpoints, visit the Swagger API Docs at:
`http://127.0.0.1:5000/apidocs`

