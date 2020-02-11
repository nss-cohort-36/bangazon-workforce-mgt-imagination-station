import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bangazonworkforcemgt.models import Employee
from bangazonworkforcemgt.models import model_factory
from ..connection import Connection


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.first_name,
            e.last_name,
            e.start_date,
            d.title
        from bangazonworkforcemgt_library e
        join department d on e.department_id = d.id
        """)

        return db_cursor.fetchall()

@login_required
def employee_form(request):
    if request.method == 'GET':
        employees = get_employees()
        template = 'employees/form.html'
        context = {
            'all_employees': employees
        }

        return render(request, template, context)