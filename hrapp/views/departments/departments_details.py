import sqlite3
from ..connection import Connection
from hrapp.models import Employee
from django.shortcuts import render, reverse, redirect

def get_employees(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select e.first_name, e.last_name, d.department_name
        from hrapp_employee e
        join hrapp_department d
        on e.department_id = d.id
        where e.department_id = ?;

            """, (department_id,))

        return db_cursor.fetchall()

def department_details(request, department_id):
    if request.method == 'GET':
        employees = get_employees(department_id)

        employee_list = []
        
        for row in employees:
            employee = Employee()
            employee.first_name = row['first_name']
            employee.last_name = row['last_name']
            employee.department_name = row['department_name']
            employee_list.append(employee)

        template = 'departments/department_detail.html'
        context = {
            'employees': employee_list,
            'dept_name': employee_list[0].department_name
        }

        return render(request, template, context)