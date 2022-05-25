from contextvars import Context
from dataclasses import dataclass
import email
from multiprocessing import context
from optparse import Values
import profile
from pyexpat import model
import re
from tkinter.tix import Form
from unicodedata import category, name
from urllib.request import Request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Users, Expenses, Vehicule, User_info, Report
from django.contrib.admin import widgets  
from .functions import *
# Create your views here.




def index(request):
    return render (request, 'pages/index.html', {})

def login(request): 
    # login_method(request)
    if 'usuario' in request.session:
        name = request.session['usuario']['name']
        user_id = request.session['usuario']['id']
        print(name)
        return render (request, 'pages/expenses.html', {'name':name, 'user_id':user_id})
    else:
        if request.method == "POST":
            values = request.POST
            email = values['email']
            password = values['password']
            if Users.objects.filter(email=email).exists():
                user = Users.objects.get(email=email)
                if validate_password(password, user.password) == True:
                    request.session['usuario'] = {'id':user.id, 'name':user.name}
                    name = request.session['usuario']['name']
                    user_id = request.session['usuario']['id']
                    return render(request,'pages/expenses.html',{'name':name, 'user_id':user_id})
                else:
                    return render (request, 'pages/login.html', {'error':'Contraseña incorrecta'})
            else:
                return render (request, 'pages/login.html', {'error':'Email incorrecto'})
    return render (request, 'pages/login.html', {})

def logout_site(request): 
    if 'usuario' in request.session:
        del request.session['usuario']
    return render(request, 'pages/index.html',)

def register(request):
    if request.method == "POST":
        values = request.POST
        validate_id = generate_id()
        print(validate_id)
        name = values['name']
        last_name = values['last_name']
        email = values['email']
        password = values['password']
        password2 = values['password2']
        pay_day = values['pay_day']
        if password == password2:
            if 8 <= len(password) <= 16:
                if re.search('[a-z]', password) and re.search('[A-Z]', password) and re.search('[0-9]', password):
                    if Users.objects.filter(email=email).exists():
                        return render (request, 'pages/register.html', {'error':'El email ya esta registrado'})
                    else:
                        encrypted_password = encrypt_password(password)
                        fullname = name + ' ' + last_name
                        user = Users(id=validate_id, name=fullname, email=email, password=encrypted_password)       # Create a new user
                        user.save()
                        user_id = Users.objects.get(id=validate_id)   
                        user_info = User_info(id= validate_id, fullname=fullname, salary=0, pay_day=pay_day, user=user_id)
                        print(user_info)
                        user_info.save()
                        return redirect('login')
                else:
                    return render (request, 'pages/register.html', {'error':'La contraseña debe contener al menos una mayuscula, una minuscula y un numero'})
            else:
                return render (request, 'pages/register.html', {'error':'La contraseña debe tener al menos 8 caracteres o no superar los 16 caracteres'})
        else:
            return render (request, 'pages/register.html', {'error':'Las contraseñas no coinciden'})

    return render (request, 'pages/register.html', {})


def expenses(request):
    if 'usuario' in request.session:
        if request.method == "POST":
            values = request.POST
            expense_id = generate_short_id(Expenses)
            expense_amount = values['expense_amount']
            expense_category = values['expense_category']
            expense_description = values['expense_description']
            expense_date = values['expense_date']
            id = request.session['usuario']['id']
            user_id = Users.objects.get(id=id)
            if expense_amount == '':
                return redirect('expenses')
            if expense_description == '':
                expense_description = 'Sin descripcion'
                expense = Expenses(id=expense_id, amount=expense_amount, category=expense_category, description=expense_description, date=expense_date, user=user_id)
                expense.save()
            elif expense_description != '':
                expense = Expenses(id=expense_id, amount=expense_amount, category=expense_category, description=expense_description, date=expense_date, user=user_id)
                expense.save()
        user_id = request.session['usuario']['id']
        expenses = get_user_expenses(user_id)
        num_vehicules, name,email,salary, pay_day= get_user_info(user_id)
        return render (request, 'pages/expenses.html', {'expenses':expenses, 'name':name , 'email':email, 'num_vehicules':num_vehicules, 'salary':salary,'user_id':user_id})
    else:
        return redirect('login')

def vehicules(request):
    if 'usuario' in request.session:
        if request.method == "POST":
            values = request.POST
            placa = values['placa']
            year = values['year']
            model = values['model']
            tecno = values['tecno']
            soat = values['soat']
            oil_change = values['oil_change']
            id = request.session['usuario']['id']
            user_id = Users.objects.get(id=id)
            vehicule_id = generate_short_id(Vehicule)
            vehicule = Vehicule(id=vehicule_id, placa=placa, year=year, model=model, tecno=tecno, soat=soat, oil_change=oil_change, user=user_id)
            vehicule.save()
            return redirect('vehicules')
        user_id = request.session['usuario']['id']
        vehicules = get_user_vehicules(user_id)
        num_vehicules, name,email,salary, pay_day= get_user_info(user_id)
        return render (request, 'pages/vehicules.html', {'vehicules':vehicules,'name':name , 'email':email, 'num_vehicules':num_vehicules, 'salary':salary,'user_id':user_id})
    else:
        return redirect('login')


def reports(request):
    if 'usuario' in request.session:
        user_id = request.session['usuario']['id']
        user = Users.objects.get(id=user_id)
        expenses = get_user_expenses(user_id)
        num_vehicules, name,email,salary, pay_day= get_user_info(user_id)
        
        if request.method == "POST":
            values = request.POST
            start_date = values['start_date']
            name = values['name']
            end_date = values['end_date']
            repot_id = generate_short_id(Report)
            description = "Reporte de gastos inicio: " + start_date + " fin: " + end_date
            report = Report(id=repot_id, name=name, description=description, start_date=start_date, end_date=end_date, user=user)
            report.save()
            return redirect('reports')
        else:
            reports = Report.objects.filter(user_id=user_id)
            return render (request, 'pages/reports.html', {'reports':reports, 'name':name , 'email':email, 'num_vehicules':num_vehicules, 'salary':salary,'user_id':user_id})      
    else:
        return redirect('login')
    

def show_reports(request, report_id):
    user_id = request.session['usuario']['id']
    if 'usuario' in request.session:
        categories = ["Alimentacion","Transporte", "Ropa", "Hogar", "Salud",  "Educacion", "Otros"]
        labels = []
        data = []
        report = Report.objects.get(id=report_id)
        name = report.name
        start_date = report.start_date
        end_date = report.end_date
        expenses_list = filter_by_dates(start_date, end_date, user_id)
        for i in categories:
            amount = 0
            for expense in expenses_list:
                if expense.category == i:
                    amount += float(expense.amount)
            labels.append(i)
            data.append(amount)

        print(labels)
        print(data)
        return render (request, 'pages/reportsView.html', {'user_id':user_id, 'labels':labels, 'data':data})
    else:
        return redirect('login')

def contact(request):
    return render (request, 'pages/contact.html', {})

def edit(request, expense_id):
    if 'usuario' in request.session:
        if request.method == "POST":
            values = request.POST.get
            expense_amount = values('expense_amount')
            expense_category = request.POST.get('expense_category')
            expense_description = values('expense_description')
            expense_date = values('expense_date')
            expense = Expenses.objects.get(id=expense_id)
            user_id = request.session['usuario']['id']
            user = Users.objects.get(id=user_id)
            num_vehicules, name,email,salary, pay_day= get_user_info(user_id)
            if expense_description == '':
                    expense_description = 'Sin descripcion'
                    expense = Expenses(id=expense_id, amount=expense_amount, category=expense_category, description=expense_description, date=expense_date, user=user)
                    expense.save()
            elif expense_description != '':
                    expense = Expenses(id=expense_id, amount=expense_amount, category=expense_category, description=expense_description, date=expense_date, user=user)
                    expense.save()
            return redirect('expenses')
        else:
            expense = Expenses.objects.get(id=expense_id)
            user_id = request.session['usuario']['id']
            num_vehicules, name,email,salary, pay_day= get_user_info(user_id)
            return render(request, 'pages/edit.html', {'expense':expense,'name':name , 'email':email, 'num_vehicules':num_vehicules, 'salary':salary, 'user_id':user_id})
        
def edit_vehicule(request, vehicule_id):
    if 'usuario' in request.session:
        if request.method == "POST":
            values = request.POST.get
            placa = values('placa')
            year = values('year')
            model = values('model')
            tecno = values('tecno')
            soat = values('soat')
            oil_change = values('oil_change')
            vehicule = Vehicule.objects.get(id=vehicule_id)
            user_id = request.session['usuario']['id']
            user = Users.objects.get(id=user_id)
            num_vehicules, name,email,salary, pay_day= get_user_info(user_id)
            vehicule = Vehicule(id=vehicule_id, placa=placa, year=year, model=model, tecno=tecno, soat=soat, oil_change=oil_change, user=user)
            vehicule.save()
            return redirect('vehicules')
        else:
            vehicule = Vehicule.objects.get(id=vehicule_id)
            user_id = request.session['usuario']['id']
            num_vehicules, name,email,salary, pay_day= get_user_info(user_id)
            return render(request, 'pages/edit_vehicule.html', {'vehicule':vehicule, 'name':name , 'email':email, 'num_vehicules':num_vehicules, 'salary':salary, 'user_id':user_id})


def config(request, user_id):
    user = User_info.objects.get(user_id=user_id)
    return render (request, 'system/config.html', {'user':user, 'user_id':user_id})

def configedit(request, user_id):
    if request.method == 'POST':
        values = request.POST.get
        fullname = values('fullname')
        salary = values('salary')
        pay_day = values('pay_day')
        user_info = User_info.objects.get(user_id=user_id)
        user_id = request.session['usuario']['id']
        user = Users.objects.get(id=user_id)
        user_info = User_info(id=user_id,fullname=fullname, salary=salary, pay_day=pay_day, user=user)
        user_info.save()
        return redirect('config', user_id)
    else:
        user = User_info.objects.get(user_id=user_id)
        return render (request, 'system/configedit.html', {'user':user, 'user_id':user_id})
