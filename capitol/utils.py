"""
Utilidades para generar gafetes y credenciales de tributos
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from io import BytesIO
from django.conf import settings
import os


def generar_gafete_pdf(tributo_info):
    """
    Genera un PDF con el gafete del tributo para imprimir
    
    Args:
        tributo_info: Instancia de TributoInfo
    
    Returns:
        BytesIO con el PDF generado
    """
    buffer = BytesIO()
    
    # Tamaño del gafete (10cm x 15cm - formato badge estándar)
    ancho = 10 * cm
    alto = 15 * cm
    
    # Crear canvas
    c = canvas.Canvas(buffer, pagesize=(ancho, alto))
    
    # Colores del tema Hunger Games
    color_primary = HexColor('#2c3e50')
    color_secondary = HexColor('#e74c3c')
    color_gold = HexColor('#f39c12')
    
    # Fondo con gradiente simulado (barras)
    c.setFillColor(color_primary)
    c.rect(0, alto - 3*cm, ancho, 3*cm, fill=1, stroke=0)
    
    # Logo o título
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ancho/2, alto - 1.5*cm, "UNPA CODING GAMES")
    
    c.setFont("Helvetica", 10)
    c.drawCentredString(ancho/2, alto - 2*cm, "Los Juegos del Hambre")
    
    # Distrito (badge)
    c.setFillColor(color_secondary)
    distrito_x = ancho - 2*cm
    distrito_y = alto - 2.5*cm
    c.circle(distrito_x, distrito_y, 0.8*cm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(distrito_x, distrito_y - 0.3*cm, str(tributo_info.distrito))
    c.setFont("Helvetica", 8)
    c.drawCentredString(distrito_x, distrito_y - 0.7*cm, "DISTRITO")
    
    # Foto del tributo (si existe)
    foto_y = alto - 7*cm
    if tributo_info.personaje.foto and os.path.exists(tributo_info.personaje.foto.path):
        try:
            foto = ImageReader(tributo_info.personaje.foto.path)
            # Foto circular simulada con rectángulo redondeado
            c.drawImage(foto, ancho/2 - 1.5*cm, foto_y, width=3*cm, height=3*cm, 
                       preserveAspectRatio=True, mask='auto')
        except:
            # Si hay error al cargar la foto, mostrar placeholder
            c.setFillColor(color_primary)
            c.rect(ancho/2 - 1.5*cm, foto_y, 3*cm, 3*cm, fill=1, stroke=0)
            c.setFillColorRGB(1, 1, 1)
            c.setFont("Helvetica-Bold", 40)
            c.drawCentredString(ancho/2, foto_y + 1.2*cm, "👤")
    else:
        # Placeholder
        c.setFillColor(color_primary)
        c.rect(ancho/2 - 1.5*cm, foto_y, 3*cm, 3*cm, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 40)
        c.drawCentredString(ancho/2, foto_y + 1.2*cm, "👤")
    
    # Información del tributo
    info_y = foto_y - 1*cm
    c.setFillColor(color_primary)
    c.setFont("Helvetica-Bold", 12)
    nombre_completo = tributo_info.personaje.get_full_name()
    c.drawCentredString(ancho/2, info_y, nombre_completo.upper())
    
    info_y -= 0.6*cm
    c.setFont("Helvetica", 9)
    c.drawCentredString(ancho/2, info_y, tributo_info.get_tipo_display())
    
    # Código del tributo
    info_y -= 0.8*cm
    c.setFillColor(color_gold)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(ancho/2, info_y, tributo_info.codigo_tributo)
    
    # Nivel
    info_y -= 0.6*cm
    c.setFillColor(color_primary)
    c.setFont("Helvetica", 8)
    nivel_text = f"Nivel: {tributo_info.get_nivel_display()}"
    c.drawCentredString(ancho/2, info_y, nivel_text)
    
    # QR Code
    qr_y = 2.5*cm
    if tributo_info.qr_code and os.path.exists(tributo_info.qr_code.path):
        try:
            qr = ImageReader(tributo_info.qr_code.path)
            qr_size = 3*cm
            c.drawImage(qr, ancho/2 - qr_size/2, qr_y, width=qr_size, height=qr_size)
        except:
            pass
    
    # Texto debajo del QR
    c.setFont("Helvetica", 7)
    c.setFillColor(color_primary)
    c.drawCentredString(ancho/2, qr_y - 0.4*cm, "Escanea para acreditar")
    
    # Instrucciones al reverso (segunda página)
    c.showPage()
    
    # Reverso del gafete
    c.setFillColor(color_primary)
    c.rect(0, alto - 2*cm, ancho, 2*cm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(ancho/2, alto - 1.2*cm, "INSTRUCCIONES")
    
    # Instrucciones
    instrucciones = [
        "1. Presenta este gafete al llegar a la sede",
        "2. El vigilante escaneará tu código QR",
        "3. Una vez acreditado, accede a la sala de PCs",
        "4. Siéntate en cualquier terminal disponible",
        "5. La webcam escaneará tu QR automáticamente",
        "6. Accederás a tu dashboard para competir",
        "",
        "¡Que los juegos comiencen! 🔥",
    ]
    
    c.setFillColor(color_primary)
    c.setFont("Helvetica", 8)
    y_pos = alto - 3*cm
    for linea in instrucciones:
        c.drawString(1*cm, y_pos, linea)
        y_pos -= 0.5*cm
    
    # Información de contacto
    c.setFont("Helvetica-Bold", 7)
    c.drawString(1*cm, 2*cm, "CONTACTO:")
    c.setFont("Helvetica", 7)
    c.drawString(1*cm, 1.6*cm, "Email: nicobutter@gmail.com")
    c.drawString(1*cm, 1.3*cm, "UNPA - Universidad Nacional de la Patagonia Austral")
    
    # Finalizar PDF
    c.save()
    
    buffer.seek(0)
    return buffer


def generar_gafete_html(tributo_info):
    """
    Genera HTML del gafete para visualización web
    
    Args:
        tributo_info: Instancia de TributoInfo
    
    Returns:
        String con HTML del gafete
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Gafete - {tributo_info.personaje.get_full_name()}</title>
        <style>
            @page {{
                size: 10cm 15cm;
                margin: 0;
            }}
            
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}
            
            .gafete {{
                width: 10cm;
                height: 15cm;
                background: white;
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            .header {{
                background: linear-gradient(135deg, #2c3e50, #34495e);
                color: white;
                padding: 1cm 0;
                text-align: center;
            }}
            
            .header h1 {{
                margin: 0;
                font-size: 16pt;
                font-weight: bold;
            }}
            
            .header p {{
                margin: 5px 0 0 0;
                font-size: 10pt;
            }}
            
            .distrito-badge {{
                position: absolute;
                top: 1.5cm;
                right: 1cm;
                background: #e74c3c;
                color: white;
                width: 1.6cm;
                height: 1.6cm;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            
            .distrito-numero {{
                font-size: 20pt;
                font-weight: bold;
                line-height: 1;
            }}
            
            .distrito-label {{
                font-size: 8pt;
                margin-top: 2px;
            }}
            
            .foto {{
                width: 3cm;
                height: 3cm;
                margin: 0.5cm auto;
                background: #ecf0f1;
                border-radius: 8px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .foto img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
            
            .foto-placeholder {{
                font-size: 48pt;
            }}
            
            .info {{
                text-align: center;
                padding: 0.5cm;
            }}
            
            .nombre {{
                font-size: 12pt;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 0.3cm;
                text-transform: uppercase;
            }}
            
            .tipo {{
                font-size: 9pt;
                color: #7f8c8d;
                margin-bottom: 0.5cm;
            }}
            
            .codigo {{
                font-size: 14pt;
                font-weight: bold;
                color: #f39c12;
                margin-bottom: 0.3cm;
            }}
            
            .nivel {{
                font-size: 8pt;
                color: #34495e;
            }}
            
            .qr-container {{
                text-align: center;
                margin-top: 0.5cm;
            }}
            
            .qr-container img {{
                width: 3cm;
                height: 3cm;
            }}
            
            .qr-label {{
                font-size: 7pt;
                color: #7f8c8d;
                margin-top: 5px;
            }}
            
            @media print {{
                .gafete {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="gafete">
            <div class="header">
                <h1>UNPA CODING GAMES</h1>
                <p>Los Juegos del Hambre</p>
            </div>
            
            <div class="distrito-badge">
                <div class="distrito-numero">{tributo_info.distrito}</div>
                <div class="distrito-label">DISTRITO</div>
            </div>
            
            <div class="foto">
                {'<img src="' + tributo_info.personaje.foto.url + '" alt="Foto">' if tributo_info.personaje.foto else '<div class="foto-placeholder">👤</div>'}
            </div>
            
            <div class="info">
                <div class="nombre">{tributo_info.personaje.get_full_name()}</div>
                <div class="tipo">{tributo_info.get_tipo_display()}</div>
                <div class="codigo">{tributo_info.codigo_tributo}</div>
                <div class="nivel">Nivel: {tributo_info.get_nivel_display()}</div>
            </div>
            
            <div class="qr-container">
                {'<img src="' + tributo_info.qr_code.url + '" alt="QR Code">' if tributo_info.qr_code else '<p>QR no disponible</p>'}
                <div class="qr-label">Escanea para acreditar</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html
