from django.http import HttpResponse
from reportlab.pdfgen import canvas
from ventas.models import Cabecera, Detalle


def generar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="facturas.pdf"'

    # Crear un objeto canvas de ReportLab
    p = canvas.Canvas(response)

    y = 800  # Posición inicial en el eje Y

    # Iterar sobre cada objeto Cabecera
    for cabecera in Cabecera.objects.all():
        p.drawString(100, y, f"Cabecera ID: {cabecera.id}")
        p.drawString(
            100, y-20, f"Cliente: {cabecera.client.first_name} {cabecera.client.last_name}")
        p.drawString(100, y-40, f"Fecha: {cabecera.date.strftime('%d/%m/%Y')}")
        p.drawString(100, y-60, f"Subtotal: {cabecera.subtotal}")
        p.drawString(100, y-80, f"Iva: {cabecera.iva}")
        p.drawString(100, y-100, f"Total: {cabecera.total}")
        y -= 120  # Espacio antes de los detalles

        # Iterar sobre cada objeto Detalle asociado con la Cabecera
        for detalle in Detalle.objects.filter(cabecera=cabecera):
            p.drawString(120, y, f"Producto: {detalle.product.name}")
            p.drawString(400, y, f"Cantidad: {detalle.quantity}")
            p.drawString(500, y, f"Precio Unitario: {detalle.unitprice}")
            p.drawString(700, y, f"Subtotal: {detalle.subtotal}")
            y -= 20

            # Verificar si se necesita una nueva página
            if y < 40:
                p.showPage()
                y = 800

        y -= 40  # Espacio adicional antes de la siguiente cabecera

        # Verificar si se necesita una nueva página
        if y < 40:
            p.showPage()
            y = 800

    p.showPage()
    p.save()

    return response
