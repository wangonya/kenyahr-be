from bson.objectid import ObjectId
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.core.repository import AbstractRepository
from app.models.employee import EmployeeCreate, EmployeeFilter, EmployeeUpdate


class EmployeeService:
    def __init__(self, repo: AbstractRepository) -> None:
        self.repo = repo

    def create_employee(self, employee: EmployeeCreate):
        try:
            return self.repo.add(employee.dict())
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An employee with the provided details already exists.",
            )

    def get_all_employees(self):
        employees = self.repo.list()
        return [employee for employee in employees]

    def get_employee_by_id(self, id: str):
        return self.repo.get(_id=ObjectId(id))

    def get_employees_by_filters(self, filter_parameters: EmployeeFilter):
        employees = self.repo.filter(
            filter_parameters=filter_parameters.dict(exclude_none=True)
        )
        return [employee for employee in employees]

    def update_employee_details(
        self,
        employee_id: str,
        employee_details: EmployeeUpdate,
    ):
        return self.repo.update(
            ObjectId(employee_id),
            employee_details.dict(exclude_none=True),
        )

    def delete_employee(self, employee_id: str):
        self.repo.delete(ObjectId(employee_id))
        return
