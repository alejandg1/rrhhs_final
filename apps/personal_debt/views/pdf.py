from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from apps.personal_debt.models import Credit, CreditsDetail


def generar_pdf_prestamo(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prestamos.pdf"'

    buffer = response
    # Define margenes para el documento
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    width, height = letter

    elements = []

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

    encabezados = ('ID Crédito', 'Empleado', 'Tipo Descuento',
                   'Valor Préstamo', 'Cuota', 'Fecha', 'Saldo')
    data = [encabezados]

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

    for credito in Credit.objects.all():
        credit_data = [
            str(credito.id),
            f"{credito.employee.last_name} {credito.employee.firts_name}",
            credito.item.description.split(" ")[0],  # Ejemplo: 'PRESTAMO'
            "{:.2f}".format(credito.loan_val),
            "", "",  # Cuotas y fechas estarán vacías en esta fila
            "{:.2f}".format(credito.balance),  # Saldo del crédito
        ]
        data.append(credit_data)

        # Agregar las filas de los CreditsDetail asociados
        for detalle in CreditsDetail.objects.filter(credit=credito).order_by('quota'):
            detail_data = [
                "", "", "", "",  # Las primeras cuatro columnas estarán vacías para los detalles
                f"Cuota {detalle.quota}",
                detalle.date_discount.strftime('%Y-%m-%d'),
                "{:.2f}".format(detalle.balance_quota),  # Saldo de la cuota
            ]
            data.append(detail_data)

    table = Table(data, colWidths=[width/7.0]*7, style=table_style)
    elements.append(table)

    doc.build(elements)
    return response
