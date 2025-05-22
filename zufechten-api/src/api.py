from app.app import app
from router.main import api_router

app.include_router(api_router)
