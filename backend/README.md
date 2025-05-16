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
- MySQL 9+
- redis 7+
- Virtualenv (optional but recommended)

### Installation Steps

1. **Clone the repository**
   ```sh
   git clone git@github.com:EmmanuelNiyonshuti/stock_buddy.git
   cd stock-buddy/backend
   ```

2. **Create a virtual environment and activate it**
   1. Option 1: Using pip
   ```sh
   python -m venv venv

   source venv/bin/activate  # On Windows use: venv\Scripts\activate

   pip install -r requirements.txt
   ```

   2. Option 2: Using **uv**
      1. make sure uv is installed on your host
         -  install **uv** by: 
         ```sh
         curl -LsSf https://astral.sh/uv/install.sh | sh # on macOs and Linux
         powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"   on windows
         ```
      -  Then add uv to your PATH if it’s not already.
      2. Create and Activate the virtual environment:
         ```sh
         uv venv .venv
         source .venv/bin/activate  # On Windows: .venv\Scripts\activate
         ```
      3. Sync dependencies (from uv.lock):
         ```sh
         uv sync
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
   alternatively you can use: 
   ```sh
   uv run run.y
   ```

The API will now be running at `http://127.0.0.1:5000/`.

## API Documentation

For a full list of available endpoints, visit the Swagger API Docs at:
`http://127.0.0.1:5000/apidocs`


7. Running the application with Docker.
      1. Ensure Docker is installed on your system
         - [Install Docker](https://docs.docker.com/get-docker/) if you haven't already

      2. Build the Docker image
         
         from the backend directory, run:
            ```sh
               docker build -t stock_buddy_restapi .
            ```
      3. Run the Docker container
         ```sh
         docker run -p 5000:5000 stock_buddy_restapi
         ```
         * The API will now be accessible at: `http://127.0.0.1:5000/`.
