from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import admin, expansion, info, village,eco,assignments
import json
import logging


description = """
Virtual Ecosystem (insert cool description here)
"""

app = FastAPI(
    title="Virtual Ecosystem",
    description=description,
    version="1.0.0",
)


app.include_router(expansion.router)
app.include_router(admin.router)
app.include_router(info.router)
app.include_router(village.router)
app.include_router(eco.router)
app.include_router(assignments.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Another cool message here"}
