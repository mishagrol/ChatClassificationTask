from fastapi import APIRouter, FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
from app import api


logging.basicConfig(
    format="%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_application() -> FastAPI:

    router = APIRouter()
    router.include_router(
        api.router,
        tags=["Chat Message Classifier"],
    )

    application = FastAPI(
        title="Chat Message Classification System",
        version="0.0.1",
        contact={
            "name": "Misha Grol",
            "email": "grol81@mail.ru",
        },
    )

    application.include_router(router)

    return application


app = get_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
