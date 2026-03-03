import os


BASE_URL = os.getenv("UI_BASE_URL", "http://127.0.0.1:5000")
PETSTORE_BASE_URL = os.getenv("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2")

# Sekrety trzymamy w zmiennych srodowiskowych, a nie w kodzie.
PETSTORE_API_KEY = os.getenv("PETSTORE_API_KEY")
