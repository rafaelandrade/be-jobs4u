import time
import uvicorn
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context import plugins, context
from starlette_context.middleware import RawContextMiddleware
from fastapi import FastAPI
from app.logger.log import logger
from app.routers import find_jobs_router
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI(
    title="BE - Job4U",
    description="MS Find4U API",
    version="0.0.1"
)

allowed_origins = [
    "http://localhost:3000",
]

async def catch_exception_middleware(request: Request, call_next):
    logger.send_log({
        "method": request.method,
        "path": request.url.path,
        "protocol": request.url.scheme
    })

    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = round((time.time() - start_time) * 1000, 2)
        logger.send_log({"process_time": process_time,
                        "status": response.status_code})

        return response
    except Exception as exception:
        logger.send_error(exception)

        return JSONResponse({
            "error": True,
            "message": "Internal server error"},
            status_code=500)



app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware('http')(catch_exception_middleware)
app.add_middleware(RawContextMiddleware, plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()))

app.include_router(find_jobs_router.router)
handler = Mangum(app)


@app.get("/")
async def root():
    return {'message': 'Hello from Jobs4U'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)