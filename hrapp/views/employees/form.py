import sqlite3
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models.department import Department
from hrapp.models.computer import Computer
from hrapp.models.employee_computer import EmployeeComputer
from hrapp.models import model_factory
from ..connection import Connection
from hrapp.views.employees.employee_details import get_employee

def get_departments():

    """
    Author: Michelle Johnson
    Purpose: Gets all departments
    """
    
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.department_name
        from hrapp_department d
        """)

        return db_cursor.fetchall()

def get_computer():

    """
    Purpose: Gets all single computer
    """

    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select 
            c.id,
            c.make,
            c.model
            from hrapp_computer c
            """)

        return db_cursor.fetchall()

def get_assigned_computer():

    """
    Purpose: Gets all computers that are assigned and computers that are decommissioned
    """

    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(EmployeeComputer)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select 
            c.id,
            c.make,
            c.model,
            c.decommission_date,
            ec.unassigned_date,
            ec.employee_id
            
            from hrapp_employeecomputer ec 
            left join hrapp_computer c on ec.computer_id = c.id
			where unassigned_date is NULL or decommission_date is not NULL;""")

        return db_cursor.fetchall()
        

@login_required
def employee_form(request):

    """
    Purpose: requests data from the database thru the SQL query
    """

    if request.method == 'GET':
        departments = get_departments()
        computers = get_computer()
        assigned_computers = get_assigned_computer()

        assigned_computer_ids = []
        unassigned_computers = []

    # loops thru all computers and takes out computers that are assigned to an employee or have been decommissioned

        for computer in assigned_computers:
            assigned_computer_ids.append(computer.id)

        for computer in computers:
            if computer.id not in assigned_computer_ids:
                unassigned_computers.append(computer)

        template = 'employees/form.html'
        context = {
            'all_departments': departments,
            'all_computers': computers,
            'unassigned_computers': unassigned_computers,
            'assigned_computer_ids': assigned_computer_ids,        }

        return render(request, template, context)

@login_required
def employee_edit_form(request, employee_id):

    """
    Purpose: requests data from the database thru the SQL query
    """

    if request.method == 'GET':
        employee = get_employee(employee_id)
        departments = get_departments()
        computers = get_computer()
        assigned_computers = get_assigned_computer()

        assigned_computer_ids = []
        unassigned_computers = []

    # loops thru all computers and takes out computers that are assigned to an employee or have been decommissioned

        for computer in assigned_computers:
            assigned_computer_ids.append(computer.id)

        for computer in computers:
            if computer.id not in assigned_computer_ids:
                unassigned_computers.append(computer)

        template = 'employees/form.html'
        context = {
            'employee': employee,
            'all_departments': departments,
            'unassigned_computers': unassigned_computers,
            'assigned_computer_ids': assigned_computer_ids,
        }

        return render(request, template, context)