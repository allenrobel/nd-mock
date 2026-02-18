#!/usr/bin/env python
"""
# Summary

Retrieve all endpoints from an OpenAPI schema and format them for
use in the README.md file.
"""
import json
from os import environ
from typing import Any

import requests


def get_endpoints_data(url: str) -> dict:
    """
    # Summary

    Issue a GET request for the url and return the JSON response.
    """
    response = requests.get(url, timeout=5)
    return response.json()


def dump_endpoints(data: dict) -> None:
    """
    # Summary

    Dump the data to a file.
    """
    print(json.dumps(data, indent=2))


def get_endpoints_paths(data: dict) -> dict:
    """
    # Summary

    Process the data from the OpenAPI schema and return the paths.
    """
    return data["paths"]


def print_endpoints(endpoints: dict) -> None:
    """
    # Summary

    Print the endpoints to the console.
    """
    for path, info in endpoints.items():
        print(f"- `{path}`")
        for method, method_info in info.items():
            print(f"  - `{method}`")
            print(f"    - {method_info.get('summary')}")


def group_endpoints_by_tag(endpoints: dict) -> dict:
    """
    # Summary

    Return the endpoints grouped by tag.
    """
    tags: dict[str, Any] = {}
    for path, info in endpoints.items():
        for method, method_info in info.items():
            if "tags" not in method_info:
                tag = "Default"
            else:
                tag = method_info.get("tags")[0]
            if tag not in tags:
                tags[tag] = []
            tags[tag].append((path, method, method_info.get("summary")))
    return tags


def write_endpoints_to_markdown(lines: list) -> None:
    """
    # Summary

    Write the endpoints to a markdown file.
    """
    home = environ["HOME"]
    repo = f"{home}/repos/podman/ndfc_mock"
    filename = f"{repo}/docs/supported_endpoints.md"

    if lines[-1] == "" and lines[-2] == "":
        lines.pop()

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    """
    # Summary

    Retrieve all endpoints from an OpenAPI schema, and print them to the
    console; formatted for use in the README.md file in this repository.
    """
    url = "http://localhost:8000/openapi.json"

    data = get_endpoints_data(url)
    # dump_endpoints(data)
    endpoints = get_endpoints_paths(data)
    # print(json.dumps(endpoints, indent=2))
    # print_endpoints(endpoints)
    tags = group_endpoints_by_tag(endpoints)
    lines = []
    lines.append("# Supported Endpoints")
    lines.append("")
    lines.append("- V1 denotes Nexus Dashboard 3.x endpoint")
    lines.append("- V2 denotes Nexus Dashboard 4.x endpoint")
    lines.append("- We are migrating endpoints out of Default and into their respective tags over the next week or so...")
    lines.append("")
    for tag, endpoints in tags.items():
        lines.append(f"## {tag}")
        lines.append("")
        for path, method, summary in endpoints:
            lines.append(f"- `{path}`")
            lines.append(f"  - `{method}`")
            lines.append(f"    - {summary}")
            lines.append("")

    write_endpoints_to_markdown(lines)


if __name__ == "__main__":
    main()
