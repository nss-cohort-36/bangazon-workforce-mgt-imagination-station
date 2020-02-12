
import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Computer, Employee, TrainingProgram
# Author: Lauren Riddle
# Purpose: to display employee details
def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    employee = Employee()
    employee.id = _row["id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.start_date = _row["start_date"]
    employee.department_name = _row["department_name"]
    return employee

def create_computer(cursor, row):
    _row = sqlite3.Row(cursor, row)

    computer = Computer()
    computer.id = _row["id"]
    computer.make = _row["make"]
    computer.model = _row["model"]
    computer.purchase_date = _row["purchase_date"]
    return computer

def create_program(cursor, row):
    _row = sqlite3.Row(cursor, row)
    programslist = list()

    program = TrainingProgram()
    program.id = _row["id"]
    program.title = _row["title"]
    program.start_date = _row["start_date"]
    program.end_date = _row["end_date"]
    programslist.append(program)
    return programslist

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
        conn.row_factory = create_computer
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select 
            c.id,
            c.make,
            c.model,
            c.purchase_date
            from hrapp_employeecomputer ec 
            join hrapp_computer c on ec.computer_id = c.id
            where ec.employee_id = ?;""", (employee_id,))

        return db_cursor.fetchone()

def get_programs(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_program
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            t.id,
            t.title,
            t.start_date,
            t.end_date
            from hrapp_employeetrainingprogram et 
            join hrapp_trainingprogram t on et.training_program_id = t.id
            where et.employee_id = ?
            """, (employee_id,))

        return db_cursor.fetchall()

def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        computer = get_computer(employee_id)
        programs = get_programs(employee_id)

        template = 'employees/employees_detail.html'
        context = {
            'employee': employee,
            'computer': computer,
            'programs': programs
        }
        print(programs)

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_employeetrainingprogram
            (
                employee_id, training_program_id
            )
            VALUES (?, ?)
            """,
            (form_data['employee_id'], form_data['training_program_id']))

        return redirect(reverse('hrapp:employee_list'))