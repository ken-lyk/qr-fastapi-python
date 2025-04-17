# QR Code Generator API

A FastAPI application to generate QR codes.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd qr-fastapi-python
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
qr-fastapi-python/
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

**Recommended (Development):**

Ensure your virtual environment is activated. Navigate to the project root directory (`qr-fastapi-python`). Then run:

```bash
fastapi dev main.py
```
This command automatically handles reloading and is generally preferred for development.

**Alternative (Using Uvicorn directly):**

Navigate to the directory *containing* your project folder (`qr-fastapi-python`). Make sure your virtual environment (located inside `qr-fastapi-python/.venv/`) is activated.

Then, run uvicorn specifying the package and module:

```bash
cd .. # Navigate one level up from qr-fastapi-python directory
python -m uvicorn qr-fastapi-python.main:app --reload
```

(Note: This method explicitly tells Python where to find the `main` module within the `qr-fastapi-python` package, which is necessary due to the relative imports used in the project.)

The API will be available at `http://127.0.0.1:8000/docs`.

## API Endpoints

*(Describe the available API endpoints here, e.g., POST /qr, GET /qr/{id})*

## Database (Optional)

If the project uses a database:

1.  Set up your database according to the configuration in `.env`.
2.  Run any necessary migrations or use the provided `seed.sql` file to initialize data.

### Updating Seed User Password

If you need to update the password for a user initially created by the `seed.sql` script (or similar seeding mechanism), follow these steps:

1.  **Ensure `SECRET_KEY` is Correct:** Verify that the `SECRET_KEY` in your `.env` file is the one currently used by the running application. The password hash depends on this key.
2.  **Generate New Hash:** Create a temporary new user through the registration API endpoint (`/users/`) with the desired new password. Note the hashed password generated for this temporary user.
3.  **Update Database:** Manually connect to your database. Locate the original seed user record in the relevant table (e.g., `users`). Update the `hashed_password` column for that user with the new hash obtained in the previous step. You can then delete the temporary user.

## Troubleshooting

### `AttributeError: module 'bcrypt' has no attribute '__about__'`

If you encounter this error when running the application, it might be due to an incompatibility between specific versions of the `passlib` and `bcrypt` libraries.

The error typically occurs in `passlib/handlers/bcrypt.py` on a line similar to:
`version = _bcrypt.__about__.__version__`

A potential workaround is to manually edit this line in your virtual environment's installed `passlib` package to:
`version = _bcrypt.__version__`

Alternatively, check for updated versions of `passlib` or `bcrypt` that might resolve this issue, or pin specific compatible versions in your `requirements.txt`.
