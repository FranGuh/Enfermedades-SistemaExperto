import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

class BusquedaActividad:
    def __init__(self, root):
        self.root = root
        self.root.title("Busqueda por Actividades")
        self.root.geometry("1600x800")
        
        # Conectar a la base de datos MySQL
        self.conn = mysql.connector.connect(
            host="localhost",        # Cambia al host de tu servidor
            user="roger",             # Cambia al usuario de tu base de datos
            password="1234",         # Cambia a la contraseña de tu base de datos
            database="Conocimiento3"  # Cambia al nombre de tu base de datos
        )
        self.cursor = self.conn.cursor()

        # Obtener síntomas para el Combobox
        self.cursor.execute("SELECT Id_Actividad, nombre, Imagen FROM Actividad")
        self.actividades = self.cursor.fetchall()
        
        # Mapear Id y Nombre de síntomas para el Combobox y la tabla
        self.actividad_map = {actividad[1]: actividad for actividad in self.actividades}
        self.actividad_nombres = [s[1] for s in self.actividades]  # Lista de nombres para el Combobox

        # Título
        title = tk.Label(root, text="Busqueda-Actividad", font=("Helvetica", 16))
        title.pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10)

        # Combobox para seleccionar Síntoma
        tk.Label(main_frame, text="Selecciona Actividad:").grid(row=0, column=0, padx=5, pady=5)
        self.actividad_cb = ttk.Combobox(main_frame, values=self.actividad_nombres)
        self.actividad_cb.grid(row=0, column=1, padx=5, pady=5)
        self.actividad_cb.bind("<<ComboboxSelected>>", self.mostrar_imagen_actividad)
        self.actividad_cb.bind("<KeyRelease>", self.filtrar_actividades)  # Filtrado en tiempo real

        # Imagen del síntoma seleccionado
        self.image_label = tk.Label(main_frame)
        self.image_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Tabla para mostrar los síntomas seleccionados
        self.relation_table = ttk.Treeview(root, columns=("Id_Actividad", "Nombre_Actividad"), show="headings")
        self.relation_table.heading("Id_Actividad", text="ID Actividad")
        self.relation_table.heading("Nombre_Actividad", text="Nombre Actividad")
        self.relation_table.pack(pady=10)

        # Botón para añadir la relación
        add_button = tk.Button(main_frame, text="Añadir", command=self.añadir_actividad)
        add_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Botón para borrar la selección de la tabla
        clear_button = tk.Button(main_frame, text="Borrar Selección", command=self.borrar_seleccion)
        clear_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Botón para ejecutar la inferencia
        inferencia_button = tk.Button(main_frame, text="Ejecutar Inferencia", command=self.ejecutar_inferencia)
        inferencia_button.grid(row=6, column=0, columnspan=2, pady=10)

    def filtrar_actividades(self, event):
        # Filtrar opciones del Combobox según el texto ingresado
        typed_text = self.actividad_cb.get().lower()
        if typed_text == '':
            # Mostrar todas las opciones si el campo está vacío
            self.actividad_cb['values'] = self.actividad_nombres
        else:
            # Filtrar opciones que contengan el texto ingresado
            filtered = [s for s in self.actividad_nombres if typed_text in s.lower()]
            self.actividad_cb['values'] = filtered

    def mostrar_imagen_actividad(self, event):
        # Obtener el síntoma seleccionado
        actividad_nombre = self.actividad_cb.get()
        actividad_data = self.actividad_map.get(actividad_nombre)

        if actividad_data:
            image_path = actividad_data[2]  # Ruta de la imagen
            try:
                image = Image.open(image_path)
                image = image.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def añadir_actividad(self):
        # Obtener el síntoma seleccionado
        actividad_nombre = self.actividad_cb.get()
        actividad_data = self.actividad_map.get(actividad_nombre)

        if actividad_data:
            # Verificar si el síntoma ya está en la tabla
            for item in self.relation_table.get_children():
                if self.relation_table.item(item, "values")[0] == str(actividad_data[0]):
                    messagebox.showinfo("Información", "Esta actividad ya está en la tabla.")
                    return
            # Añadir el síntoma a la tabla
            self.relation_table.insert("", "end", values=(actividad_data[0], actividad_data[1]))

    def borrar_seleccion(self):
        # Borrar el elemento seleccionado en la tabla
        selected_item = self.relation_table.selection()
        if selected_item:
            for item in selected_item:
                self.relation_table.delete(item)
        else:
            messagebox.showinfo("Información", "Seleccione una actividad en la tabla para eliminarlo.")

    def ejecutar_inferencia(self):
    # Obtener IDs de los síntomas seleccionados
        id_actividades = [int(self.relation_table.item(item, "values")[0]) for item in self.relation_table.get_children()]

        if not id_actividades:
            messagebox.showinfo("Información", "Seleccione al menos una actividad para ejecutar la inferencia.")
            return

        try:
            # Actualizar bandera = 1 en la tabla relacion donde id_actividad coincide
            update_query = "UPDATE relacion SET bandera = 1 WHERE id_actividad = %s"
            for id_actividad in id_actividades:
                self.cursor.execute(update_query, (id_actividad,))
            self.conn.commit()

            # Consulta para obtener las probabilidades donde bandera = 1
            consulta_query = """
                SELECT Id_Deporte, SUM(probabilidad) as total_probabilidad
                FROM relacion
                WHERE bandera = 1
                GROUP BY Id_Deporte
                ORDER BY total_probabilidad DESC
                LIMIT 5
            """
            self.cursor.execute(consulta_query)
            resultados = self.cursor.fetchall()

            # Obtener nombres de actividades seleccionadas para la justificación
            actividad_nombres_query = "SELECT nombre FROM Actividad WHERE Id_Actividad IN (%s)" % ",".join(map(str, id_actividades))
            self.cursor.execute(actividad_nombres_query)
            actividades_nombres = [row[0] for row in self.cursor.fetchall()]
            actividades_texto = ", ".join(actividades_nombres)

            # Generar mensaje con nombres de deportes y cálculo de porcentajes
            mensaje = "Los 5 deportes más probables (de mayor a menor) son:\n\n"
            deporte_principal = None
            for deporte_id, probabilidad_acumulada in resultados:
                # Obtener datos del deporte desde la tabla Deporte
                deporte_query = "SELECT nombre, peso FROM Deporte WHERE Id_Deporte = %s"
                self.cursor.execute(deporte_query, (deporte_id,))
                deporte_data = self.cursor.fetchone()

                if deporte_data:
                    nombre_deporte, peso_deporte = deporte_data
                    porcentaje_probabilidad = (probabilidad_acumulada / peso_deporte) * 100
                    if not deporte_principal:
                        deporte_principal = nombre_deporte  # Guardar el deporte más probable

                    # Formatear mensaje para cada deporte
                    mensaje += f"Deporte: {nombre_deporte}\n"
                    mensaje += f" - Probabilidad estimada: {porcentaje_probabilidad:.2f}%\n\n"

            # Añadir justificación al final del mensaje (este se añadió en el modulo de explicación :D)
            #mensaje += f"Justificación: Debido a que tienes las siguientes actividades: {actividades_texto}."

            # Crear una ventana personalizada para mostrar resultados e incluir el botón "Continuar"
            ventana_resultados = tk.Toplevel(self.root)
            ventana_resultados.title("Inferencia")
            ventana_resultados.geometry("500x400")

            # Mostrar resultados de la inferencia
            etiqueta_resultados = tk.Label(ventana_resultados, text=mensaje, justify="left", wraplength=480)
            etiqueta_resultados.pack(pady=20)

            # Botón para continuar con las preguntas
            def continuar_preguntas():
                ventana_resultados.destroy()
                if deporte_principal:
                    self.preguntar_otras_actividades(deporte_principal)

            boton_continuar = tk.Button(ventana_resultados, text="Continuar", command=continuar_preguntas)
            boton_continuar.pack(pady=10)

            # Botón para cerrar la ventana sin hacer nada más
            boton_cerrar = tk.Button(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy)
            boton_cerrar.pack(pady=10)


            # Devuelve bandera a 0 en la tabla relacion
            self.cursor.execute("UPDATE relacion SET bandera = 0")
            self.conn.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al ejecutar la inferencia: {err}")

    def preguntar_otras_actividades(self, deporte_principal):
    # Crear una lista con las actividades relacionadas que no han sido seleccionadas previamente
        try:
            # Consulta para obtener actividades relacionadas al deporte
            query = """
                SELECT a.Id_Actividad, a.nombre 
                FROM Actividad a
                JOIN relacion r ON a.Id_Actividad = r.id_actividad
                WHERE r.Id_Deporte = (SELECT Id_Deporte FROM Deporte WHERE nombre = %s)
            """
            self.cursor.execute(query, (deporte_principal,))
            actividades_relacionadas = self.cursor.fetchall()

            # Filtrar actividades que ya han sido seleccionadas en el Treeview
            actividades_seleccionadas = {
                self.relation_table.item(item, "values")[0] for item in self.relation_table.get_children()
            }
            actividades_pendientes = [
                actividad for actividad in actividades_relacionadas if str(actividad[0]) not in actividades_seleccionadas
            ]
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudieron obtener las actividades relacionadas: {err}")
            return

        # Función para preguntar por cada actividad pendiente
        def iterar_actividades():
            if not actividades_pendientes:
                messagebox.showinfo("Información", "No hay más actividades relacionadas pendientes.")
                return

            actividad_actual = actividades_pendientes.pop(0)  # Tomar la primera actividad de la lista
            actividad_id, actividad_nombre = actividad_actual

            # Crear una ventana emergente para preguntar sobre la actividad actual
            ventana_actividad = tk.Toplevel(self.root)
            ventana_actividad.title("Actividad Relacionada")
            ventana_actividad.geometry("400x200")

            etiqueta = tk.Label(
                ventana_actividad,
                text=f"La actividad '{actividad_nombre}' se presenta en el deporte '{deporte_principal}'?"
            )
            etiqueta.pack(pady=20)

            # Botón "Sí"
            def respuesta_si():
                # Añadir actividad al Treeview si es confirmada
                self.relation_table.insert("", "end", values=(actividad_id, actividad_nombre))
                ventana_actividad.destroy()
                iterar_actividades()  # Pasar a la siguiente actividad

            boton_si = tk.Button(ventana_actividad, text="Sí", command=respuesta_si)
            boton_si.pack(side=tk.LEFT, padx=50, pady=20)

            # Botón "No"
            def respuesta_no():
                ventana_actividad.destroy()
                self.mostrar_conclusion()
                #iterar_actividades()  # Pasar a la siguiente actividad

            boton_no = tk.Button(ventana_actividad, text="No", command=respuesta_no)
            boton_no.pack(side=tk.RIGHT, padx=50, pady=20)

            # Botón "No sé"
            def respuesta_no_se():
                ventana_actividad.destroy()
                iterar_actividades()  # Pasar a la siguiente actividad

            boton_no_se = tk.Button(ventana_actividad, text="No sé", command=respuesta_no_se)
            boton_no_se.pack(side=tk.RIGHT, padx=50, pady=20)

        # Iniciar la iteración de actividades pendientes
        iterar_actividades()

    def mostrar_conclusion(self):
        # Obtener IDs de los síntomas seleccionados
        id_actividades = [int(self.relation_table.item(item, "values")[0]) for item in self.relation_table.get_children()]

        if not id_actividades:
            messagebox.showinfo("Información", "Seleccione al menos una actividad para ejecutar la inferencia.")
            return

        try:
            # Actualizar bandera = 1 en la tabla relacion donde id_actividad coincide
            update_query = "UPDATE relacion SET bandera = 1 WHERE id_actividad = %s"
            for id_actividad in id_actividades:
                self.cursor.execute(update_query, (id_actividad,))
            self.conn.commit()

            # Consulta para obtener el deporte con la mayor probabilidad
            consulta_query = """
                SELECT Id_Deporte, SUM(probabilidad) as total_probabilidad
                FROM relacion
                WHERE bandera = 1
                GROUP BY Id_Deporte
                ORDER BY total_probabilidad DESC
                LIMIT 1  -- Solo obtenemos el deporte con mayor probabilidad
            """
            self.cursor.execute(consulta_query)
            resultado = self.cursor.fetchone()

            if resultado:
                deporte_id, probabilidad_acumulada = resultado

                # Obtener nombres de actividades seleccionadas para la justificación
                actividad_nombres_query = "SELECT nombre FROM Actividad WHERE Id_Actividad IN (%s)" % ",".join(map(str, id_actividades))
                self.cursor.execute(actividad_nombres_query)
                actividades_nombres = [row[0] for row in self.cursor.fetchall()]
                actividades_texto = ", ".join(actividades_nombres)

                # Obtener datos del deporte desde la tabla Deporte
                deporte_query = "SELECT nombre, peso FROM Deporte WHERE Id_Deporte = %s"
                self.cursor.execute(deporte_query, (deporte_id,))
                deporte_data = self.cursor.fetchone()

                if deporte_data:
                    nombre_deporte, peso_deporte = deporte_data
                    porcentaje_probabilidad = (probabilidad_acumulada / peso_deporte) * 100

                    # Generar el mensaje de conclusión con el deporte más probable
                    mensaje = f"CONCLUSIÓN:\n\nEl {nombre_deporte} es tu deporte más probable con un {porcentaje_probabilidad:.2f}% de probabilidad, "
                    mensaje += f"debido a que tienes las siguientes actividades seleccionadas: \n\n"

                    # Agregar las actividades en formato de lista
                    for actividad in actividades_nombres:
                        mensaje += f" - {actividad}\n"


                    # Mostrar el mensaje usando messagebox con solo el botón "Aceptar"
                    def on_accept():
                        messagebox.showinfo("Módulo de explicación", mensaje)
                        self.ejecutar_inferencia()  # Regresa a la lógica de inferencia

                    # Mostrar el mensaje
                    on_accept()  # Llamamos a la función para mostrar el mensaje y regresar a inferencia

            # Devuelve bandera a 0 en la tabla relacion
            self.cursor.execute("UPDATE relacion SET bandera = 0")
            self.conn.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al ejecutar la inferencia: {err}")




# Creación de la ventana
root = tk.Tk()
app = BusquedaActividad(root)
root.mainloop()
