from django.shortcuts import render, HttpResponse
import pyodbc 
import pandas as pd
from .models import Venta
# from sqlalchemy import create_engine
connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:/Users/Leo/Documents/Restaurant_And_Delivery_Manager_6/Datos/BD_Restaurant_All.accdb;"
    # r"SystemDB=C:\whatever\mydatabase.mdw;"
    r"Uid=Admin;"
    r"PWD=1234;"    
    )
# Create your views here.
def home(request):    
    
    conn = pyodbc.connect(connStr)   
    # Quitar al completar un pedido
    
    consulta = ' and Detalle_Venta.Id_Venta > %s ' %Venta.objects.latest('id_pedido')
    df = pd.read_sql_query('''select Detalle_Venta.Id_Venta as id, Detalle_Venta.Producto , Detalle_Venta.Cantidad, Numero_Boleta as boleta from Detalle_Venta inner join Ventas on Detalle_Venta.Id_Venta = Ventas.Id_Venta where Producto not in ('BEBIDA EN LATA') and Detalle_Venta.Id_Venta in (select distinct top 40 Id_Venta from Detalle_Venta order by Id_Venta desc) %s ''' %consulta, conn)  
    conn.close()
    return render(request, "core/index.html", {'datos': df,'rango':range(len(df))})


def completar(request, id_pedido):
    venta = Venta()
    venta.id_pedido = id_pedido
    venta.estado = 1
    venta.save()
    conn = pyodbc.connect(connStr) 
    consulta = ' and Detalle_Venta.Id_Venta > %s' %Venta.objects.latest('id_pedido')
    df = pd.read_sql_query('''select Detalle_Venta.Id_Venta as id, Detalle_Venta.Producto , Detalle_Venta.Cantidad, Numero_Boleta as boleta from Detalle_Venta inner join Ventas on Detalle_Venta.Id_Venta = Ventas.Id_Venta where Producto not in ('BEBIDA EN LATA') and Detalle_Venta.Id_Venta in (select distinct top 40 Id_Venta from Detalle_Venta order by Id_Venta desc) %s''' %consulta, conn)  
    conn.close()
    return render(request, "core/index.html", {'datos': df,'rango':range(len(df))})


def completado(request):
    conn = pyodbc.connect(connStr) 
    # Quitar al completar un pedido
    consulta = ' and Detalle_Venta.Id_Venta <= %s ' %Venta.objects.latest('id_pedido')
    df = pd.read_sql_query('''select Detalle_Venta.Id_Venta as id, Detalle_Venta.Producto , Detalle_Venta.Cantidad, Numero_Boleta as boleta from Detalle_Venta inner join Ventas on Detalle_Venta.Id_Venta = Ventas.Id_Venta where Producto not in ('BEBIDA EN LATA') and Detalle_Venta.Id_Venta in (select distinct top 20 Id_Venta from Detalle_Venta order by Id_Venta desc) %s order by Detalle_Venta.Id_Venta desc''' %consulta, conn)  
    conn.close()
    return render(request, "core/completado.html", {'datos': df,'rango':range(len(df))})
