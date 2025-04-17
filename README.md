# QR Reader FastAPI Python API

A FastAPI application to read QR codes.

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
├── .venv/                 # Virtual environment directory (managed by user)
├── config/
│   ├── config.py          # Loads environment variables using Pydantic Settings
│   └── database.py        # Database connection setup (SQLAlchemy)
├── models/
│   ├── models.py          # Base model and relationship configurations (if applicable)
│   ├── qrModel.py         # SQLAlchemy model for QR data
│   └── userModel.py       # SQLAlchemy model for User data
├── routers/
│   ├── auth.py            # Authentication endpoints (login, register, token)
│   ├── qr.py              # QR code management endpoints
│   └── user.py            # User management endpoints
├── schemas/
│   ├── qrSchemas.py       # Pydantic schemas for QR code data
│   ├── schemas.py         # Common/Base Pydantic schemas
│   └── userSchemas.py     # Pydantic schemas for User data and tokens
├── utility/
│   ├── enums.py           # Enum definitions
│   ├── oauth2.py          # OAuth2 password flow and JWT handling
│   └── qrUtil.py          # Utility functions for QR code processing
├── .env                   # Environment variables (DATABASE_*, SECRET_KEY, etc.) - **DO NOT COMMIT**
├── .gitignore             # Specifies intentionally untracked files that Git should ignore
├── main.py                # Main FastAPI application entry point
├── requirements.txt       # Project dependencies
├── readme.md              # This file
└── seed.sql               # Optional SQL script for initial database seeding
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

Here are the available API endpoints:

**Authentication (`/auth`)**

*   `POST /auth/register`: Register a new user.
*   `POST /auth/login`: Log in using email and password, returns a JWT token.
*   `POST /auth/token`: Log in using `OAuth2PasswordRequestForm` (typically used by Swagger UI/FastAPI docs), returns a JWT token.

**QR Codes (`/qr`)**

*   `GET /qr/{id}`: Get details of a specific QR code by its ID (requires authentication).
*   `GET /qr/`: Get a list of all QR codes for the current user (or all QR codes if the user is an admin) (requires authentication).
*   `POST /qr/`: Create a new QR code record from direct data (requires authentication).
*   `POST /qr/qr-image-data`: Create a new QR code record by decoding Base64 image data (requires authentication).
*   `POST /qr/qr-image-file`: Create a new QR code record by decoding an uploaded image file (requires authentication).
*   `DELETE /qr/{id}`: Delete a specific QR code by its ID (requires admin privileges).

**Users (`/users`)**

*   `GET /users/{id}`: Get details of a specific user by ID (requires admin privileges).
*   `GET /users/`: Get a list of all users (requires admin privileges).
*   `DELETE /users/{id}`: Delete a specific user by ID (requires admin privileges).

*(Note: Authentication details (e.g., sending the Bearer token) are handled via standard FastAPI mechanisms. Refer to the `/docs` endpoint for interactive testing and schema details.)*

## Database (Optional)

If the project uses a database:

1.  Set up your database according to the configuration in `.env`.
2.  Run any necessary migrations or use the provided `seed.sql`