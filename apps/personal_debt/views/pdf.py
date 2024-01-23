from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from apps.personal_debt.models import Credit, CreditsDetail


def generar_pdf_prestamo(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prestamos.pdf"'

    buffer = response
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    width, height = letter

    # Lista que contendrá todos los elementos que se añadirán al PDF
    elements = []

    # Título del PDF, centrado
    title_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ])
    title_table = Table([["Lista de Préstamos"]], colWidths=[
                        width], style=title_style)
    elements.append(title_table)

    elements.append(Spacer(1, 20))

    # Encabezados de las columnas para la tabla
    encabezados = ('ID Crédito', 'Empleado', 'Tipo Descuento',
                   'Valor Préstamo', 'Saldo', 'Cuota', 'Fecha')
    data = [encabezados]  # Lista de listas para la data de la tabla

    # Estilos de la tabla
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Agregar los datos de Credit y CreditsDetail a la tabla
    for credito in Credit.objects.all():
        credit_data = [
            str(credito.id),
            credito.employee.last_name + " " + credito.employee.firts_name,
            # Asumiendo que "PRESTAMO A LA EMPRESA" es el formato y quieres solo "PRESTAMO"
            credito.item.description.split(" ")[0],
            "{:.2f}".format(credito.loan_val),
            "{:.2f}".format(credito.balance),
            ""  # Cuota inicialmente vacía
        ]
        data.append(credit_data)

        # Agregar las filas de los CreditsDetail asociados
        for detalle in CreditsDetail.objects.filter(credit=credito).order_by('quota'):
            detail_data = [
                "",  # ID Crédito vacío para las filas de detalle
                "",  # Empleado vacío para las filas de detalle
                "",  # Tipo Descuento vacío para las filas de detalle
                "",  # Valor Préstamo vacío para las filas de detalle
                "",  # Saldo vacío para las filas de detalle
                f"Cuota {detalle.quota} - {detalle.date_discount.strftime('%Y-%m-%d')} - {detalle.balance_quota:.2f}"
            ]
            data.append(detail_data)

    # Crear la tabla y aplicar estilos
    table = Table(data, colWidths=[width/6.0]*6, style=table_style)
    elements.append(table)

    # Construir el PDF
    doc.build(elements)
    return response
