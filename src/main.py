from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# from starlette.middleware.cors import CORSMiddleware

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operation
from src.tasks.router import router as router_tasks

from redis import asyncio as aioredis

app = FastAPI(
    title="Trading App"
)


@app.get('/')
async def index():
    return {'index': 'Main Page'}


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(router_operation)
app.include_router(router_tasks)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# ###############################################
# ######### TO CONNECT WITH FRONTEND ############
# origins = [
#     "http://localhost:8000",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
#     allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
#                    "Authorization"],
# )
# ###############################################
