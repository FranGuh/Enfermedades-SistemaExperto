import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

class CuadroRelacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Cuadro-Relación")
        self.root.geometry("1600x800")
        
        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Conocimiento"
        )
        self.cursor = self.conn.cursor()

        # Título
        title = tk.Label(root, text="Cuadro-Relación", font=("Helvetica", 16))
        title.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10)

        # Combobox para seleccionar Enfermedad
        tk.Label(main_frame, text="Selecciona Enfermedad:").grid(row=0, column=0, padx=5, pady=5)
        self.enfermedad_cb = ttk.Combobox(main_frame)
        self.enfermedad_cb.grid(row=0, column=1, padx=5, pady=5)
        self.enfermedad_cb.bind("<<ComboboxSelected>>", self.load_image_and_relations)  # Sin llamar directamente a load_relations()

        self.load_enfermedades()

        # Imagen de la enfermedad seleccionada
        self.image_label = tk.Label(main_frame)
        self.image_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Combobox para seleccionar Síntoma con búsqueda
        tk.Label(main_frame, text="Selecciona Síntoma:").grid(row=2, column=0, padx=5, pady=5)
        self.sintoma_cb = ttk.Combobox(main_frame)
        self.sintoma_cb.grid(row=2, column=1, padx=5, pady=5)
        self.sintoma_cb.bind("<KeyRelease>", self.filter_sintomas)  # Evento de búsqueda en tiempo real
        self.load_sintomas()

        # Input para el Peso (probabilidad)
        tk.Label(main_frame, text="Peso (probabilidad %):").grid(row=3, column=0, padx=5, pady=5)
        self.peso_entry = tk.Entry(main_frame)
        self.peso_entry.grid(row=3, column=1, padx=5, pady=5)

        # Tabla para mostrar las relaciones
        self.relation_table = ttk.Treeview(root, columns=("Id_Sintoma", "Nombre_Sintoma", "Probabilidad"), show="headings")
        self.relation_table.heading("Id_Sintoma", text="ID Síntoma")
        self.relation_table.heading("Nombre_Sintoma", text="Nombre Síntoma")
        self.relation_table.heading("Probabilidad", text="Probabilidad (%)")
        self.relation_table.pack(pady=10)
        self.relation_table.bind("<Double-1>", self.confirm_delete_relation)
        
        # Botón para añadir la relación
        add_button = tk.Button(main_frame, text="Añadir", command=self.add_relation, compound="left")
        add_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Botón para borrar las selecciones y los campos
        clear_button = tk.Button(main_frame, text="Borrar", command=self.clear_fields, compound="left")
        clear_button.grid(row=5, column=0, columnspan=2, pady=10)

    def load_enfermedades(self):
        """Carga las enfermedades desde la tabla 'Enfermedad' en el combobox."""
        self.cursor.execute("SELECT Id_Enfermedad, Nombre, Imagen FROM Enfermedad")
        enfermedades = self.cursor.fetchall()
        self.enfermedad_cb['values'] = [f"{row[0]} - {row[1]}" for row in enfermedades]
        self.enfermedades_data = {row[0]: row[2] for row in enfermedades}  # Guardar las imágenes por ID

    def load_sintomas(self):
        """Carga los síntomas desde la tabla 'Sintomas' en el combobox."""
        self.cursor.execute("SELECT Id_Sintoma, Nombre FROM Sintomas")
        self.sintomas = self.cursor.fetchall()
        self.sintoma_cb['values'] = [f"{row[0]} - {row[1]}" for row in self.sintomas]

    def filter_sintomas(self, event):
        """Filtra los síntomas en el combobox según el texto ingresado."""
        search_term = self.sintoma_cb.get().lower()
        filtered_sintomas = [f"{row[0]} - {row[1]}" for row in self.sintomas if search_term in row[1].lower()]
        self.sintoma_cb['values'] = filtered_sintomas
        if filtered_sintomas:
            self.sintoma_cb.event_generate("<Down>")

    def load_image_and_relations(self, event):
        """Muestra la imagen de la enfermedad seleccionada y carga las relaciones correspondientes."""
        enfermedad_selec = self.enfermedad_cb.get()
        if enfermedad_selec:
            id_enfermedad = int(enfermedad_selec.split(" - ")[0])

            # Cargar y mostrar la imagen
            imagen_path = self.enfermedades_data.get(id_enfermedad)
            if imagen_path:
                img = Image.open(imagen_path)
                img = img.resize((150, 150), Image.LANCZOS)  # Redimensionar la imagen
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Guardar referencia para que no se borre

            # Cargar las relaciones de la enfermedad
            self.load_relations(id_enfermedad)

    def load_relations(self, id_enfermedad):
        """Carga las relaciones de una enfermedad en la tabla."""
        query = """
        SELECT r.Id_Sintoma, s.Nombre, r.Probabilidad 
        FROM Relacion r 
        JOIN Sintomas s ON r.Id_Sintoma = s.Id_Sintoma 
        WHERE r.Id_Enfermedad = %s
        """
        self.cursor.execute(query, (id_enfermedad,))
        relaciones = self.cursor.fetchall()

        # Limpiar la tabla
        for row in self.relation_table.get_children():
            self.relation_table.delete(row)

        # Añadir las nuevas relaciones
        for relacion in relaciones:
            self.relation_table.insert("", "end", values=relacion)

    def add_relation(self):
        """Añade la relación a la tabla Relacion."""
        enfermedad_selec = self.enfermedad_cb.get()
        sintoma_selec = self.sintoma_cb.get()
        peso = self.peso_entry.get()

        if enfermedad_selec and sintoma_selec and peso:
            try:
                id_enfermedad = int(enfermedad_selec.split(" - ")[0])
                id_sintoma = int(sintoma_selec.split(" - ")[0])
                peso = int(peso)

                query = """
                INSERT INTO Relacion (Id_Enfermedad, Id_Sintoma, Probabilidad)
                VALUES (%s, %s, %s)
                """
                self.cursor.execute(query, (id_enfermedad, id_sintoma, peso))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Relación añadida exitosamente")
                
                # Recargar las relaciones
                self.load_relations(id_enfermedad)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo añadir la relación: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos")

    def confirm_delete_relation(self, event):
        """Confirma si se desea eliminar una relación seleccionada."""
        selected_item = self.relation_table.selection()
        if selected_item:
            values = self.relation_table.item(selected_item, "values")
            id_sintoma = values[0]
            id_enfermedad = int(self.enfermedad_cb.get().split(" - ")[0])
            
            response = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta relación?")
            if response:
                try:
                    query = "DELETE FROM Relacion WHERE Id_Enfermedad = %s AND Id_Sintoma = %s"
                    self.cursor.execute(query, (id_enfermedad, id_sintoma))
                    self.conn.commit()
                    messagebox.showinfo("Éxito", "Relación eliminada exitosamente")
                    
                    # Recargar las relaciones
                    self.load_relations(id_enfermedad)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la relación: {e}")

    def __del__(self):
        """Cierra la conexión cuando se destruye la clase."""
        self.conn.close()
        
    def clear_fields(self):
        """Borra las selecciones y limpia los campos de entrada."""
        self.enfermedad_cb.set("")
        self.sintoma_cb.set("")
        self.peso_entry.delete(0, tk.END)

# Creación de la ventana
root = tk.Tk()
app = CuadroRelacion(root)
root.mainloop()
