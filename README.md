# Online Shop(React + Django REST Framework)

## Overview

This project is a full-stack e-commerce platform built using **Django REST Framework (DRF)** for the backend and **React** for the frontend. The platform allows users to browse products, add them to a cart, and place orders, with authentication and JWT-based user login.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
  - [Backend (Django + DRF)](#backend-django--drf)
  - [Frontend (React)](#frontend-react)
- [Database Setup](#database-setup)
  - [PostgreSQL Setup](#postgresql-setup)
  - [Database Configuration in Django](#database-configuration-in-django)
- [Environment Variables](#environment-variables)
- [Available Scripts](#available-scripts)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features

- **User Authentication**: Login, Registration with JWT authentication.
- **Product Management**: Browse products, product detail view.
- **Shopping Cart**: Add and remove items from the cart.
- **Checkout & Orders**: Place orders with shipping information.
- **User Profile**: View and update user profile details.
- **Admin Dashboard**: Manage products, orders, and users (Django Admin).

## Tech Stack

### Backend (Django + DRF)

- **Django**: Backend framework
- **Django REST Framework (DRF)**: API development
- **PostgreSQL**: Database
- **JWT Authentication**: User login and registration

### Frontend (React)

- **React**: Frontend library
- **Tailwind CSS**: CSS framework for styling
- **Axios**: For HTTP requests to the API
- **React Router**: For frontend routing

## Setup Instructions

### Backend (Django + DRF)

1. Clone the repository:

   ```bash
   git clone https://github.com/Abulfadl-Ahmadi/Online-Shop.git
   cd Online-Shop
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate 
   # On Windows:
   venv\Scripts\activate
   ```

3. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. [Set up the PostgreSQL database](#database-setup).

5. Apply migrations and start the Django development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend (React)

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install frontend dependencies:

   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

## Database Setup

### PostgreSQL Setup

1. **Install PostgreSQL**:

   - Install PostgreSQL on your machine from [PostgreSQL official site](https://www.postgresql.org/download/).
   - Make sure to remember the username (e.g., `postgres`) and password you set during the installation, as you'll need them for the Django database configuration.

2. **Create a Database**:
   Open the PostgreSQL terminal (or use a GUI tool like pgAdmin) and run the following commands:

   ```sql
   CREATE DATABASE ecommerce_db;
   CREATE USER ecommerce_user WITH PASSWORD 'yourpassword';
   ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
   ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE ecommerce_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
   ```

   Replace `ecommerce_db`, `ecommerce_user`, and `yourpassword` with your preferred database name, username, and password.

3. **Start PostgreSQL**: Ensure that PostgreSQL is running. You can verify this by using:
   ```bash
   sudo service postgresql status  # For Linux
   brew services start postgresql  # For Mac (Homebrew)
   ```

### Database Configuration in Django

To configure Django to use your PostgreSQL database:

1. In the Django project's root directory, create a `.env` file (if it doesn’t already exist) and add the following:

   ```bash
   DATABASE_URL=postgres://ecommerce_user:yourpassword@localhost:5432/ecommerce_db
   ```

   Replace `ecommerce_user`, `yourpassword`, and `ecommerce_db` with your PostgreSQL credentials and database name.

2. Update `settings.py` to use `django-environ` for managing environment variables:

   Install `django-environ`(It is included in `requirements.txt`):

   ```bash
   pip install django-environ
   ```

   Update your `settings.py`:

   ```python
   import environ

   # Initialise environment variables
   env = environ.Env()
   environ.Env.read_env()

   DATABASES = {
       'default': env.db(),
   }

   # Optionally, you can add other environment variable settings like DEBUG:
   DEBUG = env.bool("DEBUG", default=False)
   ```

3. Apply migrations to set up the database schema:
   ```bash
   python manage.py migrate
   ```

### Environment Variables

To run the project, you'll need to set up environment variables for both **backend** and **frontend**.

1. **Backend (.env)**:

   - `SECRET_KEY` = Your Django secret key
   - `DEBUG` = True for development
   - `DATABASE_URL` = URL for the PostgreSQL database (as explained in the Database Setup)

2. **Frontend (.env)**:
   - `REACT_APP_API_URL` = The base URL of your Django API (e.g., `http://localhost:8080/api`)

### Available Scripts

#### Backend

- `python manage.py runserver`: Start Django server
- `python manage.py migrate`: Apply migrations

#### Frontend

- `npm start`: Start React development server
- `npm build`: Create optimized production build

## API Endpoints

### Authentication

- `POST /api/login/`: User login
- `POST /api/register/`: User registration
- `GET /api/user/`: Get authenticated user's profile

### Products

- `GET /api/products/`: List all products
- `GET /api/products/:id/`: Get a single product's details

### Cart & Orders

- `POST /api/cart/`: Add item to cart
- `GET /api/cart/`: View cart items
- `POST /api/order/`: Place an order

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.