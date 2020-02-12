import sqlite3
from ..connection import Connection
from django.shortcuts import render
from hrapp.models import Computer

def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
            select
                c.id,
                c.make,
                c.model,
                c.purchase_date,
                c.decommission_date
            from hrapp_computer c
            """)

            all_computers = []
            dataset = db_cursor.fetchall()
            for row in dataset:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.model = row['model']
                computer.purchase_date = row['purchase_date']
                computer.decommission_date = row['decommission_date']

                all_computers.append(computer)
        template = 'computers/computers_list.html'
        context = {
            'computers': all_computers
        }
        return render(request, template, context)