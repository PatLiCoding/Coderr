# Coderr – Freelancer Platform Backend

Coderr is a RESTful backend API for a freelancer marketplace platform. It provides authentication, profile management, service offers, order processing, reviews, and aggregated platform statistics.

The project is built with Django and Django REST Framework and serves as the backend layer for a separate frontend application.

---

## Table of Contents


- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Run the Development Server](#run-the-development-server)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Profiles](#profiles)
  - [Offers](#offers)
  - [Orders](#orders)
  - [Reviews](#reviews)
  - [Statistics](#statistics)
- [Project Structure](#project-structure)
- [License](#license)
- [Author](#author)

---

## Features

### Authentication

* User registration
* User login
* Token-based authentication

### Profile Management

* Business and customer profiles
* Profile retrieval and updates
* Separate profile listings by user type

### Offer Management

* Create, update, and delete service offers
* Offer detail views
* Filtering and ordering support

### Order Management

* Create and manage orders
* Track order status
* Business-specific order statistics

### Review System

* Create reviews for completed orders
* Update and delete reviews
* Review listings

### Platform Statistics

* Aggregated dashboard information
* Global platform metrics via dedicated endpoints

---

## Tech Stack

* Python 3
* Django
* Django REST Framework
* django-filter
* django-cors-headers
* python-dotenv

### Testing

* pytest
* pytest-cov

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd coderr-backend
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_django_key
```

You can create it from the template:

```bash
cp .env.template .env
```

---

## Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov
```

---

## Test Coverage

The project includes comprehensive API tests covering:

* Authentication
* Permissions
* CRUD operations
* Validation rules
* Business logic
* Aggregation endpoints

Coverage is measured using pytest-cov.

---

## API Endpoints

### Authentication

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | `/api/registration/` |
| POST   | `/api/login/`        |

---

### Profiles

| Method | Endpoint                  |
| ------ | ------------------------- |
| GET    | `/api/profile/<id>/`      |
| PATCH  | `/api/profile/<id>/`      |
| GET    | `/api/profiles/business/` |
| GET    | `/api/profiles/customer/` |

---

### Offers

| Method | Endpoint                  |
| ------ | ------------------------- |
| GET    | `/api/offers/`            |
| POST   | `/api/offers/`            |
| GET    | `/api/offers/<id>/`       |
| PATCH  | `/api/offers/<id>/`       |
| DELETE | `/api/offers/<id>/`       |
| GET    | `/api/offerdetails/<id>/` |

---

### Orders

| Method | Endpoint                                         |
| ------ | ------------------------------------------------ |
| GET    | `/api/orders/`                                   |
| POST   | `/api/orders/`                                   |
| PATCH  | `/api/orders/<id>/`                              |
| DELETE | `/api/orders/<id>/`                              |
| GET    | `/api/order-count/<business_user_id>/`           |
| GET    | `/api/completed-order-count/<business_user_id>/` |

---

### Reviews

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | `/api/reviews/`      |
| POST   | `/api/reviews/`      |
| PATCH  | `/api/reviews/<id>/` |
| DELETE | `/api/reviews/<id>/` |

---

### Statistics

| Method | Endpoint          |
| ------ | ----------------- |
| GET    | `/api/base-info/` |

---

## Project Structure

```text
auth_app/
offers_app/
orders_app/
profiles_app/
reviews_app/

backend/
manage.py
requirements.txt
```

---

## License

This project was developed as part of a web development learning project and portfolio application.

## Author

Developed by Patricia Linne
