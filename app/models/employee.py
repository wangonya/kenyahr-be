from enum import Enum
from typing import Optional

from app.models import BaseModel, PydanticBaseModel


class EmployeeEmploymentStatus(Enum):
    active = "active"
    terminated = "terminated"


class EmployeeCreate(PydanticBaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]

    id_number: str
    kra_pin: str
    nhif_number: str
    nssf_number: str
    tax_exemption_number: Optional[str]

    is_resident: bool = True
    is_director: bool = False
    is_tax_exempt: bool = False
    has_disability: bool = False

    employment_status: EmployeeEmploymentStatus

    class Config:
        use_enum_values = True


class EmployeeFilter(PydanticBaseModel):
    is_resident: Optional[bool]
    is_director: Optional[bool]
    is_tax_exempt: Optional[bool]
    has_disability: Optional[bool]

    employment_status: Optional[EmployeeEmploymentStatus]

    class Config:
        use_enum_values = True


class EmployeeUpdate(EmployeeFilter):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]

    id_number: Optional[str]
    kra_pin: Optional[str]
    nhif_number: Optional[str]
    nssf_number: Optional[str]
    tax_exemption_number: Optional[str]


class EmployeeInDB(EmployeeCreate, BaseModel):
    pass
