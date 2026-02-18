import copy
import datetime


def build_nv_pairs(fabric):
    """
    # Summary

    Build the nvPairs object in a fabric response.
    """
    return fabric.model_dump()


def build_response(fabric):
    """
    # Summary

    Build a fabric response that aligns with FabricResponseModel

    ## Notes

    1. If FabricResponseModel is changed, this function must also be updated
    """
    response = {}
    response["id"] = fabric.id
    response["nvPairs"] = build_nv_pairs(fabric)
    return copy.deepcopy(response)


def build_404_response(path: str) -> dict:
    """
    # Summary

    Return an emulated NDFC 404 response which includes the request path.

    ## Example Response

    ```json
    {
        "timestamp": 1742232142,
        "status": 404,
        "error": "Not Found",
        "path": "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/F2/config-save"
    }
    ```
    """
    response = {}
    response["timestamp"] = int(datetime.datetime.now().timestamp())
    response["status"] = 404
    response["error"] = "Not Found"
    response["path"] = f"{path}"
    return response
