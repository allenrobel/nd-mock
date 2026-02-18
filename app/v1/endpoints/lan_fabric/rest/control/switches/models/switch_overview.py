# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# call-arg for the above issue.
# union-attr to disable errors due to: inspect.currentframe().f_code.co_name.
# mypy: disable-error-code="call-arg,union-attr"
import json
from typing import Any, Dict, Optional, Sequence

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, select

from ........common.functions.utilities import switch_role_db_to_external, switch_role_external_to_db
from .......models.fabric import FabricDbModelV1


class SwitchConfigBase(SQLModel):
    """
    Base class for SwitchConfig, defining the data fields without the table.

    Attributes:
        in_sync (int): The number of switches that are in sync with the configuration.
        out_of_sync (int): The number of switches that are out of sync with the configuration.
    """

    in_sync: int = Field(default=0)
    out_of_sync: int = Field(default=0)


class SwitchConfigDbModel(SwitchConfigBase, table=True):
    """
    SQLModel table representing the configuration synchronization status of switches.
    """

    fabric: Optional[str] = Field(default=None, primary_key=True)


class SwitchHealthBase(SQLModel):
    """
    Base class for SwitchHealthDbModel, defining the data fields without the table.

    Attributes:
        Healthy (int): The number of switches with a healthy status.
        Major (int): The number of switches with a major health issue.
        Minor (int): The number of switches with a minor health issue.
    """

    Healthy: int
    Major: int
    Minor: int


class SwitchHealthDbModel(SwitchHealthBase, table=True):
    """
    SQLModel table representing the health status of switches.
    """

    fabric: Optional[str] = Field(default=None, primary_key=True)


class SwitchRolesBase(SQLModel):
    """
    Base class for SwitchRolesDbModel, defining the data fields without the table.

    Attributes:
        access (int): The number of switches with the access role.
        aggregation (int): The number of switches with the aggregation role.
        border (int): The number of switches with the border role.
        border_gateway (int): The number of switches with the border gateway role.
        border_gateway_spine (int): The number of switches with the border gateway spine role.
        border_gateway_super_spine (int): The number of switches with the border gateway super spine role.
        border_spine (int): The number of switches with the border spine role.
        border_super_spine (int): The number of switches with the border super spine role.
        core_router (int): The number of switches with the core router role.
        edge_router (int): The number of switches with the edge router role.
        leaf (int): The number of switches with the leaf role.
        spine (int): The number of switches with the spine role.
        super_spine (int): The number of switches with the super spine role.
        tor (int): The number of switches with the Top of Rack (TOR) role.
    """

    access: int = Field(default=0)
    aggregation: int = Field(default=0)
    border: int = Field(default=0)
    border_gateway: int = Field(default=0, alias="border gateway")
    border_gateway_spine: int = Field(default=0, alias="border gateway spine")
    border_gateway_super_spine: int = Field(default=0, alias="border gateway super spine")
    border_spine: int = Field(default=0, alias="border spine")
    border_super_spine: int = Field(default=0, alias="border super spine")
    core_router: int = Field(default=0, alias="core router")
    edge_router: int = Field(default=0, alias="edge router")
    leaf: int = Field(default=0)
    spine: int = Field(default=0)
    super_spine: int = Field(default=0, alias="super spine")
    tor: int = Field(default=0)

    class Config:
        """
        Model configuration.
        """

        by_alias = True


class SwitchRolesDbModel(SwitchRolesBase, table=True):
    """
    SQLModel table representing the roles of switches in the network.

    Attributes:
        id (Optional[int]): The primary key for the table.
        switch_overview_id (Optional[int]): Foreign key linking to the SwitchOverviewDbModel table.
    """

    fabric: Optional[str] = Field(default=None, primary_key=True)


class SwitchHwBase(SQLModel):
    """Base class for Switch Versions."""

    count: int


class SwitchHwDbModel(SwitchHwBase, table=True):
    """
    SQLModel table representing the hardware models of switches.
    Stores each HW model as a separate row.
    """

    fabric: Optional[str] = Field(default=None, primary_key=True)
    model: Optional[str] = Field(default=None, primary_key=True)


class SwitchSwBase(SQLModel):
    """Base class for Switch Versions."""

    count: int


class SwitchSWVersionsDbModel(SwitchSwBase, table=True):
    """
    SQLModel table representing the software versions of switches.
    Stores each SW version as a separate row.
    """

    fabric: Optional[str] = Field(default=None, primary_key=True)
    version_name: Optional[str] = Field(default=None, primary_key=True)


class SwitchOverviewResponseModel(BaseModel):
    """
    Represents the overall switch overview data.

    Attributes:
        switchConfig (SwitchConfigBase): Configuration synchronization status of the switches.
        switchHealth (SwitchHealthBase): Health status of the switches.
        switchHWVersions (Dict[str, int]): Hardware versions of the switches.
        switchRoles (Dict): Roles of the switches in the network.
        switchSWVersions (Dict[str, int]): Software versions of the switches.
    """

    switchConfig: SwitchConfigBase
    switchHealth: SwitchHealthBase
    switchHWVersions: Dict[str, int]
    switchRoles: SwitchRolesBase
    switchSWVersions: Dict[str, int]


class SwitchOverviewHealth:
    """
    # Summary

    Manage the health status of switches in the fabric.

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.health.
    - delete: Delete the record/row matching self.fabric.
    - remove: Decrement the count of the record attribute matching self.fabric and self.health.
    - response_json: Return the current switch health data for self.fabric as JSON.
    - response_model: Return the current switch health data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - health: The health status of the switch.  One of Healthy, Major, Minor.
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        health = SwitchOverviewHealth()
        health.session = session
        health.fabric = "fabric1"
        health.initialize_db_table()
        health.health = "Healthy"
        health.add()
        print(f"response: {health.response_json()}")
    ```
    """

    def __init__(self):
        self._fabric = None
        self._health = None
        self._session = None
        self._model_init = SwitchHealthDbModel(Healthy=0, Major=0, Minor=0)
        self.attributes = {"Healthy", "Major", "Minor"}

    def initialize_db_table(self):
        """
        # Summary

        Initialize the database table associated with this class.
        """
        commit = False
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()
        if record is None:
            self._model_init.fabric = self.fabric
            record = SwitchHealthDbModel(**self._model_init.model_dump())
            self.session.add(record)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self):
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self):
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.health.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if self.health == attribute:
                setattr(record, attribute, getattr(record, attribute) + 1)
                self.session.add(record)
                self.session.commit()
                break

    def delete(self):
        """
        # Summary

        - Delete the record matching self.fabric from the table.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        if record is not None:
            self.session.delete(record)
            self.session.commit()

    def remove(self):
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.health.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if self.health == attribute and getattr(record, attribute) > 0:
                setattr(record, attribute, getattr(record, attribute) - 1)
                self.session.add(record)
                self.session.commit()
                break

    def response_dict(self) -> dict[str, Any]:
        """
        Returns the current switch health data for self.fabric as a dictionary.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return model.model_dump(exclude={"fabric"})

    def response_json(self) -> str:
        """
        Returns the current switch health data for self.fabric as JSON.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return model.model_dump_json(exclude={"fabric"})

    def response_model(self) -> SwitchHealthDbModel:
        """
        Returns the current switch health data for self.fabric as a model.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return model

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def health(self) -> str:
        """
        Get the health status of the switch.

        Valid values: "Healthy", "Major", "Minor"
        """
        return self._health

    @health.setter
    def health(self, value: str):
        self._health = value

    @property
    def session(self) -> Session:
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


class SwitchOverviewRoles:
    """
    # Summary

    Manage the roles of switches in the fabric.

    Roles are stored in the database with underscores in place of spaces.
    For example, "border gateway spine" is stored as "border_gateway_spine".

    The following endpoints want roles to be specified with spaces.
    For example, "border gateway spine".

    POST /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/roles

    Example POST request body

    ```json
    [
        {
            "role": "border gateway",
            "serialNumber": "FOX6127BJZS"
        }
    ]
    ```

    The response for the following endpoint shows roles in two formats:

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{{fabric_name}}/inventory/switchesByFabric

    1. switchRoleEnum: "BorderGatewaySpine"
    2. switchRole: "border gateway spine"

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.role.
    - delete: Delete from the table the record/row matching self.fabric.
    - remove: Decrement the count of the record attribute matching self.fabric and self.role.
    - response_json: Return the current switch role data for self.fabric as JSON.
    - response_model: Return the current switch role data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - role: The role of the switch.  One of access, aggregation, border, "border gateway",
    "border gateway spine", "border gateway super spine", "border spine", "border super spine",
    "core router", "edge router", leaf, spine, "super spine", tor
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        roles = SwitchOverviewRoles()
        roles.session = session
        roles.fabric = "fabric1"
        roles.initialize_db_table()
        roles.role = "border gateway"
        roles.add()
        print(f"response: {roles.response_json()}")
    ```
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self._role = None
        self._fabric = None
        self._session = None
        self._model_init = SwitchRolesDbModel(
            access=0,
            aggregation=0,
            border=0,
            border_gateway=0,
            border_gateway_spine=0,
            border_gateway_super_spine=0,
            border_spine=0,
            border_super_spine=0,
            core_router=0,
            edge_router=0,
            leaf=0,
            spine=0,
            super_spine=0,
            tor=0,
        )
        self.attributes = {
            "access",
            "aggregation",
            "border",
            "border gateway",
            "border gateway spine",
            "border gateway super spine",
            "border spine",
            "border super spine",
            "core router",
            "edge router",
            "leaf",
            "spine",
            "super spine",
            "tor",
        }

    def initialize_db_table(self):
        """
        Initializes the switch roles database table.
        """
        commit = False
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()
        if record is None:
            self._model_init.fabric = self.fabric
            record = SwitchRolesDbModel(**self._model_init.model_dump())
            self.session.add(record)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self):
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self):
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.role.
        - Add the updated record to the session.
        - Commit the session.

        ## Notes

        - self.role should be in external format. e.g. "border gateway spine"
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if attribute == self.role:
                db_attribute = switch_role_external_to_db(attribute)
                setattr(record, db_attribute, getattr(record, db_attribute) + 1)
                self.session.add(record)
                break
        self.session.commit()

    def delete(self):
        """
        # Summary

        - Delete the record matching self.fabric from the table.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        if record is not None:
            self.session.delete(record)
            self.session.commit()

    def remove(self):
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.role.
        - Add the updated record to the session.
        - Commit the session.

        ## Notes

        - self.role should be in external format. e.g. "border gateway spine"
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            db_attribute = switch_role_external_to_db(attribute)
            if self.role == attribute and getattr(record, db_attribute) > 0:
                setattr(record, db_attribute, getattr(record, db_attribute) - 1)
                self.session.add(record)
                break
        self.session.commit()

    def export(self, model):
        """
        Convert the database model to a model with keys expected by
        the outside world. e.g. border_gateway_spine -> border gateway spine
        """
        model_dict = model.model_dump()

        exported = {}
        for key, value in model_dict.items():
            if key == "fabric":
                continue
            new_key = switch_role_db_to_external(key)
            if new_key is None:
                raise ValueError(f"Invalid role: {key}")
            exported[new_key] = value
        return exported

    def response_json(self) -> str:
        """
        Returns the current switch health data as JSON.

        The JSON is returned with alias names, not database field names.

        For example "border gateway spine" instead of "border_gateway_spine".
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return json.dumps(self.export(model))

    def response_dict(self) -> dict:
        """
        # Summary

        Returns the current switch roles data as a dictionary.

        The dictionary is returned with alias names, not database field names.

        For example "border gateway spine" instead of "border_gateway_spine".

        NOTES
        """
        self.validate_properties()
        statement = select(SwitchRolesDbModel).where(SwitchRolesDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return self.export(model)

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def role(self) -> str:
        """
        Get the role of the switch.

        Valid values: "access", "aggregation", "border", "border gateway",
        "border gateway spine", "border gateway super spine", "border spine",
        "border super spine", "core_router", "edge router", "leaf", "spine",
        "super spine", "tor"
        """
        return self._role

    @role.setter
    def role(self, value: str):
        if value not in self.attributes:
            raise ValueError(f"Invalid role: {value}")
        self._role = value

    @property
    def session(self) -> Session:
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


class SwitchOverviewSw:
    """
    # Summary

    Manage the software of switches in the fabric.

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.version.
    - delete: Delete from the table the record/row matching self.fabric.
    - remove: Decrement the count of the record attribute matching self.fabric and self.version.
    - response_json: Return the current switch software version data for self.fabric as JSON.
    - response_model: Return the current switch software version data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - version: The software version of the switch.
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        sw = SwitchOverviewSw()
        sw.session = session
        sw.fabric = "fabric1"
        sw.initialize_db_table()
        sw.version = "10.2(5)"
        sw.add()
        print(f"response: {sw.response_json()}")
    ```
    """

    def __init__(self):
        self._fabric = None
        self._version = None
        self._session = None
        self._model_init = SwitchSWVersionsDbModel(version_name="ignore", count=0)

    def initialize_db_table(self) -> None:
        """
        Initializes the switch software versions database table.
        """
        commit = False
        statement = select(SwitchSWVersionsDbModel).where(SwitchSWVersionsDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if len(records) == 0:
            record = SwitchSWVersionsDbModel(**self._model_init.model_dump())
            record.fabric = self.fabric
            self.session.add(record)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self) -> None:
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self) -> None:
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.version.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchSWVersionsDbModel).where(SwitchSWVersionsDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()

        if records is None:
            return

        if self.version not in [record.version_name for record in records]:
            record = SwitchSWVersionsDbModel(fabric=self.fabric, version_name=self.version, count=1)
            self.session.add(record)
        else:
            for record in records:
                if record.version_name == self.version:
                    record.count += 1
                    self.session.add(record)
                    self.session.commit()
                    break

    def delete(self) -> None:
        """
        # Summary

        - Delete the record matching self.fabric from the table.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        if record is not None:
            self.session.delete(record)
            self.session.commit()

    def remove(self) -> None:
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.version.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchSWVersionsDbModel).where(SwitchSWVersionsDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()

        if self.version not in [record.version_name for record in records]:
            return
        commit = False
        for record in records:
            if record.version_name == self.version and record.count > 0:
                record.count -= 1
                if record.count == 0:
                    commit = True
                    self.session.delete(record)
                else:
                    commit = True
                    self.session.add(record)
        if commit is True:
            self.session.commit()

    def response_dict(self) -> dict:
        """
        Returns the current switch software version data for self.fabric as a dictionary.
        """
        self.validate_properties()
        statement = select(SwitchSWVersionsDbModel).where(SwitchSWVersionsDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if records is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        response = {}
        for record in records:
            if record.version_name != "ignore":
                response[record.version_name] = record.count
        return response

    def response_json(self) -> str:
        """
        Returns the current switch software version data for self.fabric as JSON.
        """
        self.validate_properties()
        statement = select(SwitchSWVersionsDbModel).where(SwitchSWVersionsDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if records is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        response = {}
        for record in records:
            if record.version_name != "ignore":
                response[record.version_name] = record.count
        return json.dumps(response)

    def response_model(self) -> Sequence[SwitchSWVersionsDbModel] | None:
        """
        Returns the current switch software version data for self.fabric as a model.
        """
        self.validate_properties()
        statement = select(SwitchSWVersionsDbModel).where(SwitchSWVersionsDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if records is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return records

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def version(self) -> str:
        """
        The software version of the switch.
        """
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value

    @property
    def session(self) -> Session:
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


class SwitchOverviewHw:
    """
    # Summary

    Manage the hardware of switches in the fabric.

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.version.
    - delete: Delete from the table the record/row matching self.fabric.
    - remove: Decrement the count of the record attribute matching self.fabric and self.version.
    - response_json: Return the current switch hardware version data for self.fabric as JSON.
    - response_model: Return the current switch hardware version data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - version: The hardware version of the switch.
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        hw = SwitchOverviewHw()
        hw.session = session
        hw.fabric = "fabric1"
        hw.initialize_db_table()
        hw.model = "N9K-C93180YC-EX"
        hw.add()
        print(f"response: {hw.response_json()}")
    ```
    """

    def __init__(self):
        self._fabric = None
        self._version = None
        self._session = None
        self._model_init = SwitchHwDbModel(model="ignore", count=0)

    def initialize_db_table(self) -> None:
        """
        Initializes the switch hardware versions database table.
        """
        commit = False
        statement = select(SwitchHwDbModel).where(SwitchHwDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if len(records) == 0:
            record = SwitchHwDbModel(**self._model_init.model_dump())
            record.fabric = self.fabric
            self.session.add(record)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self) -> None:
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self) -> None:
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.model.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHwDbModel).where(SwitchHwDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()

        if records is None:
            return

        if self.model not in [record.model for record in records]:
            record = SwitchHwDbModel(fabric=self.fabric, model=self.model, count=1)
            self.session.add(record)
        else:
            for record in records:
                if record.model == self.model:
                    record.count += 1
                    self.session.add(record)
                    self.session.commit()
                    break

    def delete(self) -> None:
        """
        # Summary

        - Delete the record matching self.fabric from the table.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        if record is not None:
            self.session.delete(record)
            self.session.commit()

    def remove(self) -> None:
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.model.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHwDbModel).where(SwitchHwDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()

        if self.model not in [record.model for record in records]:
            return

        commit = False
        for record in records:
            if record.model == self.model and record.count > 0:
                record.count -= 1
                commit = True
                if record.count == 0:
                    self.session.delete(record)
                else:
                    self.session.add(record)
        if commit is True:
            self.session.commit()

    def response_dict(self) -> dict:
        """
        Returns the current switch hardware model data for self.fabric as a dictionary.
        """
        self.validate_properties()
        statement = select(SwitchHwDbModel).where(SwitchHwDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if records is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        response = {}
        for record in records:
            if record.model != "ignore":
                response[record.model] = record.count
        return response

    def response_json(self) -> str:
        """
        Returns the current switch hardware model data for self.fabric as JSON.
        """
        self.validate_properties()
        statement = select(SwitchHwDbModel).where(SwitchHwDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if records is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        response = {}
        for record in records:
            if record.model != "ignore":
                response[record.model] = record.count
        return json.dumps(response)

    def response_model(self) -> Sequence[SwitchHwDbModel]:
        """
        Returns the current switch hardware model data for self.fabric as a model.
        """
        self.validate_properties()
        statement = select(SwitchHwDbModel).where(SwitchHwDbModel.fabric == self.fabric)
        records = self.session.exec(statement).all()
        if records is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return records

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def model(self) -> str:
        """
        The hardware model of the switch.
        """
        return self._model

    @model.setter
    def model(self, value: str):
        self._model = value

    @property
    def session(self) -> Session:
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


class SwitchOverviewSync:
    """
    # Summary

    Manage the configuration synchronization status of switches in the fabric.

    ## Methods

    - add: Increment the count of the record attribute matching self.fabric and self.sync.
    - delete: Delete from the table the record/row matching self.fabric.
    - remove: Decrement the count of the record attribute matching self.fabric and self.sync.
    - response_json: Return the current switch configuration synchronization data for self.fabric as JSON.
    - response_model: Return the current switch configuration synchronization data for self.fabric as a model.
    - initialize_db_table: Initialize the database record for self.fabric.

    ## Properties

    - fabric: The fabric name.
    - sync: The synchronization status of the switch.  One of in_sync, out_of_sync.
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        sync = SwitchOverviewSync()
        sync.session = session
        sync.fabric = "fabric1"
        sync.initialize_db_table()
        sync.sync = "in_sync"
        sync.add()
        print(f"response: {sync.response_json()}")
    ```
    """

    def __init__(self):
        self._fabric = None
        self._sync = None
        self._session = None
        self._model_init = SwitchConfigDbModel(in_sync=0, out_of_sync=0)
        self.attributes = {"in_sync", "out_of_sync"}

    def initialize_db_table(self) -> None:
        """
        Initializes the switch configuration synchronization database table.
        """
        commit = False
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()
        if record is None:
            self._model_init.fabric = self.fabric
            record = SwitchConfigDbModel(**self._model_init.model_dump())
            self.session.add(record)
            commit = True

        # Persist the database table
        if commit:
            self.session.commit()

    def validate_properties(self) -> None:
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    def add(self) -> None:
        """
        # Summary

        - Increment by 1 the count of the record attribute matching self.sync.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if attribute == self.sync:
                setattr(record, attribute, getattr(record, attribute) + 1)
                self.session.add(record)
                self.session.commit()
                break

    def delete(self) -> None:
        """
        # Summary

        - Delete the record matching self.fabric from the table.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchHealthDbModel).where(SwitchHealthDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        if record is not None:
            self.session.delete(record)
            self.session.commit()

    def remove(self) -> None:
        """
        # Summary

        - Decrement by 1 the count of the record attribute matching self.sync.
        - Add the updated record to the session.
        - Commit the session.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        record = self.session.exec(statement).first()

        for attribute in self.attributes:
            if self.sync == attribute and getattr(record, attribute) > 0:
                setattr(record, attribute, getattr(record, attribute) - 1)
                self.session.add(record)
                self.session.commit()
                break

    def response_dict(self) -> dict[str, Any]:
        """
        Returns the current switch sync status data as a dictionary.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return model.model_dump(exclude={"fabric"})

    def response_json(self) -> str:
        """
        Returns the current switch sync status data as JSON.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return model.model_dump_json(exclude={"fabric"})

    def response_model(self) -> SwitchConfigDbModel:
        """
        Returns the current switch sync status data as a model.
        """
        self.validate_properties()
        statement = select(SwitchConfigDbModel).where(SwitchConfigDbModel.fabric == self.fabric)
        model = self.session.exec(statement).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")
        return model

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def sync(self) -> bool:
        """
        Get the sync status of the switch.

        Valid values: in_sync, out_of_sync
        """
        return self._sync

    @sync.setter
    def sync(self, value: bool):
        if value not in self.attributes:
            msg = f"Invalid sync status: {value}. "
            msg += f"Expected one of {','.join(self.attributes)}."
            raise ValueError(msg)
        self._sync = value

    @property
    def session(self) -> Session:
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        self._session = value


class SwitchOverview:
    """
    # Summary

    Utilities for managing switch overview aggregate data.
    """

    def __init__(self):
        self._fabric = None
        self._session = None

    def initialize_db_table(self):
        """
        Initialize the database tables for the switch overview data.
        """
        self.validate_properties()
        sync = SwitchOverviewSync()
        sync.session = self.session
        sync.fabric = self.fabric
        sync.initialize_db_table()

        health = SwitchOverviewHealth()
        health.session = self.session
        health.fabric = self.fabric
        health.initialize_db_table()

        hw = SwitchOverviewHw()
        hw.session = self.session
        hw.fabric = self.fabric
        hw.initialize_db_table()

        roles = SwitchOverviewRoles()
        roles.session = self.session
        roles.fabric = self.fabric
        roles.initialize_db_table()

        sw = SwitchOverviewSw()
        sw.session = self.session
        sw.fabric = self.fabric
        sw.initialize_db_table()

    def delete(self):
        """
        Delete the database tables for the switch overview data.
        """
        self.validate_properties()

        # pylint: disable=no-member
        db_fabric = self.session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == self.fabric)).first()
        # pylint: enable=no-member
        if not db_fabric:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")

        sync = SwitchOverviewSync()
        sync.session = self.session
        sync.fabric = self.fabric
        sync.delete()

        health = SwitchOverviewHealth()
        health.session = self.session
        health.fabric = self.fabric
        health.delete()

        hw = SwitchOverviewHw()
        hw.session = self.session
        hw.fabric = self.fabric
        hw.delete()

        roles = SwitchOverviewRoles()
        roles.session = self.session
        roles.fabric = self.fabric
        roles.delete()

        sw = SwitchOverviewSw()
        sw.session = self.session
        sw.fabric = self.fabric
        sw.delete()

    def validate_properties(self):
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def session(self) -> Session:
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value: Session):
        self._session = value


class SwitchOverviewResponse:
    """
    # Summary

    Generate a response containing switch overview data for self.fabric
    combining the data from the SwitchOverviewSync, SwitchOverviewHealth,
    SwitchOverviewHw, SwitchOverviewRoles, and SwitchOverviewSw classes.

    ## Methods
    - refresh: Retrieve the switch overview data for self.fabric from the database.
    - response_json: Return the current switch overview data for self.fabric as JSON.
    - response_dict: Return the current switch overview data for self.fabric as a dictionary.

    ## Properties

    - fabric: The fabric name.
    - session: A database session object.

    ## Example Usage

    ```python
    from sqlmodel import Session, create_engine

    DATABASE_URL = "sqlite:///./nexus_dashboard.db"
    engine = create_engine(DATABASE_URL, echo=False)

    with Session(engine) as session:
        response = SwitchOverviewResponse()
        response.session = session
        response.fabric = "fabric1"
        response.refresh()
        print(f"response: {response.response_json()}")
        response_dict = response.response_dict()
        print("Model access")
        print(f"  fabric: {response_dict.get('switchConfig', {}).get('fabric')}")
        print("   Sync status:")
        print(f"      in_sync: {response_dict.get('switchConfig', {}).get('in_sync')}")
        print(f"      out_of_sync: {response_dict.get('switchConfig', {}).get('out_of_sync')}")
        print("   Health status:")
        print(f"      Healthy: {response_dict.get('switchHealth', {}).get('Healthy')}")
        print(f"      Major: {response_dict.get('switchHealth', {}).get('Major')}")
        print(f"      Minor: {response_dict.get('switchHealth', {}).get('Minor')")
        print(f"  HW Versions: {response_dict.get('switchHWVersions')}")
        print(f"  Roles:")
        print(f"     access: {response_dict.get('switchRoles', {}).get("access")}")
        print(f"     aggregation: {response_dict.get('switchRoles', {}).get("aggregation")}")
        print(f"  SW Versions: {response_dict.get('switchSWVersions')}")
        print()
    ```

    ## Notes

    - The response_dict method returns a dictionary because switchRoles is a dictionary,
      not a model.  switchRoles is a dictionary because the keys used by NDFC have spaces
      in them (e.g. "border gateway spine"), which are not valid Python attribute names.
      Looked into using Field(alias=...), but that didn't work (based on some internet
      sleuthing).
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self._fabric = None
        self._session = None
        self._refreshed = False

        self.sync = None
        self.health = None
        self.hw = None
        self.roles = None
        self.sw = None
        self.hw_record = None
        self.sw_record = None

    def refresh(self) -> None:
        """
        Retrieve the switch overview data for self.fabric from the database.
        """
        self.validate_properties()
        # pylint: disable=no-member
        db_fabric = self.session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == self.fabric)).first()
        # pylint: enable=no-member
        if not db_fabric:
            raise HTTPException(status_code=404, detail=f"Fabric {self.fabric} not found")

        self.sync = SwitchOverviewSync()
        self.sync.session = self.session
        self.sync.fabric = self.fabric

        self.health = SwitchOverviewHealth()
        self.health.session = self.session
        self.health.fabric = self.fabric

        self.hw = SwitchOverviewHw()
        self.hw.session = self.session
        self.hw.fabric = self.fabric

        self.roles = SwitchOverviewRoles()
        self.roles.session = self.session
        self.roles.fabric = self.fabric

        self.sw = SwitchOverviewSw()
        self.sw.session = self.session
        self.sw.fabric = self.fabric

        self._refreshed = True

    def build_hw_response(self) -> Dict[str, int]:
        """
        Build the contents of the switchHWVersions attribute.
        """
        if not self._refreshed:
            raise ValueError("Data not refreshed. Call refresh() first.")

        switch_hw_response = {}
        for self.hw_record in self.hw.response_model():
            if self.hw_record.model == "ignore":
                continue
            switch_hw_response[self.hw_record.model] = self.hw_record.count
        return switch_hw_response

    def build_sw_response(self) -> Dict[str, int]:
        """
        Build the contents of the switchSWVersions attribute
        """
        if not self._refreshed:
            raise ValueError("Data not refreshed. Call refresh() first.")

        switch_sw_response = {}
        for self.sw_record in self.sw.response_model():
            if self.sw_record.version_name == "ignore":
                continue
            switch_sw_response[self.sw_record.version_name] = self.sw_record.count
        return switch_sw_response

    def response_dict(self) -> dict:
        """
        Returns the current switch overview data for self.fabric as a dictionary.

        NOTES:

        -   We cannot return a SwitchOverviewResponseModel object because switchRoles
            is a dictionary, not a model.  switchRoles is a dictionary because the
            keys used by NDFC have spaces in them (e.g. "border gateway spine"), which
            are not valid Python attribute names.  Looked into using Field(alias=...),
            but that didn't work (based on some internet sleuthing).
        """
        if not self._refreshed:
            raise ValueError("Data not refreshed. Call refresh() first.")

        response = {}
        response["switchConfig"] = self.sync.response_dict()
        response["switchHealth"] = self.health.response_dict()
        response["switchHWVersions"] = self.hw.response_dict()
        response["switchRoles"] = self.roles.response_dict()
        response["switchSWVersions"] = self.sw.response_dict()
        return response

    def response_json(self) -> str:
        """
        Returns the current switch overview data for self.fabric as JSON.
        """
        return json.dumps(self.response_dict())

    def validate_properties(self) -> None:
        """
        Validate the properties of the class.
        """
        if self._fabric is None:
            raise ValueError("Fabric name not set.")
        if self._session is None:
            raise ValueError("Session not set")

    @property
    def fabric(self) -> str:
        """
        The fabric name.
        """
        return self._fabric

    @fabric.setter
    def fabric(self, value: str):
        self._fabric = value

    @property
    def session(self) -> Session:
        """
        Get the session object.
        """
        return self._session

    @session.setter
    def session(self, value: Session):
        self._session = value
