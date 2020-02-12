import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram, EmployeeTrainingProgram
from hrapp.models import model_factory
from ..connection import Connection

def get_programs():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            t.id,
            t.title,
            t.start_date,
            t.end_date,
            t.capacity
        from hrapp_trainingprogram t
        """)

        return db_cursor.fetchall()

def get_relationships(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(EmployeeTrainingProgram)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            t.id,
            t.title,
            t.start_date,
            t.end_date,
            et.training_program_id,
            et.employee_id
            from hrapp_employeetrainingprogram et 
            join hrapp_trainingprogram t on et.training_program_id = t.id
            where et.employee_id = ?
        """, (employee_id))
    
        return db_cursor.fetchall()

def employee_training_program_form(request, employee_id):
    if request.method == 'GET':
        employeeId = employee_id
        programs = get_programs()
        relationships = get_relationships(employee_id)
        template = 'employees/employee_training_program_form.html'
        context = {
            'all_programs': programs,
            'employeeId': employeeId,
            'relationships': relationships
        }


        return render(request, template, context)
