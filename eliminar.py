import tkinter as tk
from tkinter import messagebox
from controlador.controlador import ControladorDB  # Asegúrate de tener el controlador

def centrar_ventana(ventana, ancho=300, alto=200):
    # Obtener el tamaño de la pantalla
    ancho_ventana = ancho
    alto_ventana = alto
    x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

def eliminar_objeto(id_objeto):
    try:
        db_controlador = ControladorDB('localhost', 'root', 'root', 'Conocimiento')

        # Consulta para obtener el nombre del objeto por ID
        query = "SELECT Nombre FROM Enfermedad WHERE Id_Enfermedad = %s"
        resultado = db_controlador.obtener_datos(query, (id_objeto,))

        if resultado:
            nombre_objeto = resultado[0][0]  # Nombre del objeto
            # Pregunta si desea eliminar el objeto
            if messagebox.askyesno("Confirmar Eliminación", f"¿Deseas eliminar la enfermedad '{nombre_objeto}'?"):
                # Ejecutar eliminación
                query_delete = "DELETE FROM Enfermedad WHERE Id_Enfermedad = %s"
                db_controlador.modificar_datos(query_delete, (id_objeto,))
                messagebox.showinfo("Éxito", "Enfermedad eliminada exitosamente.")
        else:
            messagebox.showinfo("Advertencia", "No se encontró ninguna Enfermedad con ese ID.")

    except Exception as e:
        messagebox.showinfo("Error", f"Error al eliminar Enfermedad: {e}")

    finally:
        db_controlador.cerrar_conexion()

def ventana_bajas():
    def obtener_id_y_eliminar():
        id_objeto = id_entry.get()  # Obtiene el ID del campo de entrada
        if id_objeto:
            eliminar_objeto(id_objeto)  # Llama a la función para eliminar el objeto
            ventana_bajas.destroy()  # Destruye la ventana de bajas
        else:
            messagebox.showinfo("Advertencia", "Por favor, ingresa un ID de Enfermedad.")

    # Crear ventana para ingresar el ID
    ventana_bajas = tk.Toplevel()
    ventana_bajas.title("Eliminar Enfermedad")

    tk.Label(ventana_bajas, text="ID de Enfermedad a Eliminar:").pack()
    id_entry = tk.Entry(ventana_bajas)  # Definimos id_entry aquí
    id_entry.pack(pady=5)

    buscar_btn = tk.Button(ventana_bajas, text="Eliminar Enfermedad", command=obtener_id_y_eliminar)
    buscar_btn.pack(pady=5)

    # Centrar la ventana
    centrar_ventana(ventana_bajas, 300, 150)  # Ancho: 300, Alto: 150
