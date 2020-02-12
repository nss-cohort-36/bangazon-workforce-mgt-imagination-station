import sqlite3
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer, model_factory
from ..connection import Connection
from django.contrib import messages

def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.make,
            c.model,
            c.purchase_date,
            c.decommission_date,
            e.first_name,
            e.last_name            
        FROM 
            hrapp_computer c
        LEFT JOIN 
            hrapp_employeecomputer ec
        ON
            ec.computer_id = c.id
        LEFT JOIN 
            hrapp_employee e
        ON 
            ec.employee_id = e.id
        WHERE c.id = ?
        """, (computer_id,))

        data_set = db_cursor.fetchone()
        computer = Computer()
        computer.id = data_set['id']
        computer.make = data_set['make']
        computer.model = data_set['model']
        computer.purchase_date = data_set['purchase_date']
        computer.decommission_date = data_set['decommission_date']
        computer.first_name = data_set['first_name']
        computer.last_name = data_set['last_name']

        return computer




@login_required
def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)

        template = 'computers/computer_details.html'
        context = {
            'computer': computer
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        
        # Check if this POST is for deleting a computer
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_computer
                WHERE id = ?
                """, (computer_id,))

        return redirect(reverse('hrapp:computer_list'))