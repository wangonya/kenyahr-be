from typing import List, Optional

from fastapi import APIRouter, Depends

from app.core.repository import MongoDBRepository
from app.models.employee import (
    EmployeeCreate,
    EmployeeFilter,
    EmployeeInDB,
    EmployeeUpdate,
)
from app.services.employee import EmployeeService
from app.services.user import UserService

router = APIRouter(prefix="/employees", tags=["Employees"])
repo = MongoDBRepository("employees")


@router.post("/create-employee", response_model=EmployeeInDB)
def create_employee(
    new_employee: EmployeeCreate,
    _=Depends(UserService(MongoDBRepository("users")).get_current_user),
):
    return EmployeeService(repo=repo).create_employee(new_employee)


@router.get("/get-all-employees", response_model=List[Optional[EmployeeInDB]])
def get_all_employees(
    _=Depends(UserService(MongoDBRepository("users")).get_current_user),
):
    return EmployeeService(repo=repo).get_all_employees()


@router.get("/get-employee-by-id", response_model=Optional[EmployeeInDB])
def get_employee_by_id(
    employee_id: str,
    _=Depends(UserService(MongoDBRepository("users")).get_current_user),
):
    return EmployeeService(repo=repo).get_employee_by_id(employee_id)


@router.get("/get-employees-by-filters", response_model=List[Optional[EmployeeInDB]])
def get_employee_by_filters(
    filter_parameters: EmployeeFilter = Depends(),
    _=Depends(UserService(MongoDBRepository("users")).get_current_user),
):
    return EmployeeService(repo=repo).get_employees_by_filters(filter_parameters)


@router.patch("/update-employee", response_model=EmployeeInDB)
def update_employee_details(
    employee_id: str,
    employee_details: EmployeeUpdate,
    _=Depends(UserService(MongoDBRepository("users")).get_current_user),
):
    return EmployeeService(repo=repo).update_employee_details(
        employee_id, employee_details
    )


@router.delete("/delete-employee", response_model=None)
def delete_employee(
    employee_id: str,
    _=Depends(UserService(MongoDBRepository("users")).get_current_user),
):
    return EmployeeService(repo=repo).delete_employee(employee_id)
