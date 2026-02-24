#!/usr/bin/env python
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=invalid-name
import json

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v1.models.fabric import FabricDbModel
from app.v1.models.switch import SwitchDbModel
from app.v1.models.vrf import VrfAttachmentDbModel, VrfDbModel
from ..common import client_fixture, session_fixture


def _create_fabric(session: Session, name: str = "f1") -> FabricDbModel:
    fabric = FabricDbModel(
        management='{"bgpAsn": "65001", "type": "vxlanIbgp"}',
        category="fabric",
        latitude=71.1,
        longitude=61.1,
        licenseTier="premier",
        name=name,
        securityDomain="all",
        telemetryCollectionType="inBand",
        telemetrySourceInterface="Ethernet1/1",
        telemetrySourceVrf="vrf_1",
        telemetryStreamingProtocol="ipv4",
    )
    session.add(fabric)
    session.commit()
    return fabric


def _create_switch(session: Session, fabric_name: str = "f1", switch_id: str = "SAL1111", hostname: str = "leaf1", role: str = "leaf") -> SwitchDbModel:
    switch = SwitchDbModel(
        switchId=switch_id,
        fabricName=fabric_name,
        fabricManagementIp="10.1.1.1",
        hostname=hostname,
        model="N9K-C93180YC-FX",
        serialNumber=switch_id,
        softwareVersion="10.3(3)",
        switchRole=role,
    )
    session.add(switch)
    session.commit()
    return switch


def _create_vrf(
    session: Session,
    fabric_name: str = "f1",
    vrf_name: str = "MyVRF_50000",
    vrf_id: int = 50000,
    vlan_id: int = 2000,
    extra_data: str = "{}",
) -> VrfDbModel:
    vrf = VrfDbModel(
        id=f"{fabric_name}:{vrf_name}",
        fabricName=fabric_name,
        vrfName=vrf_name,
        vrfType="",
        vrfId=vrf_id,
        vlanId=vlan_id,
        vrfStatus="",
        tenantName="",
        extraData=extra_data,
    )
    session.add(vrf)
    session.commit()
    return vrf


def _create_vrf_attachment(
    session: Session,
    fabric_name: str = "f1",
    vrf_name: str = "MyVRF_50000",
    switch_id: str = "SAL1111",
    status: str = "notApplicable",
    attach: bool = False,
) -> VrfAttachmentDbModel:
    attachment = VrfAttachmentDbModel(
        id=f"{fabric_name}:{vrf_name}:{switch_id}",
        fabricName=fabric_name,
        vrfName=vrf_name,
        switchId=switch_id,
        status=status,
        attach=attach,
    )
    session.add(attachment)
    session.commit()
    return attachment


# ---------------------------------------------------------------------------
# POST /fabrics/{fabricName}/vrfs
# ---------------------------------------------------------------------------


def test_v1_vrf_post_100(session: Session, client: TestClient):
    """Verify single VRF creation returns 207 with success status."""
    _create_fabric(session)
    body = {"vrfs": [{"vrfName": "MyVRF_50000", "vrfId": 50000, "vlanId": 2000}]}
    response = client.post("/api/v1/manage/fabrics/f1/vrfs", json=body)
    data = response.json()

    assert response.status_code == 207
    assert len(data["results"]) == 1
    assert data["results"][0]["status"] == "success"
    assert data["results"][0]["vrfName"] == "MyVRF_50000"
    assert data["results"][0]["vrfId"] == 50000


def test_v1_vrf_post_110(session: Session, client: TestClient):
    """Verify multiple VRFs in one request returns 207 with all success."""
    _create_fabric(session)
    body = {
        "vrfs": [
            {"vrfName": "VRF_A", "vrfId": 50001},
            {"vrfName": "VRF_B", "vrfId": 50002},
        ]
    }
    response = client.post("/api/v1/manage/fabrics/f1/vrfs", json=body)
    data = response.json()

    assert response.status_code == 207
    assert len(data["results"]) == 2
    assert all(r["status"] == "success" for r in data["results"])
    names = {r["vrfName"] for r in data["results"]}
    assert names == {"VRF_A", "VRF_B"}


def test_v1_vrf_post_200(session: Session, client: TestClient):
    """Verify duplicate VRF returns 207 with failed status."""
    _create_fabric(session)
    _create_vrf(session)

    body = {"vrfs": [{"vrfName": "MyVRF_50000", "vrfId": 50000}]}
    response = client.post("/api/v1/manage/fabrics/f1/vrfs", json=body)
    data = response.json()

    assert response.status_code == 207
    assert data["results"][0]["status"] == "failed"
    assert data["results"][0]["message"] == "VRF MyVRF_50000 already exists"


def test_v1_vrf_post_300(client: TestClient):
    """Verify VRF creation in nonexistent fabric returns 500."""
    body = {"vrfs": [{"vrfName": "MyVRF_50000", "vrfId": 50000}]}
    response = client.post("/api/v1/manage/fabrics/nonexistent/vrfs", json=body)
    data = response.json()

    assert response.status_code == 500
    assert data["detail"]["code"] == 500
    assert data["detail"]["message"] == "Invalid Fabric name: nonexistent"


# ---------------------------------------------------------------------------
# GET /fabrics/{fabricName}/vrfs
# ---------------------------------------------------------------------------


def test_v1_vrf_get_100(session: Session, client: TestClient):
    """Verify GET returns VRFs with meta counts."""
    _create_fabric(session)
    _create_vrf(session, vrf_name="VRF_A", vrf_id=50001)
    _create_vrf(session, vrf_name="VRF_B", vrf_id=50002)

    response = client.get("/api/v1/manage/fabrics/f1/vrfs")
    data = response.json()

    assert response.status_code == 200
    assert data["meta"]["counts"]["total"] == 2
    assert data["meta"]["counts"]["remaining"] == 0
    assert len(data["vrfs"]) == 2


def test_v1_vrf_get_110(session: Session, client: TestClient):
    """Verify pagination with max and offset."""
    _create_fabric(session)
    for i in range(5):
        _create_vrf(session, vrf_name=f"VRF_{i}", vrf_id=50000 + i)

    response = client.get("/api/v1/manage/fabrics/f1/vrfs?offset=0&max=2")
    data = response.json()

    assert response.status_code == 200
    assert len(data["vrfs"]) == 2
    assert data["meta"]["counts"]["total"] == 5
    assert data["meta"]["counts"]["remaining"] == 3


def test_v1_vrf_get_200(client: TestClient):
    """Verify GET from nonexistent fabric returns 404."""
    response = client.get("/api/v1/manage/fabrics/nonexistent/vrfs")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"]["message"] == "Fabric not found"
    assert data["detail"]["code"] == 404


def test_v1_vrf_get_210(session: Session, client: TestClient):
    """Verify empty VRF list returns 200 with total=0."""
    _create_fabric(session)

    response = client.get("/api/v1/manage/fabrics/f1/vrfs")
    data = response.json()

    assert response.status_code == 200
    assert data["vrfs"] == []
    assert data["meta"]["counts"]["total"] == 0
    assert data["meta"]["counts"]["remaining"] == 0


def test_v1_vrf_get_300(session: Session, client: TestClient):
    """Verify coreData round-trip through JSON blob."""
    _create_fabric(session)
    core_data = {"tag": "12345", "vrfVlanId": 2000, "rtBothAuto": True}
    extra = json.dumps({"coreData": core_data})
    _create_vrf(session, extra_data=extra)

    response = client.get("/api/v1/manage/fabrics/f1/vrfs")
    data = response.json()

    assert response.status_code == 200
    vrf = data["vrfs"][0]
    assert vrf["coreData"]["tag"] == "12345"
    assert vrf["coreData"]["vrfVlanId"] == 2000
    assert vrf["coreData"]["rtBothAuto"] is True


# ---------------------------------------------------------------------------
# DELETE /fabrics/{fabricName}/vrfs/{vrfName}
# ---------------------------------------------------------------------------


def test_v1_vrf_delete_100(session: Session, client: TestClient):
    """Verify delete unattached VRF returns 204."""
    _create_fabric(session)
    _create_vrf(session)

    response = client.delete("/api/v1/manage/fabrics/f1/vrfs/MyVRF_50000")
    assert response.status_code == 204

    # Verify VRF is gone
    response = client.get("/api/v1/manage/fabrics/f1/vrfs")
    data = response.json()
    assert data["meta"]["counts"]["total"] == 0


def test_v1_vrf_delete_200(session: Session, client: TestClient):
    """Verify delete nonexistent VRF returns 400 (not 404!)."""
    _create_fabric(session)
    response = client.delete("/api/v1/manage/fabrics/f1/vrfs/NONEXISTENT")
    data = response.json()

    assert response.status_code == 400
    assert data["detail"]["code"] == 400
    assert data["detail"]["message"] == "Invalid VRF"
    assert data["detail"]["errors"] is None


def test_v1_vrf_delete_300(session: Session, client: TestClient):
    """Verify delete VRF with 'attached' attachment returns 400."""
    _create_fabric(session)
    _create_switch(session)
    _create_vrf(session)
    _create_vrf_attachment(session, status="attached", attach=True)

    response = client.delete("/api/v1/manage/fabrics/f1/vrfs/MyVRF_50000")
    data = response.json()

    assert response.status_code == 400
    assert data["detail"]["message"] == "Delete is not allowed as the VRF is currently not in 'NA' state"


def test_v1_vrf_delete_310(session: Session, client: TestClient):
    """Verify delete VRF with 'pending' attachment returns 400."""
    _create_fabric(session)
    _create_switch(session)
    _create_vrf(session)
    _create_vrf_attachment(session, status="pending", attach=False)

    response = client.delete("/api/v1/manage/fabrics/f1/vrfs/MyVRF_50000")
    data = response.json()

    assert response.status_code == 400
    assert data["detail"]["message"] == "Delete is not allowed as the VRF is currently not in 'NA' state"


def test_v1_vrf_delete_320(session: Session, client: TestClient):
    """Verify delete VRF with 'notApplicable' attachment returns 204."""
    _create_fabric(session)
    _create_switch(session)
    _create_vrf(session)
    _create_vrf_attachment(session, status="notApplicable", attach=False)

    response = client.delete("/api/v1/manage/fabrics/f1/vrfs/MyVRF_50000")
    assert response.status_code == 204


# ---------------------------------------------------------------------------
# POST /fabrics/{fabricName}/vrfAttachments/query
# ---------------------------------------------------------------------------


def test_v1_vrf_attachment_query_100(session: Session, client: TestClient):
    """Verify query returns cross-product with correct fields."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", hostname="leaf1", role="leaf")
    _create_switch(session, switch_id="SAL2222", hostname="spine1", role="spine")
    _create_vrf(session, vrf_name="VRF_A")
    _create_vrf(session, vrf_name="VRF_B")

    body = {"switchIds": ["SAL1111", "SAL2222"], "vrfNames": ["VRF_A", "VRF_B"]}
    response = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    data = response.json()

    assert response.status_code == 200
    assert data["meta"]["counts"]["total"] == 4
    assert data["meta"]["counts"]["remaining"] == 0
    assert len(data["attachments"]) == 4

    # Verify all expected fields are present
    for att in data["attachments"]:
        assert "attach" in att
        assert "errorMessage" in att
        assert "instanceValues" in att
        assert "showVlan" in att
        assert "status" in att
        assert "switchId" in att
        assert "switchName" in att
        assert "switchRole" in att
        assert "vrfName" in att


def test_v1_vrf_attachment_query_110(session: Session, client: TestClient):
    """Verify existing attached record is reflected in response."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", hostname="leaf1", role="leaf")
    _create_vrf(session, vrf_name="VRF_A")
    _create_vrf_attachment(session, vrf_name="VRF_A", switch_id="SAL1111", status="attached", attach=True)

    body = {"switchIds": ["SAL1111"], "vrfNames": ["VRF_A"]}
    response = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    data = response.json()

    assert response.status_code == 200
    assert len(data["attachments"]) == 1
    att = data["attachments"][0]
    assert att["status"] == "attached"
    assert att["attach"] is True
    assert att["switchId"] == "SAL1111"
    assert att["switchName"] == "leaf1"
    assert att["switchRole"] == "leaf"
    assert att["vrfName"] == "VRF_A"


def test_v1_vrf_attachment_query_200(client: TestClient):
    """Verify query from nonexistent fabric returns 404."""
    body = {"switchIds": [], "vrfNames": []}
    response = client.post("/api/v1/manage/fabrics/nonexistent/vrfAttachments/query", json=body)
    data = response.json()

    assert response.status_code == 404
    assert data["detail"]["message"] == "Fabric not found"
    assert data["detail"]["code"] == 404


def test_v1_vrf_attachment_query_210(session: Session, client: TestClient):
    """Verify default status is notApplicable when no attachment record exists."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", hostname="leaf1", role="leaf")
    _create_vrf(session, vrf_name="VRF_A")

    body = {"switchIds": ["SAL1111"], "vrfNames": ["VRF_A"]}
    response = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    data = response.json()

    assert response.status_code == 200
    assert len(data["attachments"]) == 1
    assert data["attachments"][0]["status"] == "notApplicable"
    assert data["attachments"][0]["attach"] is False


# ---------------------------------------------------------------------------
# POST /fabrics/{fabricName}/vrfActions/deploy
# ---------------------------------------------------------------------------


def test_v1_vrf_deploy_100(session: Session, client: TestClient):
    """Verify deploy transitions attach=True pending attachment to 'attached'."""
    _create_fabric(session)
    _create_switch(session)
    _create_vrf(session)
    _create_vrf_attachment(session, status="pending", attach=True)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["MyVRF_50000"]})
    assert response.status_code == 202
    assert response.json()["status"] == "Deployment of VRF(s) has been initiated successfully"

    # Verify the attachment transitioned to "attached"
    body = {"switchIds": ["SAL1111"], "vrfNames": ["MyVRF_50000"]}
    query_response = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    att = query_response.json()["attachments"][0]
    assert att["status"] == "attached"
    assert att["attach"] is True


def test_v1_vrf_deploy_110(session: Session, client: TestClient):
    """Verify deploy transitions attach=False pending attachment to 'notApplicable'."""
    _create_fabric(session)
    _create_switch(session)
    _create_vrf(session)
    _create_vrf_attachment(session, status="pending", attach=False)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["MyVRF_50000"]})
    assert response.status_code == 202

    body = {"switchIds": ["SAL1111"], "vrfNames": ["MyVRF_50000"]}
    query_response = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    att = query_response.json()["attachments"][0]
    assert att["status"] == "notApplicable"
    assert att["attach"] is False


def test_v1_vrf_deploy_120(session: Session, client: TestClient):
    """Verify deploy handles multiple pending attachments with mixed attach flags."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", hostname="leaf1")
    _create_switch(session, switch_id="SAL2222", hostname="leaf2")
    _create_vrf(session, vrf_name="VRF_A", vrf_id=50001)
    _create_vrf(session, vrf_name="VRF_B", vrf_id=50002)
    _create_vrf_attachment(session, vrf_name="VRF_A", switch_id="SAL1111", status="pending", attach=True)
    _create_vrf_attachment(session, vrf_name="VRF_B", switch_id="SAL2222", status="pending", attach=False)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["VRF_A", "VRF_B"]})
    assert response.status_code == 202

    # Check VRF_A on SAL1111 -> attached
    body = {"switchIds": ["SAL1111"], "vrfNames": ["VRF_A"]}
    q = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    assert q.json()["attachments"][0]["status"] == "attached"

    # Check VRF_B on SAL2222 -> notApplicable
    body = {"switchIds": ["SAL2222"], "vrfNames": ["VRF_B"]}
    q = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    assert q.json()["attachments"][0]["status"] == "notApplicable"


def test_v1_vrf_deploy_130(session: Session, client: TestClient):
    """Verify deploy with vrfNames filter only transitions matching VRFs."""
    _create_fabric(session)
    _create_switch(session)
    _create_vrf(session, vrf_name="VRF_A", vrf_id=50001)
    _create_vrf(session, vrf_name="VRF_B", vrf_id=50002)
    _create_vrf_attachment(session, vrf_name="VRF_A", switch_id="SAL1111", status="pending", attach=True)
    _create_vrf_attachment(session, vrf_name="VRF_B", switch_id="SAL1111", status="pending", attach=True)

    # Deploy only VRF_A
    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["VRF_A"]})
    assert response.status_code == 202

    # VRF_A should be attached
    body = {"switchIds": ["SAL1111"], "vrfNames": ["VRF_A"]}
    q = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    assert q.json()["attachments"][0]["status"] == "attached"

    # VRF_B should still be pending
    body = {"switchIds": ["SAL1111"], "vrfNames": ["VRF_B"]}
    q = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    assert q.json()["attachments"][0]["status"] == "pending"


def test_v1_vrf_deploy_140(session: Session, client: TestClient):
    """Verify deploy with switchIds filter only transitions matching switches."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", hostname="leaf1")
    _create_switch(session, switch_id="SAL2222", hostname="leaf2")
    _create_vrf(session)
    _create_vrf_attachment(session, switch_id="SAL1111", status="pending", attach=True)
    _create_vrf_attachment(session, switch_id="SAL2222", status="pending", attach=True)

    # Deploy only SAL1111
    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": ["SAL1111"], "vrfNames": ["MyVRF_50000"]})
    assert response.status_code == 202

    # SAL1111 should be attached
    body = {"switchIds": ["SAL1111"], "vrfNames": ["MyVRF_50000"]}
    q = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    assert q.json()["attachments"][0]["status"] == "attached"

    # SAL2222 should still be pending
    body = {"switchIds": ["SAL2222"], "vrfNames": ["MyVRF_50000"]}
    q = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    assert q.json()["attachments"][0]["status"] == "pending"


def test_v1_vrf_deploy_200(client: TestClient):
    """Verify deploy returns 400 for nonexistent fabric (not 404, matches real ND)."""
    response = client.post("/api/v1/manage/fabrics/nonexistent/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["SomeVRF"]})
    data = response.json()

    assert response.status_code == 400
    assert data["detail"]["code"] == 400
    assert data["detail"]["message"] == "Invalid Fabric name: nonexistent"


def test_v1_vrf_deploy_210(session: Session, client: TestClient):
    """Verify deploy with empty vrfNames returns 400 (vrfNames is mandatory)."""
    _create_fabric(session)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": []})
    data = response.json()

    assert response.status_code == 400
    assert data["detail"]["message"] == "'vrfNames' is a mandatory parameter for this endpoint."


def test_v1_vrf_deploy_220(session: Session, client: TestClient):
    """Verify deploy with nonexistent VRF name returns 400."""
    _create_fabric(session)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["NONEXISTENT_VRF"]})
    data = response.json()

    assert response.status_code == 400
    assert data["detail"]["message"] == "Invalid VRF name(s): NONEXISTENT_VRF"


def test_v1_vrf_deploy_230(session: Session, client: TestClient):
    """Verify deploy with nonexistent switchId returns 400."""
    _create_fabric(session)
    _create_vrf(session)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": ["FAKE_SWITCH"], "vrfNames": ["MyVRF_50000"]})
    data = response.json()

    assert response.status_code == 400
    assert data["detail"]["message"] == "Invalid switch serial number(s) : [FAKE_SWITCH]"


def test_v1_vrf_deploy_300(session: Session, client: TestClient):
    """Verify deploy with no pending attachments returns success (no-op)."""
    _create_fabric(session)
    _create_vrf(session)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["MyVRF_50000"]})
    assert response.status_code == 202
    assert response.json()["status"] == "No switches pending for deployment."


def test_v1_vrf_deploy_310(session: Session, client: TestClient):
    """Verify deploy does not alter non-pending attachments."""
    _create_fabric(session)
    _create_switch(session)
    _create_vrf(session)
    _create_vrf_attachment(session, status="attached", attach=True)

    response = client.post("/api/v1/manage/fabrics/f1/vrfActions/deploy", json={"switchIds": [], "vrfNames": ["MyVRF_50000"]})
    assert response.status_code == 202

    body = {"switchIds": ["SAL1111"], "vrfNames": ["MyVRF_50000"]}
    q = client.post("/api/v1/manage/fabrics/f1/vrfAttachments/query", json=body)
    assert q.json()["attachments"][0]["status"] == "attached"
