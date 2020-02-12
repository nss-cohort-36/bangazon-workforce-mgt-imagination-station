import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram
from ..connection import Connection


def get_training_program_details(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select
                tp.id,
                tp.title,
                tp.start_date,
                tp.end_date,
                tp.capacity,
                e.first_name,
                e.last_name
            from hrapp_trainingprogram tp
            join hrapp_employeetrainingprogram etp
            on etp.training_program_id = tp.id
            join hrapp_employee e
            on e.id = etp.employee_id
            where tp.id = ?
        """,
            (training_program_id,),
        )

        return db_cursor.fetchall()


@login_required
def training_program_details(request, training_program_id):
    if request.method == "GET":
        training_program_details = get_training_program_details(
            training_program_id)

        employee_training = TrainingProgram()

        for row in training_program_details:
            if employee_training.title == "":
                employee_training.title = row['title']
                employee_training.start_date = row['start_date']
                employee_training.end_date = row['end_date']
                employee_training.capacity = row['capacity']
                employee_training.attendees = [
                    f"{row['first_name']} {row['last_name']}"]

            else:
                employee_training.attendees.append(
                    f"{row['first_name']} {row['last_name']}")

        template = "training_programs/detail.html"
        context = {"training_program_details": employee_training}

        return render(request, template, context)
