import subprocess
import tkinter as tk
from tkinter import messagebox

class UsuarioInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz Usuario")
        self.center_window(400, 300)  # Tamaño de la ventana 400x300

        # Etiqueta de título
        title_label = tk.Label(root, text="Interfaz Usuario", font=("Helvetica", 16))
        title_label.pack(pady=20)

        # Botón para "Búsqueda por síntomas"
        btn_sintomas = tk.Button(root, text="Búsqueda por síntomas", command=self.abrir_busqueda_sintomas)
        btn_sintomas.pack(pady=10)

        # Botón para "Búsqueda por enfermedad"
        btn_enfermedad = tk.Button(root, text="Búsqueda por enfermedad", command=self.busqueda_enfermedad)
        btn_enfermedad.pack(pady=10)

        # Botón para "Regresar"
        btn_regresar = tk.Button(root, text="Regresar", command=self.root.destroy)
        btn_regresar.pack(pady=10)

    def center_window(self, width, height):
        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular posición x e y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Establecer tamaño y posición de la ventana
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def abrir_busqueda_sintomas(self):
        ejecutar_BusquedaSintoma()

    def busqueda_enfermedad(self):
        messagebox.showinfo("Funcionalidad no implementada", "Esta función aún no está disponible.")

def ejecutar_BusquedaSintoma():
    subprocess.run(["python", "BusquedaSintoma.py"])

def mostrar_interfaz_usuario():
    root = tk.Tk()
    app = UsuarioInterfaz(root)
    root.mainloop()