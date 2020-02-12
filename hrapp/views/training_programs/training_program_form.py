import sqlite3
from django.shortcuts import render
from hrapp.models import TrainingProgram
from ..connection import Connection


# def get_training_program(training_program_id):
#     with sqlite3.connect(Connection.db_path) as conn:
#         conn.row_factory = model_factory(Book)
#         db_cursor = conn.cursor()

#         db_cursor.execute(
#             """
#         select
#             tp.id,
#             tp.title,
#             tp.start_date,
#             tp.end_date,
#             tp.capacity
#         from hrapp_trainingprogram tp
#         WHERE tp.id = ?
#         """,
#             (training_program_id,),
#         )

#         return db_cursor.fetchone()


def training_program_form(request):
    if request.method == "GET":
        template = "training_programs/training_programs_form.html"
        context = {}

        return render(request, template, context)


# def book_edit_form(request, book_id):

#     if request.method == "GET":
#         book = get_book(book_id)
#         libraries = get_libraries()

#         template = "books/form.html"
#         context = {"book": book, "all_libraries": libraries}

#         return render(request, template, context)
