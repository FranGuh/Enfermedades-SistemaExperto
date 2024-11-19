import tkinter as tk
from tkinter import messagebox
import mysql.connector  # Para interactuar con MySQL

class ModuloDiagnostico:
    def __init__(self, root, resultados, actividades_nombres, sintomas_seleccionados):
        self.root = root
        self.resultados = resultados
        self.actividades_nombres = actividades_nombres
        self.sintomas_seleccionados = sintomas_seleccionados
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(self.frame, text="Diagnóstico", font=("Helvetica", 16)).pack(pady=10)

        # Mostrar tabla de diagnóstico (síntomas y actividades)
        self.diagnostico_frame = tk.Frame(self.frame)
        self.diagnostico_frame.pack(pady=10)
        
        tk.Label(self.diagnostico_frame, text="Síntomas", font=("Helvetica", 14)).grid(row=0, column=0, padx=10)
        tk.Label(self.diagnostico_frame, text="Actividades", font=("Helvetica", 14)).grid(row=0, column=1, padx=10)

        # Llenar la tabla con los síntomas seleccionados y las actividades
        for i, sintoma in enumerate(self.sintomas_seleccionados):
            tk.Label(self.diagnostico_frame, text=sintoma, font=("Helvetica", 12)).grid(row=i + 1, column=0, padx=10, pady=5)
            tk.Label(self.diagnostico_frame, text=self.actividades_nombres[i], font=("Helvetica", 12)).grid(row=i + 1, column=1, padx=10, pady=5)

        # Mostrar los resultados de probabilidad de deportes
        tk.Label(self.frame, text="Resultados de probabilidad:", font=("Helvetica", 14)).pack(pady=10)
        for deporte_id, probabilidad, nombre_deporte in self.resultados:
            tk.Label(self.frame, text=f"{nombre_deporte}: {probabilidad:.2f}%", font=("Helvetica", 14)).pack(pady=5)

        # Botones de interacción
        tk.Button(self.frame, text="Mostrar base de hechos", command=self.mostrar_base_de_hechos).pack(pady=10)
        tk.Button(self.frame, text="Continuar", command=self.continuar_con_preguntas).pack(pady=10)

    def mostrar_base_de_hechos(self):
        # Realizar consulta a la base de datos de hechos
        connection = mysql.connector.connect(
            host="localhost",
            user="roger",
            password="1234",
            database="Conocimiento3"
        )
        cursor = connection.cursor()

        # Consulta a la base de datos para obtener datos relevantes
        cursor.execute(''' 
            SELECT sintomas.sintoma, actividades.nombre_actividad
            FROM sintomas
            JOIN actividades ON sintomas.id_actividad = actividades.id_actividad
            WHERE sintomas.sintoma IN (%s)
        ''', tuple(self.sintomas_seleccionados))  # Usamos los síntomas seleccionados

        results = cursor.fetchall()

        # Mostrar la información obtenida
        base_hechos = "\n".join([f"Sintoma: {row[0]} - Actividad: {row[1]}" for row in results])
        messagebox.showinfo("Base de Hechos", base_hechos)

        # Cerrar la conexión
        cursor.close()
        connection.close()

    def continuar_con_preguntas(self):
        # Preguntar si se observan más actividades para el deporte más probable
        respuesta = messagebox.askquestion("¿Más actividades?", "¿Observas más actividades para este deporte?")
        if respuesta == "no":
            ModuloExplicacion(self.root)
        else:
            self.incrementar_porcentaje()

    def incrementar_porcentaje(self):
        # Aquí aumentas el porcentaje de la actividad seleccionada
        messagebox.showinfo("Actualización", "Porcentaje incrementado para el deporte seleccionado.")
        # Regresar a la pantalla de diagnóstico con el porcentaje actualizado
        ModuloDiagnostico(self.root, self.resultados, self.actividades_nombres, self.sintomas_seleccionados)

class ModuloExplicacion:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(self.frame, text="Explicación del Diagnóstico", font=("Helvetica", 16)).pack(pady=10)

        # Explicación de la enfermedad y las actividades
        tk.Label(self.frame, text="Conclusión: Las actividades más comunes en este deporte son...", font=("Helvetica", 14)).pack(pady=10)

        # Mostrar los resultados de diagnóstico final
        tk.Label(self.frame, text="Ejemplo de deporte: Fútbol (85% probabilidad)", font=("Helvetica", 12)).pack(pady=5)

        # Botón para regresar a la pantalla 7
        tk.Button(self.frame, text="Aceptar", command=self.regresar_inicio).pack(pady=20)

    def regresar_inicio(self):
        self.frame.pack_forget()  # Regresa a la pantalla anterior (pantalla 7)
        # Crear la pantalla de diagnóstico nuevamente
        resultados = [(1, 85.5, "Fútbol"), (2, 75.2, "Básquetbol"), (3, 60.0, "Tennis")]
        actividades_nombres = ["Fútbol", "Básquetbol", "Tennis"]
        sintomas_seleccionados = ["Dolor de rodilla", "Fatiga extrema"]
        ModuloDiagnostico(self.root, resultados, actividades_nombres, sintomas_seleccionados)
