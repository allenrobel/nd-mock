#!/usr/bin/env python
import json

from fastapi import APIRouter, HTTPException

from ......models.configtemplate_easy_fabric import V1ConfigtemplateEasyFabricResponseModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates",
)


@router.get(
    "/{template_name}",
    response_model=V1ConfigtemplateEasyFabricResponseModel,
    description="(v1) Get a configuration template by name.",
)
def v1_get_configtemplate_by_name(template_name: str):
    """
    # Summary

    GET request handler.
    """
    try:
        with open(f"app/v1/templates/{template_name}.json", "r", encoding="utf-8") as template:
            response = json.load(template)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Template {template_name} not found.") from error
    return response
