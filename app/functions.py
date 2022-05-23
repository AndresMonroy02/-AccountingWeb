from asyncio.windows_events import NULL
from random import random
from socket import MsgFlag
from urllib import request
from django.shortcuts import render, redirect
from .models import User_info, Users, Expenses, Vehicule
from cryptography.fernet import Fernet
from django.http import HttpResponse
import re
import uuid
import shortuuid
import bcrypt

def generate_id():
    id = str(uuid.uuid4())
    if Users.objects.filter(id=id).exists():
        new_id = generate_id()
        return new_id
    else:
        return id
    
def encrypt_password(password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

def validate_password(password, hashed):
    if bcrypt.hashpw(password, hashed) == hashed:
        return True
    else:
        return False

def generate_short_id(object):
    id = str(shortuuid.uuid())
    if object.objects.filter(id=id).exists():
        new_id = generate_id()
        return new_id
    else:
        return id

def get_user_data(user_id):
    user = Users.objects.get(id=user_id)
    return user

def get_user_vehicules(user_id):
    vehicules = Vehicule.objects.filter(user_id=user_id)
    return vehicules

def get_user_expenses(user_id):
    expenses = Expenses.objects.filter(user_id=user_id)
    return expenses

def get_user_info(user_id):
    vehicules = get_user_vehicules(user_id)
    num_vehicules = len(vehicules) 
    user_data = get_user_data(user_id)
    user_info = User_info.objects.get(id=user_id)
    name = user_data.name
    email = user_data.email
    salary = user_info.salary
    pay_day = user_info.pay_day
    return num_vehicules, name, email, salary , pay_day


def filter_by_dates(start_date, end_date, user_id):
    expenses = Expenses.objects.filter(
        user_id=user_id,
        date__gte=start_date,
        date__lte=end_date
    )
    return expenses

