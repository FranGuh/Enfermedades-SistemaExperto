import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

class BusquedaSintoma:
    def __init__(self, root):
        self.root = root
        self.root.title("Busqueda por Sintomas")
        self.root.geometry("1600x800")
        
        # Conectar a la base de datos MySQL
        self.conn = mysql.connector.connect(
            host="localhost",        # Cambia al host de tu servidor
            user="root",             # Cambia al usuario de tu base de datos
            password="root",         # Cambia a la contraseña de tu base de datos
            database="Conocimiento"  # Cambia al nombre de tu base de datos
        )
        self.cursor = self.conn.cursor()

        # Obtener síntomas para el Combobox
        self.cursor.execute("SELECT Id_Sintoma, nombre, Imagen FROM Sintomas")
        self.sintomas = self.cursor.fetchall()
        
        # Mapear Id y Nombre de síntomas para el Combobox y la tabla
        self.sintoma_map = {sintoma[1]: sintoma for sintoma in self.sintomas}
        self.sintoma_nombres = [s[1] for s in self.sintomas]  # Lista de nombres para el Combobox

        # Título
        title = tk.Label(root, text="Busqueda-Sintoma", font=("Helvetica", 16))
        title.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10)

        # Combobox para seleccionar Síntoma
        tk.Label(main_frame, text="Selecciona Sintoma:").grid(row=0, column=0, padx=5, pady=5)
        self.sintoma_cb = ttk.Combobox(main_frame, values=self.sintoma_nombres)
        self.sintoma_cb.grid(row=0, column=1, padx=5, pady=5)
        self.sintoma_cb.bind("<<ComboboxSelected>>", self.mostrar_imagen_sintoma)
        self.sintoma_cb.bind("<KeyRelease>", self.filtrar_sintomas)  # Filtrado en tiempo real

        # Imagen del síntoma seleccionado
        self.image_label = tk.Label(main_frame)
        self.image_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Tabla para mostrar los síntomas seleccionados
        self.relation_table = ttk.Treeview(root, columns=("Id_Sintoma", "Nombre_Sintoma"), show="headings")
        self.relation_table.heading("Id_Sintoma", text="ID Síntoma")
        self.relation_table.heading("Nombre_Sintoma", text="Nombre Síntoma")
        self.relation_table.pack(pady=10)

        # Botón para añadir la relación
        add_button = tk.Button(main_frame, text="Añadir", command=self.añadir_sintoma)
        add_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Botón para borrar la selección de la tabla
        clear_button = tk.Button(main_frame, text="Borrar Selección", command=self.borrar_seleccion)
        clear_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Botón para ejecutar la inferencia
        inferencia_button = tk.Button(main_frame, text="Ejecutar Inferencia", command=self.ejecutar_inferencia)
        inferencia_button.grid(row=6, column=0, columnspan=2, pady=10)

    def filtrar_sintomas(self, event):
        # Filtrar opciones del Combobox según el texto ingresado
        typed_text = self.sintoma_cb.get().lower()
        if typed_text == '':
            # Mostrar todas las opciones si el campo está vacío
            self.sintoma_cb['values'] = self.sintoma_nombres
        else:
            # Filtrar opciones que contengan el texto ingresado
            filtered = [s for s in self.sintoma_nombres if typed_text in s.lower()]
            self.sintoma_cb['values'] = filtered

    def mostrar_imagen_sintoma(self, event):
        # Obtener el síntoma seleccionado
        sintoma_nombre = self.sintoma_cb.get()
        sintoma_data = self.sintoma_map.get(sintoma_nombre)

        if sintoma_data:
            image_path = sintoma_data[2]  # Ruta de la imagen
            try:
                image = Image.open(image_path)
                image = image.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def añadir_sintoma(self):
        # Obtener el síntoma seleccionado
        sintoma_nombre = self.sintoma_cb.get()
        sintoma_data = self.sintoma_map.get(sintoma_nombre)

        if sintoma_data:
            # Verificar si el síntoma ya está en la tabla
            for item in self.relation_table.get_children():
                if self.relation_table.item(item, "values")[0] == str(sintoma_data[0]):
                    messagebox.showinfo("Información", "Este síntoma ya está en la tabla.")
                    return
            # Añadir el síntoma a la tabla
            self.relation_table.insert("", "end", values=(sintoma_data[0], sintoma_data[1]))

    def borrar_seleccion(self):
        # Borrar el elemento seleccionado en la tabla
        selected_item = self.relation_table.selection()
        if selected_item:
            for item in selected_item:
                self.relation_table.delete(item)
        else:
            messagebox.showinfo("Información", "Seleccione un síntoma en la tabla para eliminarlo.")

    def ejecutar_inferencia(self):
        # Obtener IDs de los síntomas seleccionados
        id_sintomas = [int(self.relation_table.item(item, "values")[0]) for item in self.relation_table.get_children()]

        if not id_sintomas:
            messagebox.showinfo("Información", "Seleccione al menos un síntoma para ejecutar la inferencia.")
            return

        try:
            # Actualizar bandera = 1 en la tabla relacion donde id_sintoma coincide
            update_query = "UPDATE relacion SET bandera = 1 WHERE id_sintoma = %s"
            for id_sintoma in id_sintomas:
                self.cursor.execute(update_query, (id_sintoma,))
            self.conn.commit()

            # Consulta para obtener las probabilidades donde bandera = 1
            consulta_query = """
                SELECT Id_enfermedad, SUM(probabilidad) as total_probabilidad
                FROM relacion
                WHERE bandera = 1
                GROUP BY Id_enfermedad
                ORDER BY total_probabilidad DESC
                LIMIT 5
            """
            self.cursor.execute(consulta_query)
            resultados = self.cursor.fetchall()

            # Obtener nombres de síntomas seleccionados para la justificación
            sintoma_nombres_query = "SELECT nombre FROM Sintomas WHERE Id_Sintoma IN (%s)" % ",".join(map(str, id_sintomas))
            self.cursor.execute(sintoma_nombres_query)
            sintomas_nombres = [row[0] for row in self.cursor.fetchall()]
            sintomas_texto = ", ".join(sintomas_nombres)

            # Generar mensaje con nombres de enfermedades y cálculo de porcentajes
            mensaje = "Las 5 enfermedades más probables (de mayor a menor) son:\n\n"
            for enfermedad_id, probabilidad_acumulada in resultados:
                # Obtener datos de la enfermedad desde la tabla enfermedad
                enfermedad_query = "SELECT nombre, peso FROM enfermedad WHERE Id_enfermedad = %s"
                self.cursor.execute(enfermedad_query, (enfermedad_id,))
                enfermedad_data = self.cursor.fetchone()
                
                if enfermedad_data:
                    nombre_enfermedad, peso_enfermedad = enfermedad_data
                    porcentaje_probabilidad = (probabilidad_acumulada / peso_enfermedad) * 100

                    # Formatear mensaje para cada enfermedad
                    mensaje += f"Enfermedad: {nombre_enfermedad}\n"
                    mensaje += f" - Probabilidad estimada: {porcentaje_probabilidad:.2f}%\n\n"

            # Añadir justificación al final del mensaje
            mensaje += f"Justificación: Debido a que tienes los siguientes síntomas: {sintomas_texto}."

            # Muestra el mensaje con las enfermedades y su probabilidad calculada
            messagebox.showinfo("Inferencia", mensaje)

            # Devuelve bandera a 0 en la tabla relacion
            self.cursor.execute("UPDATE relacion SET bandera = 0")
            self.conn.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al ejecutar la inferencia: {err}")


# Creación de la ventana
root = tk.Tk()
app = BusquedaSintoma(root)
root.mainloop()
