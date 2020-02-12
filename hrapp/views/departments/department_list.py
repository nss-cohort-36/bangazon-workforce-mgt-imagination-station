import sqlite3
from django.shortcuts import render
from hrapp.models import Department
from ..connection import Connection

def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # TODO: Add dept total
            db_cursor.execute("""
            select
            d.id,
            d.department_name,
            d.budget,
            count() as dept_total
            from hrapp_department d
            join hrapp_employee e
            on d.id = e.department_id
            group by d.id
            """)

            all_departments = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                department = Department()
                department.id = row['id']
                department.department_name = row['department_name']
                department.budget = row['budget']
                department.dept_total = row['dept_total']
            
                all_departments.append(department)

    template = 'departments/department_list.html'
    context = {
        'departments': all_departments
    }

    return render(request, template, context)