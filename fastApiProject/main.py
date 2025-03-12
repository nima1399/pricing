from fastapi import FastAPI
from contextlib import asynccontextmanager

from task_handler import TaskHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await TaskHandler.notify_handler()
    yield


app = FastAPI(lifespan=lifespan)
