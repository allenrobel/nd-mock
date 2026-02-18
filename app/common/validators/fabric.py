import re

from pydantic import AfterValidator
from typing_extensions import Annotated


def validate_bgp_asn(bgp_asn: str) -> str:
    """
    Validate BGP ASN format.
    """
    # pylint: disable=line-too-long
    re_bgp_asn = re.compile(
        "^(((\\+)?[1-9]{1}[0-9]{0,8}|(\\+)?[1-3]{1}[0-9]{1,9}|(\\+)?[4]{1}([0-1]{1}[0-9]{8}|[2]{1}([0-8]{1}[0-9]{7}|[9]{1}([0-3]{1}[0-9]{6}|[4]{1}([0-8]{1}[0-9]{5}|[9]{1}([0-5]{1}[0-9]{4}|[6]{1}([0-6]{1}[0-9]{3}|[7]{1}([0-1]{1}[0-9]{2}|[2]{1}([0-8]{1}[0-9]{1}|[9]{1}[0-5]{1})))))))))|([1-5]\\d{4}|[1-9]\\d{0,3}|6[0-4]\\d{3}|65[0-4]\\d{2}|655[0-2]\\d|6553[0-5])(\\.([1-5]\\d{4}|[1-9]\\d{0,3}|6[0-4]\\d{3}|65[0-4]\\d{2}|655[0-2]\\d|6553[0-5]|0))?)$"  # noqa: E501
    )
    if not re.match(re_bgp_asn, str(bgp_asn)):
        raise ValueError("Invalid BGP ASN format")
    return bgp_asn


BgpValue = Annotated[str, AfterValidator(validate_bgp_asn)]
