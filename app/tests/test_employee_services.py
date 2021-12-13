import random

import pytest
from faker import Faker
from fastapi.exceptions import HTTPException

from app.models.employee import EmployeeCreate, EmployeeFilter, EmployeeUpdate
from app.services.employee import EmployeeService

fake = Faker()


first_name, last_name = fake.name().split()[:2]
employee_data = {
    "first_name": first_name,
    "last_name": last_name,
    "id_number": fake.ssn(),
    "kra_pin": fake.ssn(),
    "nhif_number": fake.ssn(),
    "nssf_number": fake.ssn(),
    "tax_exemption_number": fake.ssn(),
    "is_resident": random.choice([True, False]),
    "is_director": random.choice([True, False]),
    "is_tax_exempt": random.choice([True, False]),
    "has_disability": random.choice([True, False]),
    "employment_status": "active",
}
employee_data_2 = {
    "first_name": first_name,
    "last_name": last_name,
    "id_number": fake.ssn(),
    "kra_pin": fake.ssn(),
    "nhif_number": fake.ssn(),
    "nssf_number": fake.ssn(),
    "tax_exemption_number": fake.ssn(),
    "is_resident": random.choice([True, False]),
    "is_director": random.choice([True, False]),
    "is_tax_exempt": random.choice([True, False]),
    "has_disability": random.choice([True, False]),
    "employment_status": "active",
}


def test_create_employee(mongodb_test_repository):
    employee = EmployeeCreate(**employee_data)
    created_employee = EmployeeService(mongodb_test_repository).create_employee(
        employee
    )
    del created_employee["_id"]
    del created_employee["middle_name"]
    assert employee_data == created_employee


def test_create_duplicate_employee(mongodb_test_repository):
    mongodb_test_repository.collection.create_index("id_number", unique=True)
    employee = EmployeeCreate(**employee_data)
    EmployeeService(mongodb_test_repository).create_employee(employee)
    with pytest.raises(HTTPException) as e:
        EmployeeService(mongodb_test_repository).create_employee(employee)
    assert e.value.status_code == 409


def test_get_all_employees(mongodb_test_repository):
    employee_1 = EmployeeCreate(**employee_data)
    employee_2 = EmployeeCreate(**employee_data_2)
    EmployeeService(mongodb_test_repository).create_employee(employee_1)
    EmployeeService(mongodb_test_repository).create_employee(employee_2)

    employees = EmployeeService(mongodb_test_repository).get_all_employees()
    assert (len(employees)) == 2


def test_get_employee_by_id(mongodb_test_repository):
    employee_1 = EmployeeCreate(**employee_data)
    employee_2 = EmployeeCreate(**employee_data_2)
    created_employee_1 = EmployeeService(mongodb_test_repository).create_employee(
        employee_1
    )
    created_employee_2 = EmployeeService(mongodb_test_repository).create_employee(
        employee_2
    )

    employee = EmployeeService(mongodb_test_repository).get_employee_by_id(
        created_employee_1.get("_id")
    )
    assert employee.get("_id") == created_employee_1.get("_id")
    employee = EmployeeService(mongodb_test_repository).get_employee_by_id(
        created_employee_2.get("_id")
    )
    assert employee.get("_id") == created_employee_2.get("_id")


def test_get_employee_by_first_name_filter(mongodb_test_repository):
    employee = EmployeeCreate(**employee_data)
    EmployeeService(mongodb_test_repository).create_employee(employee)
    filter_parameters = EmployeeFilter(first_name=employee.first_name)
    filtered_employee = EmployeeService(
        mongodb_test_repository
    ).get_employees_by_filters(filter_parameters)
    assert employee.first_name == filtered_employee[0].get("first_name")


def test_update_employee_details(mongodb_test_repository):
    employee = EmployeeCreate(**employee_data)
    created_employee = EmployeeService(mongodb_test_repository).create_employee(
        employee
    )
    update = EmployeeUpdate(first_name=employee.first_name + "!!")
    updated_employee = EmployeeService(mongodb_test_repository).update_employee_details(
        created_employee.get("_id"), update
    )
    assert employee.first_name != updated_employee.get("first_name")


def test_delete_employee(mongodb_test_repository):
    employee = EmployeeCreate(**employee_data)
    created_employee = EmployeeService(mongodb_test_repository).create_employee(
        employee
    )
    employee = EmployeeService(mongodb_test_repository).get_employee_by_id(
        created_employee.get("_id")
    )
    assert employee.get("_id") == created_employee.get("_id")
    EmployeeService(mongodb_test_repository).delete_employee(
        created_employee.get("_id")
    )
    employee = EmployeeService(mongodb_test_repository).get_employee_by_id(
        created_employee.get("_id")
    )
    assert employee is None
