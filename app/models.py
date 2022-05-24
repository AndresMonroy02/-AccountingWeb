from ast import Delete
import email
from operator import truediv
from pyexpat import model
from tabnanny import verbose
from unicodedata import category, name
from django.db import models


class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=150, verbose_name="Id")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(max_length=100, verbose_name="Email")
    password = models.CharField(max_length=100,  verbose_name="contraseña",)
    
    def __str__(self):
        return self.name

class User_info(models.Model):
    id = models.CharField(primary_key=True, max_length=100, verbose_name="Id")
    fullname = models.CharField(max_length=100, verbose_name="Nombre")
    salary = models.FloatField(max_length=100, verbose_name="Salario")
    pay_day = models.DateField(verbose_name="Dia de pago")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Id")

    def __str__(self):
        return self.fullname

class Expenses(models.Model):
    id = models.CharField(primary_key=True, max_length=100, verbose_name="Id")
    amount = models.FloatField(max_length=100, verbose_name="Valor")
    category = models.CharField(max_length=100, verbose_name="Categoria",)
    description = models.CharField(max_length=100, verbose_name="Descripcion")
    date = models.DateField(verbose_name="Fecha")
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.id


class Vehicule(models.Model):
    id = models.CharField(primary_key=True, max_length=100, verbose_name="Id")
    placa = models.CharField(max_length=40, verbose_name="Placa")
    year = models.CharField(max_length=10, verbose_name="Año")
    model = models.CharField(max_length=10, verbose_name="Modelo")
    tecno = models.DateField(max_length=10, verbose_name="tecnomecanica")
    soat = models.DateField(max_length=10, verbose_name="Soat")
    oil_change = models.DateField(max_length=10, verbose_name="Cambio de aceite")
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.placa

class Report(models.Model):
    id = models.CharField(primary_key=True, max_length=150, verbose_name="Id")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.CharField(max_length=100, verbose_name="Descripcion")
    start_date = models.DateField(max_length=10,verbose_name="Fecha inicial")
    end_date = models.DateField(max_length=10,verbose_name="Fecha final")
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.id