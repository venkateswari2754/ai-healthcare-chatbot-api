from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.endpoints import user  # 👈 make sure this is correct!
from app.api.api_v1.endpoints import order 


app = FastAPI()

# Allow Angular dev server to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(order.router, prefix="/api/v1/orders", tags=["orders"])