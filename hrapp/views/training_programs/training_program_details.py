import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram
from ..connection import Connection
from .training_program_list import is_future_training


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
                e.id employee_id,
                e.first_name,
                e.last_name
            from hrapp_trainingprogram tp
            left join hrapp_employeetrainingprogram etp
            on etp.training_program_id = tp.id
            left join hrapp_employee e
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
                employee_training.id = row['id']
                employee_training.title = row['title']
                employee_training.start_date = row['start_date']
                employee_training.end_date = row['end_date']
                employee_training.capacity = row['capacity']
                employee_training.is_future = is_future_training(
                    employee_training.start_date)
                employee_training.attendees = []
                if row['employee_id']:
                    employee_training.attendees.append((row['employee_id'],
                                                        f"{row['first_name']} {row['last_name']}"))

            else:
                employee_training.attendees.append(
                    (row['employee_id'], f"{row['first_name']} {row['last_name']}"))

        template = "training_programs/training_programs_detail.html"
        context = {"training_details": employee_training}

        return render(request, template, context)

    if request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_trainingprogram
                WHERE id = ?
                """, (training_program_id,))

            return redirect(reverse('hrapp:training_program_list'))

        # Check if this POST is for editing a book
        if "actual_method" in form_data and form_data["actual_method"] == "PUT":
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute(
                    """
                UPDATE hrapp_trainingprogram
                SET title = ?,
                    start_date = ?,
                    end_date = ?,
                    capacity = ?
                WHERE id = ?
                """,
                    (
                        form_data["title"],
                        form_data["start_date"],
                        form_data["end_date"],
                        form_data["capacity"],
                        training_program_id,
                    ),
                )

            return redirect(reverse("hrapp:training_program_details", kwargs={'training_program_id': training_program_id}))
