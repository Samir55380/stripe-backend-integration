from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src import logger

api_controller = APIRouter(tags=["Stripe API Integration"])

@api_controller.post("/create_checkout_session")
async def create_checkout_session():
    """
    Create a new checkout session
    """
    logger.info("create_checkout_session")
    return JSONResponse(content={"message": "create_checkout_session"})