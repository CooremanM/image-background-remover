import os
from PIL import Image
from rembg import remove

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_image(image_path):
    with open(image_path, "rb") as f:
        input_data = f.read()

    # Remover fondo
    output_data = remove(input_data)

    # Guardar temporalmente como PNG con transparencia
    temp_path = os.path.join(OUTPUT_FOLDER, "temp.png")
    with open(temp_path, "wb") as out:
        out.write(output_data)

    # Abrir imagen manteniendo transparencia
    img = Image.open(temp_path).convert("RGBA")

    # Redimensionar manteniendo proporción
    img.thumbnail((1000, 1000))

    # Crear fondo blanco de 1000x1000
    final_img = Image.new("RGB", (1000, 1000), (255, 255, 255))

    # Centrar imagen
    x = (1000 - img.width) // 2
    y = (1000 - img.height) // 2

    # Pegar usando transparencia como máscara
    final_img.paste(img, (x, y), img)

    # Nombre de salida
    output_name = os.path.splitext(os.path.basename(image_path))[0] + ".jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    # Guardar como JPG
    final_img.save(output_path, "JPEG", quality=95)

    # Eliminar temporal
    os.remove(temp_path)

def process_folder():
    for file in os.listdir(INPUT_FOLDER):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Procesando: {file}")
            process_image(os.path.join(INPUT_FOLDER, file))

if __name__ == "__main__":
    process_folder()
    print("Procesamiento completo.")
