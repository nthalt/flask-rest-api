# Flask REST API with User Management

This project is a JSON RESTful API built with Flask, following OpenAPI standards. It uses PostgreSQL with SQLAlchemy for database management and includes user authentication and management features.

-   [Desription](#description)
-   [Features](#features)
-   [Setup and Installation](#setup-and-installation)
-   [API Documentation](#api-documentation)
    -   [Authentication](#authentication)
        -   [Register](#register-a-new-user)
        -   [Login](#user-login)
        -   [Forgot Password](#forgot-password)
        -   [Reset Password](#reset-password)
        -   [Change password](#change-password)
    -   [Users](#users)
        -   [Get all users](#get-all-users)
        -   [Get user by id](#get-user-by-id)
        -   [Update user](#update-user)
        -   [Delete user](#delete-user)
        -   [Promote user to admin](#promote-user-to-admin)
-   [User Roles and Permissions](#user-roles-and-permissions)
-   [Development](#development)
-   [Contributing](#contributing)

## Description

The API is built using Flask and PostgreSQL with SQLAlchemy. It provides user management functionalities including registration, sign-in, password forget, password reset and admin-level user management.

## Features

1. Utilizes appropriate REST methods
2. Uses SQLAlchemy and PostgreSQL for database models and schema. Database and table will be automatically created if it does not exist
3. Implements user registration, sign-in, password forget, password reset functionalities
4. Admin users can modify, delete, activate, and deactivate non-admin users
5. Admin can make other user admin, but cannot modify other existing admin
6. User information stored includes:
    - Username (varchar)
    - User First Name (varchar)
    - User Last Name (varchar)
    - Password (encrypted, varchar)
    - Email (varchar)
    - Role (Admin/User, Enum)
    - Create date (datetime, auto-insert)
    - Update date (datetime, auto-update during REST API calls)
    - Active status (Boolean)
7. Implements JWT Token authentication

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/nthalt/flask-rest-api.git
cd flask-rest-api
```

2. Create and activate a virtual environment:

```python
python -m venv venv
source venv/bin/activate  # On Windows use: source venv\Scripts\activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

5. Create a file named .env in project root and copy your own configuration values into it according to the format provided in .env.example

```bash
cp .env.example .env
```

4. Set up your PostgreSQL database and update the `.env` file with your database URL:

```
DATABASE_URL=postgresql://DATABASE_username:DATABASE_password@localhost:5432/DATABASE_name
```

6. Run the application:

```
python run.py run
```

The application will create the necessary database and tables if they don't exist.

To create an admin user:

```bash
python run.py create_admin
```

## API Documentation

The API follows OpenAPI standards and provides JSON responses. You can access the Swagger UI documentation at `http://127.0.0.1:5000/` when running the application.

### Endpoints

#### Authentication

-   **POST /auth/register** - Register a new user
-   **POST /auth/login** - User login
-   **POST /auth/forgot-password** - Request password reset
-   **POST /auth/reset-password** - Reset password
-   **POST /auth/change-password** - Change password

#### Users

-   **GET /users/** - Get all users (Admin only)
-   **GET /users/:id** - Get user by ID (Admin or own user)
-   **PUT /users/:id** - Update user (Admin or own user)
-   **DELETE /users/:id** - Delete user (Admin only)
-   **POST /users/promote/:id** - Promote user to Admin (Admin only)

### Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header of your requests according to the format:

Authorization: Bearer your_jwt_token

### Testing Instructions

#### Register a New User

-   **Method:** POST
-   **URL:** `/auth/register`

**Example:**

```bash
curl -X POST http://localhost:5000/auth/register \
-H "Content-Type: application/json" \
-d '{"username": "john_doe", "password": "SecureP@ssw0rd", "email": "john@example.com", "first_name": "John", "last_name": "Doe"}'
```

**Request Body:**

```json
{
    "username": "john_doe",
    "password": "SecureP@ssw0rd",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Expected Response:**

```json
{
    "message": "User created successfully"
}
```

#### User Login

-   **Method:** `POST`
-   **URL:** `/auth/login`

**Example:**

```bash
curl -X POST http://localhost:5000/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "john_doe", "password": "SecureP@ssw0rd"}'
```

**Request Body**

```json
{
    "username": "john_doe",
    "password": "SecureP@ssw0rd"
}
```

**Expected Response:**

```json
{
    "access_token": "your_jwt_token"
}
```

#### Forgot Password

-   Method: POST
-   URL: /auth/forgot-password

**Example:**

```bash

curl -X POST http://localhost:5000/auth/forgot-password \
-H "Content-Type: application/json" \
-d '{"email": "john@example.com"}'
```

**Request Body**

```json
{
    "email": "john@example.com"
}
```

**Expected Response:**

```json
{
    "message": "If a user with this email exists, a password reset link has been sent."
}
```

#### Reset Password

-   Method: POST
-   URL: /auth/reset-password

**Example:**

```bash

curl -X POST http://localhost:5000/auth/reset-password \
-H "Content-Type: application/json" \
-d '{"token": "reset_token", "new_password": "NewSecureP@ssw0rd"}'
```

**Request Body**

```json
{
    "token": "reset_token",
    "new_password": "NewSecureP@ssw0rd"
}
```

**Expected Response:**

```json
{
    "message": "Password has been reset successfully"
}
```

#### Change Password

-   Method: POST
-   URL: /auth/change-password

**Example:**

```bash

curl -X POST http://localhost:5000/auth/change-password \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"current_password": "SecureP@ssw0rd", "new_password": "NewSecureP@ssw0rd"}'
```

**Request Header**

```http
Authorization: Bearer your_jwt_token
```

**Request Body**

```json
{
    "current_password": "SecureP@ssw0rd",
    "new_password": "NewSecureP@ssw0rd"
}
```

**Expected Response:**

```json
{
    "message": "Password changed successfully"
}
```

#### Get All Users

-   Method: GET
-   URL: /users/

**Example:**

```bash

curl -X GET http://localhost:5000/users/ \
-H "Authorization: Bearer your_jwt_token"
```

**Request Header**

```http
Authorization: Bearer your_jwt_token
```

**Expected Response:**

```json
[
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "User",
        "is_active": true,
        "created_at": "2024-07-05T12:00:00Z",
        "updated_at": "2024-07-05T12:00:00Z"
    }
    // more users
]
```

#### Get User by ID

-   Method: GET
-   URL: /users/{id}

**Example:**

```bash

curl -X GET http://localhost:5000/users/1 \
-H "Authorization: Bearer your_jwt_token"
```

**Request Header**

```http
Authorization: Bearer your_jwt_token
```

**Expected Response:**

```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "User",
    "is_active": true,
    "created_at": "2024-07-05T12:00:00Z",
    "updated_at": "2024-07-05T12:00:00Z"
}
```

#### Update User

-   Method: PUT
-   URL: /users/{id}

**Example:**

```bash

curl -X PUT http://localhost:5000/users/1 \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"username": "john_doe", "email": "john@example.com", "first_name": "John", "last_name": "Doe", "role": "User", "is_active": false}'
```

**Request Header**

```http
Authorization: Bearer your_jwt_token
```

**Request Body**

```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "User",
    "is_active": false
}
```

**Expected Response:**

```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "User",
    "is_active": false,
    "created_at": "2024-07-05T12:00:00Z",
    "updated_at": "2024-07-05T12:00:00Z"
}
```

#### Delete User

-   Method: DELETE
-   URL: /users/{id}

**Example:**

```bash

curl -X DELETE http://localhost:5000/users/1 \
-H "Authorization: Bearer your_jwt_token"
```

**Request Header**

```http
Authorization: Bearer your_jwt_token
```

**Expected Response:**

```json
{
    "message": "User deleted"
}
```

#### Promote User to Admin

-   Method: POST
-   URL: /users/promote/{id}

**Example:**

```bash

curl -X POST http://localhost:5000/users/promote/1 \
-H "Authorization: Bearer your_jwt_token"
```

**Request Header**

```http
Authorization: Bearer your_jwt_token
```

**Expected Response:**

```json
{
    "message": "User promoted to Admin"
}
```

## User Roles and Permissions

-   **User**: Can view and edit their own information
-   **Admin**: Can view, edit, delete, and promote all users (except deleting other admins)

## Contributing

We welcome contributions to this project. To ensure a smooth collaboration, please follow these guidelines:

1. **Fork the Repository**: Start by forking the repository on GitHub.

2. **Clone the Repository**: Clone your forked repository to your local machine using:

    ```bash
    git clone https://github.com/your-username/flask-rest-api.git
    ```

3. **Create a Branch**: Create a new branch for your feature or bug fix:

    ```bash
    git checkout -b feature-or-bugfix-description
    ```

4. **Make Changes**: Implement your changes in the codebase. Ensure your code adheres to the project's coding standards and includes appropriate tests.

5. **Commit Changes**: Commit your changes with a clear and descriptive commit message:

    ```bash
    git add .
    git commit -m "Description of the feature or bug fix"
    ```

6. **Push to GitHub**: Push your branch to your forked repository on GitHub:

    ```bash
    git push origin feature-or-bugfix-description
    ```

7. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request. Provide a clear and detailed description of your changes.

8. **Review Process**: Wait for the project maintainers to review your pull request. Be prepared to make any necessary changes based on feedback.

Thank you for your contributions! Your help is greatly appreciated.
