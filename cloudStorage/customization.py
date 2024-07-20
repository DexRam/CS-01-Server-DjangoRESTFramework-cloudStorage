from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zordtkukn0kt16)h^g&t7(vb%^1xk2zkj*^u9l0xw8uvt4g*+%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "mydatabase",
#         "USER": "mydatabaseuser",
#         "PASSWORD": "mypassword",
#         "HOST": "127.0.0.1",
#         "PORT": "5432",
#     }
# }


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

ALLOWED_HOSTS = []


FILES_DIRECTORY = Path(BASE_DIR, "files")
