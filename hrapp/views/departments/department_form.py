from django.shortcuts import render

def department_form(request):
    if request.method == 'GET':
        template = 'departments/department_form.html'
        context = {}
        
        return render(request, template, context)