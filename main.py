from fastapi import FastAPI

from crypto_getter.src.routes.crypto_getter import *
app = FastAPI(
    title="crypto checker",
    openapi_url="/openapi.json",
)
app.include_router(router, tags=["crypto"])



