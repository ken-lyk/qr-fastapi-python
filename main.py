# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the authentication router and dependencies
from .routers import auth, user, qr


app = FastAPI(title="QR Reader")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the authentication router
# All routes defined in auth_router will be available under the /auth prefix
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(qr.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}