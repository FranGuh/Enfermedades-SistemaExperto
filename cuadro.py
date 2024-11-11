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
            user="roger",
            password="1234",
            database="Conocimiento3"
        )
        self.cursor = self.conn.cursor()

        # Título
        title = tk.Label(root, text="Cuadro-Relación", font=("Helvetica", 16))
        title.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10)

        # Combobox para seleccionar Deporte
        tk.Label(main_frame, text="Selecciona Deporte:").grid(row=0, column=0, padx=5, pady=5)
        self.deporte_cb = ttk.Combobox(main_frame)
        self.deporte_cb.grid(row=0, column=1, padx=5, pady=5)
        self.deporte_cb.bind("<<ComboboxSelected>>", self.load_image_and_relations)  # Sin llamar directamente a load_relations()

        self.load_deportes()

        # Imagen del deporte seleccionado
        self.image_label = tk.Label(main_frame)
        self.image_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Combobox para seleccionar actividad con búsqueda
        tk.Label(main_frame, text="Selecciona Actividad:").grid(row=2, column=0, padx=5, pady=5)
        self.actividad_cb = ttk.Combobox(main_frame)
        self.actividad_cb.grid(row=2, column=1, padx=5, pady=5)
        self.actividad_cb.bind("<KeyRelease>", self.filter_actividades)  # Evento de búsqueda en tiempo real
        self.load_actividades()

        # Input para el Peso (probabilidad)
        tk.Label(main_frame, text="Peso (probabilidad %):").grid(row=3, column=0, padx=5, pady=5)
        self.peso_entry = tk.Entry(main_frame)
        self.peso_entry.grid(row=3, column=1, padx=5, pady=5)

        # Tabla para mostrar las relaciones
        self.relation_table = ttk.Treeview(root, columns=("Id_Actividad", "Nombre_Actividad", "Probabilidad"), show="headings")
        self.relation_table.heading("Id_Actividad", text="ID Actividad")
        self.relation_table.heading("Nombre_Actividad", text="Nombre Actividad")
        self.relation_table.heading("Probabilidad", text="Probabilidad (%)")
        self.relation_table.pack(pady=10)
        self.relation_table.bind("<Double-1>", self.confirm_delete_relation)
        
        # Botón para añadir la relación
        add_button = tk.Button(main_frame, text="Añadir", command=self.add_relation, compound="left")
        add_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Botón para borrar las selecciones y los campos
        clear_button = tk.Button(main_frame, text="Borrar", command=self.clear_fields, compound="left")
        clear_button.grid(row=5, column=0, columnspan=2, pady=10)

    def load_deportes(self):
        """Carga los deportes desde la tabla 'Deporte' en el combobox."""
        self.cursor.execute("SELECT Id_Deporte, Nombre, Imagen FROM Deporte")
        deportes = self.cursor.fetchall()
        self.deporte_cb['values'] = [f"{row[0]} - {row[1]}" for row in deportes]
        self.deportes_data = {row[0]: row[2] for row in deportes}  # Guardar las imágenes por ID

    def load_actividades(self):
        """Carga las actividades desde la tabla 'Actividades' en el combobox."""
        self.cursor.execute("SELECT Id_Actividad, Nombre FROM Actividad")
        self.actividades = self.cursor.fetchall()
        self.actividad_cb['values'] = [f"{row[0]} - {row[1]}" for row in self.actividades]

    def filter_actividades(self, event):
        """Filtra los actividades en el combobox según el texto ingresado."""
        search_term = self.actividad_cb.get().lower()
        filtered_actividades = [f"{row[0]} - {row[1]}" for row in self.actividades if search_term in row[1].lower()]
        self.actividad_cb['values'] = filtered_actividades
        if filtered_actividades:
            self.actividad_cb.event_generate("<Down>")

    def load_image_and_relations(self, event):
        """Muestra la imagen del deporte seleccionado y carga las relaciones correspondientes."""
        deporte_selec = self.deporte_cb.get()
        if deporte_selec:
            id_deporte = int(deporte_selec.split(" - ")[0])

            # Cargar y mostrar la imagen
            imagen_path = self.deportes_data.get(id_deporte)
            if imagen_path:
                img = Image.open(imagen_path)
                img = img.resize((150, 150), Image.LANCZOS)  # Redimensionar la imagen
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Guardar referencia para que no se borre

            # Cargar las relaciones del deporte
            self.load_relations(id_deporte)

    def load_relations(self, id_deporte):
        """Carga las relaciones de un deporte en la tabla."""
        query = """
        SELECT r.Id_Actividad, s.Nombre, r.Probabilidad 
        FROM Relacion r 
        JOIN Actividad s ON r.Id_Actividad = s.Id_Actividad 
        WHERE r.Id_Deporte = %s
        """
        self.cursor.execute(query, (id_deporte,))
        relaciones = self.cursor.fetchall()

        # Limpiar la tabla
        for row in self.relation_table.get_children():
            self.relation_table.delete(row)

        # Añadir las nuevas relaciones
        for relacion in relaciones:
            self.relation_table.insert("", "end", values=relacion)

    def add_relation(self):
        """Añade la relación a la tabla Relacion."""
        deporte_selec = self.deporte_cb.get()
        actividad_selec = self.actividad_cb.get()
        peso = self.peso_entry.get()

        if deporte_selec and actividad_selec and peso:
            try:
                id_deporte = int(deporte_selec.split(" - ")[0])
                id_actividad = int(actividad_selec.split(" - ")[0])
                peso = int(peso)

                query = """
                INSERT INTO Relacion (Id_Deporte, Id_Actividad, Probabilidad)
                VALUES (%s, %s, %s)
                """
                self.cursor.execute(query, (id_deporte, id_actividad, peso))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Relación añadida exitosamente")
                
                # Recargar las relaciones
                self.load_relations(id_deporte)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo añadir la relación: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos")

    def confirm_delete_relation(self, event):
        """Confirma si se desea eliminar una relación seleccionada."""
        selected_item = self.relation_table.selection()
        if selected_item:
            values = self.relation_table.item(selected_item, "values")
            id_actividad = values[0]
            id_deporte = int(self.deporte_cb.get().split(" - ")[0])
            
            response = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta relación?")
            if response:
                try:
                    query = "DELETE FROM Relacion WHERE Id_Deporte = %s AND Id_Actividad = %s"
                    self.cursor.execute(query, (id_deporte, id_actividad))
                    self.conn.commit()
                    messagebox.showinfo("Éxito", "Relación eliminada exitosamente")
                    
                    # Recargar las relaciones
                    self.load_relations(id_deporte)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la relación: {e}")

    def __del__(self):
        """Cierra la conexión cuando se destruye la clase."""
        self.conn.close()
        
    def clear_fields(self):
        """Borra las selecciones y limpia los campos de entrada."""
        self.deporte_cb.set("")
        self.actividad_cb.set("")
        self.peso_entry.delete(0, tk.END)

# Creación de la ventana
root = tk.Tk()
app = CuadroRelacion(root)
root.mainloop()
