
import os

from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

import sqlite3 as dbapi
class ReportLab:

    bd = dbapi.connect("biblioteca.dat")
    cursor = bd.cursor()

    cursor.execute("select * from biblioteca")
    tablaBaseDatos = []

    cabecera = ["CODIGO","NOMBRE","PRECIO","UNIDADES","FECHA","AUTOR"]

    tablaBaseDatos.append(cabecera)

    for fila in cursor:
        tablaBaseDatos.append(fila)

    taboa = Table(tablaBaseDatos)

    guion = []
    guion.append(taboa)

    document = SimpleDocTemplate("Informe.pdf", pagesize=A4, showBoundary=0)
    document.build(guion)
    cursor.close()
    bd.close()

