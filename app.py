import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image
import os


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Toolkit 🧼")
        self.root.geometry("650x450")
        self.root.resizable(False, False)

        self.image_path = []

        # Título
        self.title = tk.Label(
            root,
            text="🧼 Image Toolkit Pro",
            font=("Arial", 16, "bold")
        )
        self.title.pack(pady=10)

        # Texto de venta
        self.description = tk.Label(
            root,
            text=(
                "Quitar fondo • Ampliar imagen 1000x1000 • Convertidor\n"
                "Optimizado para tu tienda nuebe 🛒"
            ),
            font=("Arial", 10),
            fg="black",
            justify="center"
        )
        self.description.pack(pady=5)

        # Selección de imágenes
        self.btn_select = tk.Button(
            root,
            text="📁 Seleccionar Imágenes",
            command=self.select_image,
            width=28,
            height=2
        )
        self.btn_select.pack(pady=10)

        # Estado selección
        self.path_label = tk.Label(
            root,
            text="Ninguna imagen seleccionada",
            wraplength=450
        )
        self.path_label.pack(pady=5)

        # Procesar
        self.btn_process = tk.Button(
            root,
            text="🧼 Procesar imágenes",
            command=self.process_image,
            width=30,
            height=2,
            bg="#4CAF50",
            fg="white"
        )
        self.btn_process.pack(pady=10)

        # Estado
        self.status = tk.Label(
            root,
            text="",
            fg="blue"
        )
        self.status.pack(pady=5)

        # Firma
        self.footer = tk.Label(
            root,
            text="by Maico Cooreman",
            fg="#111111",
            font=("Arial", 11, "bold")
        )
        self.footer.pack(side="bottom", pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
        )

        if self.image_path:
            self.path_label.config(text=f"{len(self.image_path)} imágenes seleccionadas")
            self.status.config(text="Imágenes cargadas ✔️")

    def process_image(self):
        if not self.image_path:
            messagebox.showwarning("Atención", "Primero seleccioná imágenes")
            return

        try:
            self.status.config(text="Procesando... 🧠🧼")
            self.root.update()

            total = len(self.image_path)

            for i, img_path in enumerate(self.image_path, start=1):

                # abrir imagen
                input_image = Image.open(img_path)

                # quitar fondo
                output_image = remove(input_image)

                # convertir a RGBA
                rgba_image = output_image.convert("RGBA")

                # fondo blanco
                background = Image.new("RGB", (1000, 1000), (255, 255, 255))

                # redimensionar manteniendo imagen
                rgba_image.thumbnail((1000, 1000))

                # centrar imagen
                x = (1000 - rgba_image.width) // 2
                y = (1000 - rgba_image.height) // 2

                background.paste(rgba_image, (x, y), rgba_image)

                # guardar
                save_path = os.path.splitext(img_path)[0] + "_no_bg.jpg"
                background.save(save_path, "JPEG", quality=95)

                self.status.config(text=f"Procesando {i}/{total}... 🧼")
                self.root.update()

            self.status.config(text="Listo ✔️ Todo procesado")
            messagebox.showinfo("Éxito", "Imágenes procesadas correctamente")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error ❌")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
