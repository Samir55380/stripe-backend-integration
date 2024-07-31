import uvicorn
from dotenv import load_dotenv
import os
from src import app
from src.controller.api_controller import api_controller



app.include_router(api_controller)

if __name__ == "__main__":
    load_dotenv()
    port = os.getenv("PORT", "8000")
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), reload=True)