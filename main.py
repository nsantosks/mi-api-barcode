import barcode
from barcode.writer import ImageWriter
from fastapi import FastAPI, Response
from io import BytesIO

# 1. Inicializar la aplicación FastAPI
app = FastAPI(
    title="API de Códigos de Barras",
    description="Una API simple para generar imágenes de códigos de barras.",
    version="1.0.0"
)

# 2. Definir el endpoint (la URL que generará el código)
@app.get("/generate-barcode/", tags=["Barcode Generator"])
def generate_barcode_endpoint(data: str, barcode_type: str = 'code128'):
    """
    Genera una imagen de código de barras.

    - **data**: El texto o número a codificar.
    - **barcode_type**: El tipo de código de barras (ej. code128, ean13, etc.).
    """
    try:
        # Buffer en memoria para no tener que guardar el archivo en disco
        buffer = BytesIO()

        # Obtener la clase del código de barras solicitado
        barcode_class = barcode.get_barcode_class(barcode_type)

        # Generar el código de barras como imagen SVG y escribirlo en el buffer
        # Usamos SVG porque es vectorial y escalable, pero PNG también es una opción.
        # Opciones del writer para controlar el tamaño y apariencia
        writer_options = {
            "module_width": 0.3, # Ancho de las barras
            "module_height": 10.0, # Altura de las barras
            "font_size": 8, # Tamaño del texto debajo
            "text_distance": 4.0, # Distancia entre las barras y el texto
            "quiet_zone": 2.0 # Margen en blanco a los lados
        }
        barcode_instance = barcode_class(data, writer=ImageWriter())
        barcode_instance.write(buffer, options=writer_options)

        # Mover el cursor del buffer al inicio para leer su contenido
        buffer.seek(0)

        # 3. Devolver la imagen como una respuesta HTTP
        return Response(content=buffer.getvalue(), media_type="image/png")

    except barcode.errors.BarcodeNotFoundError:
        return Response(content=f"Error: El tipo de código de barras '{barcode_type}' no es válido.", status_code=400)
    except Exception as e:
        return Response(content=f"Error interno del servidor: {e}", status_code=500)