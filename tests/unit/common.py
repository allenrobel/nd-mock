#!/usr/bin/env python

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import get_session
from app.main import app


def get_timestamp_from_tz_aware_datetime_string(date_str):
    """
    # Summary

    Convert a timezone aware date to a unix timestamp.

    ## Example input (type: str)

    2025-02-13T18:31:41.162512

    ## Example output (type: float)

    1739507501.162512
    """
    print(f"type(date_str): {type(date_str)} date_str: {date_str}")
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    dt = datetime.strptime(date_str, date_format)
    dt = dt.replace(tzinfo=None)
    return dt.timestamp()


def get_timestamp_from_datetime(dt):
    """
    # Summary

    Given a datetime object, return a timestamp.
    """
    return dt.timestamp()


def convert_model_date_to_timestamp(date_obj):
    """
    # Summary

    Given a datetime object, return a unix timestamp.
    """
    return get_timestamp_from_datetime(date_obj)


def convert_db_date_to_timestamp(date_str):
    """
    # Summary

    Given a datetime string in timezone-aware format, return
    a unix timestamp.
    """
    return get_timestamp_from_tz_aware_datetime_string(date_str)


def timestamps_within_delta(ts1, ts2, delta=900000):
    """
    # Summary

    Compare two unix timestamps by converting them
    to datetime objects and using timedelta to verify
    if ts2 - ts1 <= delta microseconds.

    ## Examples

    ts1 = 1739508125.401565
    ts2 = 1739508125.403565
    delta = 403565 - 401565
    result = timestamps_within_delta(ts1, ts2, delta=delta) # True
    result = timestamps_within_delta(ts1, ts2, delta=delta-1) # False

    Return True if delta is <= delta microseconds.
    Return False otherwise.
    """
    print(f"timestamps_within_delta: ts1: {ts1}")
    print(f"timestamps_within_delta: ts2: {ts2}")
    dt1 = datetime.fromtimestamp(ts1)
    dt2 = datetime.fromtimestamp(ts2)
    print(f"dt2 - dt1: {dt2 - dt1}")
    return dt2 - dt1 <= timedelta(microseconds=delta)


@pytest.fixture(name="session")
def session_fixture():
    """
    # Summary

    Return a SQLModel Session() instance that interacts with an in-memory
    database.
    """
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    # Summary

    yield a FastAPI TestClient() instance.

    After the calling test case completes, execution continues
    after the yield statement to clear the SQLModel Session.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
