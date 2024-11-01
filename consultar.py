import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
from controlador.controlador import ControladorDB  # Asegúrate de tener el controlador

def ventana_modificacion(id_objeto):
    def cargar_datos():
        try:
            db_controlador = ControladorDB('localhost', 'root', 'root', 'Conocimiento')

            # Consulta para obtener los datos del objeto
            query = "SELECT Nombre, Descripcion, Imagen FROM Enfermedad WHERE Id_Enfermedad = %s"
            resultado = db_controlador.obtener_datos(query, (id_objeto,))

            if resultado:
                nombre_entry.delete(0, tk.END)
                descripcion_text.delete("1.0", tk.END)

                nombre_entry.insert(0, resultado[0][0])  # Nombre
                descripcion_text.insert("1.0", resultado[0][1])  # Descripción

                # Cargar imagen
                imagen_path = resultado[0][2]
                if os.path.exists(imagen_path):
                    img = Image.open(imagen_path)
                    img = img.resize((250, 250), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    img_label.img_tk = img_tk
                    img_label.config(image=img_tk)
                    img_label.image_path = imagen_path
                else:
                    messagebox.showwarning("Advertencia", "La imagen no se encontró.")
            else:
                messagebox.showwarning("Advertencia", "No se encontró ningúna enfermedad con ese ID.")
                ventana_modificacion.destroy()  # Destruir la ventana si no se encuentra el ID
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")

        finally:
            db_controlador.cerrar_conexion()

    def realizar_modificacion():
        nuevo_nombre = nombre_entry.get()
        nueva_descripcion = descripcion_text.get("1.0", tk.END).strip()
        nueva_imagen = img_label.image_path if hasattr(img_label, 'image_path') else None

        if nuevo_nombre and nueva_descripcion:
            try:
                db_controlador = ControladorDB('localhost', 'root', 'root', 'Conocimiento')

                # Preparar la consulta de actualización
                query = "UPDATE Enfermedad SET Nombre = %s, Descripcion = %s, Imagen = %s WHERE Id_Enfermedad = %s"
                db_controlador.modificar_datos(query, (nuevo_nombre, nueva_descripcion, nueva_imagen, id_objeto))

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", "Enfermedad modificada exitosamente.")
                
                # Cerrar ventana de modificación
                ventana_modificacion.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar enfermedad: {e}")

            finally:
                db_controlador.cerrar_conexion()

        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            nombre_entry.focus_set()  # Regresar el foco al campo de nombre si hay advertencias

    def cargar_imagen():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )

        if file_path:
            try:
                img = Image.open(file_path)
                img = img.resize((250, 250), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                img_label.img_tk = img_tk
                img_label.config(image=img_tk)
                img_label.image_path = file_path

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
                img_label.image_path = None

    # Crear ventana para modificación
    ventana_modificacion = tk.Toplevel()
    ventana_modificacion.title("Objeto")
    ventana_modificacion.attributes('-topmost', False)  # Mantener en primer plano

    # Centrar la ventana
    window_width = 1300  # Ancho de la ventana
    window_height = 600  # Alto de la ventana
    screen_width = ventana_modificacion.winfo_screenwidth()
    screen_height = ventana_modificacion.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    ventana_modificacion.geometry(f'{window_width}x{window_height}+{x}+{y}')
    ventana_modificacion.focus_force()  # Forzar el foco en esta ventana

    # Entrada para el nuevo nombre
    tk.Label(ventana_modificacion, text="Nombre:").pack()
    nombre_entry = tk.Entry(ventana_modificacion)
    nombre_entry.pack(pady=5)
    nombre_entry.focus_set()  # Establecer el foco en el campo de nombre

    # Área de texto para la nueva descripción
    tk.Label(ventana_modificacion, text="Descripción:").pack()
    descripcion_text = tk.Text(ventana_modificacion, width=30, height=5)
    descripcion_text.pack(pady=5)

    # Etiqueta para mostrar la imagen
    img_label = tk.Label(ventana_modificacion, text="No hay imagen cargada")
    img_label.pack(pady=10)

    # Botón para cargar nueva imagen
   # cargar_imagen_btn = tk.Button(ventana_modificacion, text="Cargar Nueva Imagen", command=cargar_imagen)
   # cargar_imagen_btn.pack(pady=5)

    # Botón para realizar la modificación
   # modificar_btn = tk.Button(ventana_modificacion, text="", command=realizar_modificacion)
   # modificar_btn.pack(pady=10)

    # Cargar los datos al abrir la ventana
    cargar_datos()

def ventana_ingreso_id2():
    def obtener_id_y_modificar():
        id_objeto = id_entry.get()  # Obtiene el ID del campo de entrada
        if id_objeto:
            # Comprobar si el ID existe antes de abrir la ventana de modificación
            try:
                db_controlador = ControladorDB('localhost', 'root', 'root', 'Conocimiento')
                query = "SELECT * FROM Enfermedad WHERE Id_Enfermedad = %s"
                resultado = db_controlador.obtener_datos(query, (id_objeto,))

                if resultado:
                    ventana_modificacion(id_objeto)  # Llama a la función modificar con el ID ingresado
                    ventana_ingreso.destroy()  # Destruye la ventana de ingreso de ID
                else:
                    messagebox.showwarning("Advertencia", "No se encontró una enfermedad con ese ID.")

            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar enfermedad: {e}")

            finally:
                db_controlador.cerrar_conexion()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un ID de una enfermedad.")

    # Crear ventana para ingresar el ID
    ventana_ingreso = tk.Toplevel()
    ventana_ingreso.title("Buscar Enfermedad")
    # ventana_ingreso.attributes('-topmost', True)  # Mantener en primer plano

    # Centrar la ventana
    window_width = 300  # Ancho de la ventana
    window_height = 200  # Alto de la ventana
    screen_width = ventana_ingreso.winfo_screenwidth()
    screen_height = ventana_ingreso.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    ventana_ingreso.geometry(f'{window_width}x{window_height}+{x}+{y}')
    ventana_ingreso.focus_force()  # Forzar el foco en esta ventana

    tk.Label(ventana_ingreso, text="ID de la Enfermedad:").pack()
    id_entry = tk.Entry(ventana_ingreso)  # Definimos id_entry aquí
    id_entry.pack(pady=5)
    id_entry.focus_set()  # Establecer el foco en el campo de ID

    buscar_btn = tk.Button(ventana_ingreso, text="Buscar", command=obtener_id_y_modificar)
    buscar_btn.pack(pady=5)
