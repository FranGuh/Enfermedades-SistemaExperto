import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class BusquedaSintoma:
    def __init__(self, root):
        self.root = root
        self.root.title("Busqueda por Sintomas")
        self.root.geometry("1600x800")
        
        # Título
        title = tk.Label(root, text="Busqueda-Sintoma", font=("Helvetica", 16))
        title.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10)

        # Combobox para seleccionar Enfermedad
        tk.Label(main_frame, text="Selecciona Sintoma:").grid(row=0, column=0, padx=5, pady=5)
        self.enfermedad_cb = ttk.Combobox(main_frame)
        self.enfermedad_cb.grid(row=0, column=1, padx=5, pady=5)

        # Imagen de la enfermedad seleccionada
        self.image_label = tk.Label(main_frame)
        self.image_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Combobox para seleccionar Síntoma
        #tk.Label(main_frame, text="Selecciona Síntoma:").grid(row=2, column=0, padx=5, pady=5)
        #self.sintoma_cb = ttk.Combobox(main_frame)
        #self.sintoma_cb.grid(row=2, column=1, padx=5, pady=5)

        # Input para el Peso (probabilidad)
        #tk.Label(main_frame, text="Peso (probabilidad %):").grid(row=3, column=0, padx=5, pady=5)
        #self.peso_entry = tk.Entry(main_frame)
        #self.peso_entry.grid(row=3, column=1, padx=5, pady=5)

        # Tabla para mostrar las relaciones
        self.relation_table = ttk.Treeview(root, columns=("Id_Sintoma", "Nombre_Sintoma"), show="headings")
        self.relation_table.heading("Id_Sintoma", text="ID Síntoma")
        self.relation_table.heading("Nombre_Sintoma", text="Nombre Síntoma")
        #self.relation_table.heading("Probabilidad", text="Imagen")
        self.relation_table.pack(pady=10)
        
        # Botón para añadir la relación
        add_button = tk.Button(main_frame, text="Añadir")
        add_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Botón para borrar las selecciones y los campos
        clear_button = tk.Button(main_frame, text="Borrar")
        clear_button.grid(row=5, column=0, columnspan=2, pady=10)

# Creación de la ventana
root = tk.Tk()
app = BusquedaSintoma(root)
root.mainloop()
