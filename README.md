# Cloud Storage Server

This is a cloud storage server built with Django REST Framework. It provides an API for managing users and files in the cloud.

## Features

- User rigistration & authorization
- Token-based authentication
- User management
- File management

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DexRam/CS-01-Server-DjangoRESTFramework-cloudStorage
    cd CS-01-Server-DjangoRESTFramework-cloudStorage
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up the settings:

    a. Go to cloudStorage - settings.py
    b. Configure DATABASES = {}
    c. Configure ALLOWED_HOSTS = []
    d. Configure CORS_ALLOWED_ORIGINS = []

5. Set up the database:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Endpoints

### UserViewSet Endpoints

#### Register
- **URL:** `/api/users/register/`
- **Method:** `POST`
- **Permission:** `AllowAny`

#### Login
- **URL:** `/api/users/login/`
- **Method:** `POST`
- **Permission:** `AllowAny`

#### Get Current User
- **URL:** `/api/users/me/`
- **Method:** `GET`
- **Permission:** `IsAuthenticated`

### FileViewSet Endpoints

#### Upload File
- **URL:** `/api/files/upload-file/`
- **Method:** `POST`
- **Permission:** `IsAuthenticated`

#### Update File
- **URL:** `/api/files/{id}/update-file/`
- **Method:** `PATCH`
- **Permission:** `IsAuthenticated`

#### Download File
- **URL:** `/api/files/{id}/download-file/`
- **Method:** `GET`
- **Permission:** `IsAuthenticated`

#### Share File
- **URL:** `/api/files/{id}/share-file/`
- **Method:** `POST`
- **Permission:** `IsAuthenticated`

#### Delete File
- **URL:** `/api/files/{id}/delete-file/`
- **Method:** `DELETE`
- **Permission:** `IsAuthenticated`

#### Get User Files
- **URL:** `/api/files/user-files/`
- **Method:** `POST`
- **Permission:** `IsAuthenticated`

#### Download Shared File
- **URL:** `/api/files/download-shared/{share_link}/`
- **Method:** `GET`
- **Permission:** `AllowAny`

### Standard ModelViewSet Endpoints (for UserViewSet and FileViewSet)

#### List
- **URL:** `/api/users/` or `/api/files/`
- **Method:** `GET`
- **Permission:** `IsAuthenticated, IsAdminUser`

#### Create
- **URL:** `/api/users/` or `/api/files/`
- **Method:** `POST`
- **Permission:** `IsAuthenticated, IsAdminUser`

#### Retrieve
- **URL:** `/api/users/{id}/` or `/api/files/{id}/`
- **Method:** `GET`
- **Permission:** `IsAuthenticated, IsAdminUser`

#### Update
- **URL:** `/api/users/{id}/` or `/api/files/{id}/`
- **Method:** `PUT`
- **Permission:** `IsAuthenticated, IsAdminUser`

#### Partial Update
- **URL:** `/api/users/{id}/` or `/api/files/{id}/`
- **Method:** `PATCH`
- **Permission:** `IsAuthenticated, IsAdminUser`

#### Destroy
- **URL:** `/api/users/{id}/` or `/api/files/{id}/`
- **Method:** `DELETE`
- **Permission:** `IsAuthenticated, IsAdminUser`

These endpoints cover user registration, authentication, file upload, download, sharing, and management functionalities.


## Contributing
1. Fork the repository
2. Create a new branch (git checkout -b feature-branch)
3. Commit your changes (git commit -am 'Add new feature')
4. Push to the branch (git push origin feature-branch)
5. Create a new Pull Request

## License
This project is licensed under the MIT License.
Feel free to customize it according to your project's specific details and requirements.