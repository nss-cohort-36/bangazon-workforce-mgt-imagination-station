import sqlite3
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer, model_factory
from ..connection import Connection
from django.contrib import messages

def never_assigned(computer_id):
    """
    Checks to see if a computer was ever assigned to an employee.
    Returns a Boolean FALSE if ever assigned, and TRUE if never assigned.
    Arugments:
        computer_id: integer
    Author: Ryan Crowley
    """
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT computer_id
        FROM hrapp_employeecomputer
        WHERE computer_id = ?
        """, (computer_id,))

        data_set = db_cursor.fetchall()

        if data_set:
            return False
        else:
            return True

def currently_assigned(computer_id):
    """
    Checks to see if a computer is currently assigned to an employee.
    Returns a Boolean TRUE computer is currently assigned, and FALSE if not.
    Arugments:
        computer_id: integer
    Author: Ryan Crowley
    """
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()
        conn.row_factory = sqlite3.Row

        db_cursor.execute("""
        SELECT 
            unassigned_date
        FROM hrapp_employeecomputer
        WHERE computer_id = ?
        """, (computer_id,))

        data_set = db_cursor.fetchall()
        for row in data_set:
            if not row[0]:
                return True
        return False


def get_computer(computer_id):
    """
    Queries the database to get information about a computer
    Returns a Computer instance. Calls never_assigned and currently_assigned to
    determine how to instantiate the Computer instance that will be returned.
    Arugments:
        computer_id: integer
    Author: Ryan Crowley
    """
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
            e.last_name,
            ec.unassigned_date          
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

        data_set = db_cursor.fetchall()

        for row in data_set:
            if currently_assigned(row['id']):
                if not row['unassigned_date']:
                    computer = Computer()
                    computer.id = row['id']
                    computer.make = row['make']
                    computer.model = row['model']
                    computer.purchase_date = row['purchase_date']
                    computer.decommission_date = row['decommission_date']
                    computer.first_name = row['first_name']
                    computer.last_name = row['last_name']
                    computer.never_assigned = never_assigned(computer.id)

                    return computer
            else:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.model = row['model']
                computer.purchase_date = row['purchase_date']
                computer.decommission_date = row['decommission_date']
                computer.never_assigned = never_assigned(computer.id)

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