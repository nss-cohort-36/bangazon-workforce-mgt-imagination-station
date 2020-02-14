
# Author: Lauren Riddle
# Purpose: To display employee details
import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Computer, Employee, TrainingProgram
def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    employee = Employee()
    employee.id = _row["id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.start_date = _row["start_date"]
    employee.is_supervisor = _row["is_supervisor"]
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
        return render(request, template, context)

# author: Michelle Johnson

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_employee
                SET first_name = ?,
                    last_name = ?,
                    start_date = ?,
                    department_id = ?,
                    is_supervisor = ?
                WHERE id = ?
                """,
                (
                    form_data['first_name'], form_data['last_name'],
                    form_data['start_date'], form_data['department_id'],
                    form_data["is_supervisor"], employee_id,
                ))

                db_cursor.execute("""
                UPDATE hrapp_employeecomputer
                SET unassigned_date = CURRENT_DATE
                WHERE employee_id = ?
                AND unassigned_date IS NULL;
                """,
                (employee_id,))


                db_cursor.execute("""
                INSERT INTO hrapp_employeecomputer
                (
                    assigned_date, computer_id, employee_id, unassigned_date
                )
                VALUES (CURRENT_DATE, ?, ?, NULL)
                """,

                (form_data["computer_id"],employee_id))

        return redirect(reverse('hrapp:employee_list'))
            
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

        return redirect(reverse('hrapp:employee_details', kwargs={'employee_id':employee_id}))
