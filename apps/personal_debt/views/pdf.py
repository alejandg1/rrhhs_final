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
                   'Valor Préstamo', 'Saldo')
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
        # Agregar la fila de cada Credit
        data.append([
            str(credito.id),
            credito.employee.get_full_name(),
            credito.item.description,
            str(credito.loan_val),
            str(credito.balance)
        ])

        # Agregar las filas de los CreditsDetail asociados
        for detalle in CreditsDetail.objects.filter(credit=credito):
            data.append([
                '',
                f'Cuota {detalle.quota}',
                detalle.date_discount.strftime('%Y-%m-%d'),
                '',
                str(detalle.balance_quota),
            ])

    # Crear la tabla y aplicar estilos
    table = Table(data, colWidths=[width/5.0]*5, style=table_style)
    elements.append(table)

    # Construir el PDF
    doc.build(elements)
    return response
