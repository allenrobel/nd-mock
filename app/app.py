#!/usr/bin/env python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import create_db_and_tables


@asynccontextmanager
async def lifespan(runner: FastAPI):
    """
    App entry point.

    Place startup code before the yield statement.
    Place cleanup code after the yield statement.
    """
    print(f"app version {runner.version}. Creating db and tables")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
