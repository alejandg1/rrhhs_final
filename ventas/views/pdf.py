from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from ventas.models import Cabecera, Detalle


def generar_pdf(request, factura_id):
    # Seleccionar la factura específica por ID
    cabecera = Cabecera.objects.get(id=factura_id)
    detalles = Detalle.objects.filter(cabecera=cabecera)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{cabecera.id}.pdf"'

    buffer = response
    # Define margenes para el documento
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    width, height = letter
    flowables = []

    # Datos de la cabecera de la factura
    header_data = [
        ['Factura No:', str(cabecera.id)],
        ['Cliente:',
            f"{cabecera.client.first_name} {cabecera.client.last_name}"],
        ['Fecha:', cabecera.date.strftime('%d/%m/%Y')],
    ]

    # Estilo para la cabecera de la factura
    header_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('SIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ])
    header_table = Table(header_data, colWidths=[120, 400], style=header_style)
    flowables.append(header_table)
    flowables.append(Spacer(1, 20))

    # Encabezados de la tabla de detalles de la factura
    detail_headers = ['Producto', 'Cantidad', 'P/U', 'Subtotal']

    # Datos de los detalles de la factura
    detail_data = [detail_headers] + [
        [detalle.product.name, detalle.quantity,
            f"{detalle.unitprice:.2f}", f"{detalle.subtotal:.2f}"]
        for detalle in detalles
    ]

    # Estilo para la tabla de detalles de la factura
    detail_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('SIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    detail_table = Table(detail_data, colWidths=[
                         None, None, 60, 60], style=detail_style)
    flowables.append(detail_table)

    # Totales de la factura
    totals_data = [
        ['IVA', f"{cabecera.iva:.2f}"],
        ['TOTAL', f"{cabecera.total:.2f}"],
    ]

    # Estilo para la tabla de totales
    totals_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('SIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ])
    totals_table = Table(totals_data, colWidths=[
                         None, 100], style=totals_style)
    flowables.append(Spacer(1, 20))
    flowables.append(totals_table)

    doc.build(flowables)

    return response
