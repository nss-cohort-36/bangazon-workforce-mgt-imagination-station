import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram, EmployeeTrainingProgram
from hrapp.models import model_factory
from ..connection import Connection
from ..training_programs.training_program_list import is_future_training

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

def get_relationships(employee_id):
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
@login_required
def employee_training_program_form(request, employee_id):
    if request.method == 'GET':
        program_list = list()
        employeeId = employee_id
        programs = get_programs()
        relationships = get_relationships(employee_id)
        programIds_list = list()
        for relationship in relationships:
            programIds_list.append(relationship[0].id)
        for program in programs:
            if program.id not in programIds_list and is_future_training(program.start_date):
                program_list.append(program)
        template = 'employees/employee_training_program_form.html'
        context = {
            'all_programs': program_list,
            'employeeId': employeeId,
            'relationships': relationships
        }


        return render(request, template, context)
