import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from rembg import remove
from PIL import Image, ImageTk
import os


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Toolkit 🧼")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.image_path = []

        # Estilo barra progreso
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "TProgressbar",
            troughcolor="#333333",
            background="#00cc66",
            bordercolor="#1e1e1e",
            lightcolor="#00cc66",
            darkcolor="#00cc66"
        )

        # Carpeta de salida
        self.output_folder = os.path.join(os.getcwd(), "output")
        os.makedirs(self.output_folder, exist_ok=True)

        # Título
        self.title = tk.Label(
            root,
            text="🧼 Image Toolkit Pro",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        self.title.pack(pady=10)

        # Texto comercial
        self.description = tk.Label(
            root,
            text=(
                "Quitar fondo • Ampliar imagen 1000x1000 • Convertidor\n"
                "Optimizado para tu tienda nuebe 🛒"
            ),
            font=("Arial", 10),
            fg="white",
            bg="#1e1e1e",
            justify="center"
        )
        self.description.pack(pady=5)

        # Botón seleccionar imágenes
        self.btn_select = tk.Button(
            root,
            text="📁 Seleccionar Imágenes",
            command=self.select_image,
            width=28,
            height=2,
            bg="#333333",
            fg="white",
            activebackground="#555555",
            activeforeground="white"
        )
        self.btn_select.pack(pady=5)

        # Botón seleccionar carpeta
        self.btn_folder = tk.Button(
            root,
            text="📂 Seleccionar Carpeta",
            command=self.select_folder,
            width=28,
            height=2,
            bg="#333333",
            fg="white",
            activebackground="#555555",
            activeforeground="white"
        )
        self.btn_folder.pack(pady=5)

        # Estado selección
        self.path_label = tk.Label(
            root,
            text="Ninguna imagen seleccionada",
            wraplength=500,
            fg="white",
            bg="#1e1e1e"
        )
        self.path_label.pack(pady=5)

        # Vista previa
        self.preview_label = tk.Label(
            root,
            bg="#1e1e1e"
        )
        self.preview_label.pack(pady=10)

        # Botón procesar
        self.btn_process = tk.Button(
            root,
            text="🧼 Procesar imágenes",
            command=self.process_image,
            width=30,
            height=2,
            bg="#00aa55",
            fg="white",
            activebackground="#00cc66",
            activeforeground="white"
        )
        self.btn_process.pack(pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        # Estado general
        self.status = tk.Label(
            root,
            text="",
            fg="#00ff99",
            bg="#1e1e1e"
        )
        self.status.pack(pady=5)

        # Firma
        self.footer = tk.Label(
            root,
            text="by Maico Cooreman",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 11, "bold")
        )
        self.footer.pack(side="bottom", pady=10)

    def show_preview(self):
        if self.image_path:
            first_image = Image.open(self.image_path[0])
            first_image.thumbnail((200, 200))

            preview = ImageTk.PhotoImage(first_image)

            self.preview_label.config(image=preview)
            self.preview_label.image = preview

    def select_image(self):
        self.image_path = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp")]
        )

        if self.image_path:
            self.path_label.config(
                text=f"{len(self.image_path)} imágenes seleccionadas"
            )
            self.status.config(text="Imágenes cargadas ✔️")
            self.show_preview()

    def select_folder(self):
        folder_selected = filedialog.askdirectory(
            title="Seleccionar carpeta con imágenes"
        )

        if not folder_selected:
            return

        supported_formats = (".png", ".jpg", ".jpeg", ".webp")

        self.image_path = [
            os.path.join(folder_selected, file)
            for file in os.listdir(folder_selected)
            if file.lower().endswith(supported_formats)
        ]

        if self.image_path:
            self.path_label.config(
                text=f"{len(self.image_path)} imágenes cargadas desde carpeta"
            )
            self.status.config(text="Carpeta cargada ✔️")
            self.show_preview()

        else:
            messagebox.showwarning(
                "Sin imágenes",
                "No se encontraron imágenes compatibles en la carpeta"
            )

    def process_image(self):
        if not self.image_path:
            messagebox.showwarning(
                "Atención",
                "Primero seleccioná imágenes o carpeta"
            )
            return

        try:
            total = len(self.image_path)
            self.progress["maximum"] = total
            self.progress["value"] = 0

            self.status.config(text="Procesando... 🧠🧼")
            self.root.update()

            for i, img_path in enumerate(self.image_path, start=1):
                input_image = Image.open(img_path)

                output_image = remove(input_image)
                rgba_image = output_image.convert("RGBA")

                background = Image.new(
                    "RGB",
                    (1000, 1000),
                    (255, 255, 255)
                )

                rgba_image.thumbnail((1000, 1000))

                x = (1000 - rgba_image.width) // 2
                y = (1000 - rgba_image.height) // 2

                background.paste(
                    rgba_image,
                    (x, y),
                    rgba_image
                )

                filename = os.path.splitext(
                    os.path.basename(img_path)
                )[0]

                save_path = os.path.join(
                    self.output_folder,
                    f"{filename}_no_bg.jpg"
                )

                background.save(
                    save_path,
                    "JPEG",
                    quality=95
                )

                self.progress["value"] = i
                self.status.config(
                    text=f"Procesando {i}/{total}... 🧼"
                )
                self.root.update()

            self.status.config(
                text="Listo ✔️ Todo procesado en carpeta output"
            )

            messagebox.showinfo(
                "Éxito",
                f"Imágenes procesadas correctamente\nGuardadas en:\n{self.output_folder}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error ❌")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
