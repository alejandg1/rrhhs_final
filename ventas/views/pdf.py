from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from ventas.models import Cabecera, Detalle


def generar_pdf(request):
    # Seleccionar la última factura creada
    cabecera = Cabecera.objects.last()
    if not cabecera:
        return HttpResponse("No hay facturas disponibles para imprimir.", status=400)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{cabecera.id}.pdf"'

    buffer = response
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    flowables = []

    # Datos de la cabecera de la factura
    header_data = [
        ['Cliente:',
            f"{cabecera.client.first_name} {cabecera.client.last_name}"],
        ['Fecha:', cabecera.date.strftime('%d/%m/%Y')],
        ['Factura No:', str(cabecera.id)],
    ]

    # Estilo para la cabecera de la factura
    header_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('SIZE', (0, 0), (-1, -1), 12),
    ])
    header_table = Table(header_data, style=header_style)
    flowables.append(header_table)
    flowables.append(Spacer(1, 12))

    # Encabezados de la tabla de detalles de la factura
    detail_headers = ['Producto', 'Cantidad', 'P/U', 'Subtotal']

    # Datos de los detalles de la factura
    detail_data = [detail_headers] + [
        [
            detalle.product.name,
            detalle.quantity,
            detalle.unitprice,
            detalle.subtotal
        ] for detalle in Detalle.objects.filter(cabecera=cabecera)
    ]

    # Estilo para la tabla de detalles de la factura
    detail_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('SIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    detail_table = Table(detail_data, style=detail_style)
    flowables.append(detail_table)

    # Totales de la factura
    totals_data = [
        ['IVA', cabecera.iva],
        ['TOTAL', cabecera.total],
    ]

    totals_table = Table(totals_data, colWidths=[
                         None, 100], style=detail_style)
    flowables.append(Spacer(1, 12))
    flowables.append(totals_table)

    doc.build(flowables)
    return response
