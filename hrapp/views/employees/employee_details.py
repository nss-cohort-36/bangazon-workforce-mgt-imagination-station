
import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Computer, Employee

def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    employee = Employee()
    employee.id = _row["id"]
    employee.make = _row["make"]
    employee.model = _row["model"]
    employee.purchase_date = _row["purchase_date"]
    employee.department_name = _row["department_name"]
    return employee

def create_computer(cursor, row):
    _row = sqlite3.Row(cursor, row)

    computer = Computer()
    computer.id = _row["id"]
    computer.first_name = _row["first_name"]
    computer.last_name = _row["last_name"]
    computer.start_date = _row["start_date"]
    return computer

def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_employee
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                d.department_name
            from hrapp_employee e
            join hrapp_department d 
            on e.department_id = d.id 
            where e.id = ?;

            """, (employee_id,))

        return db_cursor.fetchone()

def get_computer(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_employee
        db_cursor = conn.cursor()
        db_cursor.execute("""select 
            c.id,
            c.make,
            c.model,
            c.purchase_date
            from hrapp_employeecomputer ec 
            join hrapp_computer c on ec.computer_id = c.id
            where ec.employee_id = ?;""", (employee_id,))

        return db_cursor.fetchone()

@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        computer = get_computer(employee_id)

        template = 'employees/employees_detail.html'
        context = {
            'employee': employee,
            'computer': computer
        }
        print(employee)

        return render(request, template, context)