import random
import string
from datetime import datetime

from fastapi import HTTPException


def get_datetime() -> datetime:
    """
    We specifically do NOT want to store timezone info
    in the datetime object since we don't need it.  Rather,
    we are treating datetime like a timestamp.
    """
    return datetime.now().replace(tzinfo=None)


def gen_hex(length) -> str:
    """
    Generate a random hex string of length `length`.
    """
    return "".join(random.choice("0123456789ABCDEF") for _ in range(length))


def gen_number(length) -> str:
    """
    Generate a random number of length `length`.
    """
    return "".join(random.choice("0123456789") for _ in range(length))


def gen_string(length) -> str:
    """
    Generate a random alphabetic string of length `length`.
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def random_unicast_mac_address() -> str:
    """
    Generate a random unicast MAC address, with an OUI of 00:AA:BB.
    """
    return f"00:AA:BB:{gen_hex(2)}:{gen_hex(2)}:{gen_hex(2)}"


def random_switch_serial_number() -> str:
    """
    # Summary

    Generate a random switch serial number.

    FOX2109PGCS
    """
    return f"FOX{gen_number(4)}{gen_string(4).upper()}"


external_role_to_db = {
    "access": "access",
    "aggregation": "aggregation",
    "border": "border",
    "border gateway": "border_gateway",
    "border gateway spine": "border_gateway_spine",
    "border gateway super spine": "border_gateway_super_spine",
    "border spine": "border_spine",
    "border super spine": "border_super_spine",
    "core router": "core_router",
    "edge router": "edge_router",
    "leaf": "leaf",
    "spine": "spine",
    "super spine": "super_spine",
    "tier2 leaf": "tier2_leaf",
    "tor": "tor",
}
db_to_external_role = {v: k for k, v in external_role_to_db.items()}


def switch_role_db_to_external(role: str) -> str:
    """
    # Summary

    Map a user switch role name to a database switch role key.

    For example:

    "border gateway spine" -> "border_gateway_spine"

    # Parameters

    - role: The external switch role (e.g. "border gateway spine", "edge router", etc).

    # Returns

    The key used internally for the role (e.g. "border_gateway_spine", "edge_router", etc).
    """
    return_role = db_to_external_role.get(role)
    if not return_role:
        msg = f"Invalid role: {role}."
        raise HTTPException(status_code=500, detail=msg)
    return return_role


def switch_role_external_to_db(role: str) -> str:
    """
    # Summary

    Map a user switch role name to a database switch role key.

    For example:

    "border gateway spine" -> "border_gateway_spine"

    # Parameters

    - role: The external switch role (e.g. "border gateway spine", "edge router", etc).

    # Returns

    The key used internally for the role (e.g. "border_gateway_spine", "edge_router", etc).
    """
    return_role = external_role_to_db.get(role)
    if not return_role:
        msg = f"Invalid role: {role}."
        raise HTTPException(status_code=500, detail=msg)
    return return_role
