# QR Code Generator API

A FastAPI application to generate QR codes.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd qr-fastapi
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the project root. You can copy the structure from the example below. This file stores sensitive configuration like database credentials and secret keys. **Make sure this file is included in your `.gitignore` to avoid committing sensitive information.**

    Example `.env` structure:
    ```dotenv
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=3306 # Or your database port
    DATABASE_PASSWORD=your_db_password
    DATABASE_NAME=qr_app_db
    DATABASE_USERNAME=your_db_username
    SECRET_KEY=a_very_strong_random_secret_key # Generate using: openssl rand -hex 32
    ALGORITHM=HS256 # Algorithm for JWT
    ACCESS_TOKEN_EXPIRE_MINUTES=60 # Token expiry time in minutes
    ```
    Fill in the actual values for your environment.

## Project Structure

```
qr-fastapi/
├── .venv/                 # Virtual environment directory
├── config/
│   ├── config.py          # Loads environment variables using Pydantic Settings
│   └── database.py        # Database connection setup (SQLAlchemy)
├── routers/
│   ├── auth.py            # Authentication endpoints (login)
│   ├── qr.py              # QR code generation/management endpoints
│   └── user.py            # User creation endpoints
├── schemas/
│   ├── qrSchemas.py       # Pydantic schemas for QR code data
│   ├── schemas.py         # Common/Base Pydantic schemas
│   └── userSchemas.py     # Pydantic schemas for User data and tokens
├── utility/
│   ├── enums.py           # Enum definitions
│   ├── oauth2.py          # OAuth2 password flow and JWT handling
│   └── qrUtil.py          # Utility functions for QR code generation
├── .env                   # Environment variables (DATABASE_URL, SECRET_KEY, etc.) - **DO NOT COMMIT**
├── .gitignore             # Specifies intentionally untracked files that Git should ignore
├── main.py                # Main FastAPI application entry point
├── models.py              # SQLAlchemy database models
├── requirements.txt       # Project dependencies
├── seed.sql               # Optional SQL script for initial database seeding
└── README.md              # This file
```

## Running the Application

Use uvicorn to run the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

*(Describe the available API endpoints here, e.g., POST /qr, GET /qr/{id})*

## Database (Optional)

If the project uses a database:

1.  Set up your database according to the configuration in `.env`.
2.  Run any necessary migrations or use the provided `seed.sql` file to initialize data.

## Contributing

*(Add guidelines for contributing if applicable)*

## License

*(Specify the project license)*
