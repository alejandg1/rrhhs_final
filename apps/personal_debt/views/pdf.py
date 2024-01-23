from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from ventas.models import Cabecera, Detalle


def generar_pdf_factura(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="facturas.pdf"'

    buffer = response
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
    title_table = Table([["Listado de Facturas"]],
                        colWidths=[width], style=title_style)
    elements.append(title_table)
    elements.append(Spacer(1, 20))

    encabezados = ('ID Factura', 'Cliente', 'Fecha',
                   'Subtotal', 'IVA', 'Total')
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

    # Suponiendo que deseas listar todas las facturas
    for cabecera in Cabecera.objects.all():
        factura_data = [
            str(cabecera.id),
            f"{cabecera.client.first_name} {cabecera.client.last_name}",
            cabecera.date.strftime('%Y-%m-%d'),
            f"{cabecera.subtotal:.2f}",
            f"{cabecera.iva:.2f}",
            f"{cabecera.total:.2f}"
        ]
        data.append(factura_data)

        # Agregar las filas de los Detalles asociados a la factura
        for detalle in Detalle.objects.filter(cabecera=cabecera).order_by('id'):
            detail_data = [
                "", "", "", "",  # Las primeras cuatro columnas estarán vacías para los detalles
                f"{detalle.product.name}",
                f"{detalle.quantity}",
                f"{detalle.unitprice:.2f}",
                f"{detalle.subtotal:.2f}"
            ]
            data.append(detail_data)
        # Agregar un espacio entre cada factura
        data.append([""] * 6)

    table = Table(data, colWidths=[width/6.0]*6, style=table_style)
    elements.append(table)

    doc.build(elements)
    return response
