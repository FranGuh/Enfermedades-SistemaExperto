import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import os
import shutil
import Imagenes
from Actividads.modificar import ventana_ingreso_id
from Actividads.eliminar import ventana_bajas
from Actividads.consultar import ventana_ingreso_id2
from controlador.controlador import ControladorDB  # Importar el controlador de base de datos



def menu_agregarActividad(master):
    global img_label  
    global carpeta_imagenes  
    carpeta_imagenes = r"Imagenes\Actividad"
    os.makedirs(carpeta_imagenes, exist_ok=True)  # Crear la carpeta si no existe
    

    def volverPantalla():
        ventana.withdraw()
        ventana.deiconify()
        
    def agregar_objeto():
        nombre = nombre_entry.get()
        #descripcion = descripcion_text.get("1.0", tk.END).strip()
        imagen = getattr(img_label, 'image_path', None)  # Asegúrate de que esto tenga la ruta correcta

        if nombre and imagen:
            try:
                # Establecer la conexión a la base de datos
                db_controlador = ControladorDB('localhost', 'roger', '1234', 'Conocimiento3')

                # Preparar la consulta de inserción
                query = "INSERT INTO Actividads (Nombre, Imagen) VALUES (%s, %s)"
                db_controlador.insertar_datos(query, (nombre, imagen))

                # Mostrar un mensaje de éxito
                messagebox.showinfo("Éxito", "Actividads agregado a la base de datos.")
                
                # Volver a la pantalla anterior
                volverPantalla()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el Actividads a la base de datos: {e}")
                volverPantalla()

            finally:
                db_controlador.cerrar_conexion()
                volverPantalla()

        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            volverPantalla()


    def consultar_datos():
        ventana_consulta = tk.Toplevel(ventana)
        ventana_consulta.title("Consulta de Actividads")
        ventana.geometry(f'{window_width}x{window_height}+{x}+{y}') 

        tree = ttk.Treeview(ventana_consulta, columns=("Id_Actividad","Nombre", "Imagen"), show='headings')
        tree.heading("Id_Actividad", text="Id_Actividad")
        tree.heading("Nombre", text="Nombre")
        #tree.heading("Descripcion", text="Descripción")
        tree.heading("Imagen", text="Imagen")
        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(ventana_consulta, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        try:
            db_controlador = ControladorDB('localhost', 'roger', '1234', 'Conocimiento3')
            query = "SELECT Id_Actividad,Nombre, Imagen FROM Actividads"
            objetos = db_controlador.obtener_datos(query)

            for objeto in objetos:
                tree.insert('', tk.END, values=objeto)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la consulta: {e}")
        finally:
            db_controlador.cerrar_conexion()
            
    def cargar_imagen():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )

        if file_path:
            try:
                # Obtener el nombre de la imagen y la ruta de destino
                nombre_imagen = os.path.basename(file_path)
                destino = os.path.join(carpeta_imagenes, nombre_imagen)

                # Comprobar si la imagen ya existe
                if os.path.exists(destino):
                    messagebox.showwarning("Advertencia", "La imagen ya existe.")
                    img = Image.open(destino)
                    volverPantalla()
                else:
                    shutil.copy(file_path, destino)  # Copiar la imagen
                    img = Image.open(destino)
                    volverPantalla()
                # Redimensionar y mostrar la imagen
                img = img.resize((250, 250), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                img_label.img_tk = img_tk
                img_label.config(image=img_tk)

                # Guardar la ruta de la imagen en el label
                img_label.image_path = destino  # Asignar la ruta correctamente

                print(f"Imagen cargada: {img_label.image_path}")  # Debug: Verificar que la imagen se cargó
                volverPantalla()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
                img_label.image_path = None  # Asegurarse de que sea None en caso de error
                volverPantalla()
                
    

    # Crear la ventana principal
    ventana = tk.Toplevel(master)
    ventana.title("Agregar Actividad")
    
        #ICONOS
    #flecha_icono = Image.open("Imagenes/Iconos/flecha.png")   
    #flecha_icono = flecha_icono.resize((20, 20), Image.Resampling.LANCZOS)
    #flecha_icono = ImageTk.PhotoImage(flecha_icono)

    #elimina
    #baja_icono = Image.open("Imagenes/Iconos/baja.png")   
    #baja_icono = baja_icono.resize((20, 20), Image.Resampling.LANCZOS)
    #baja_icono = ImageTk.PhotoImage(baja_icono)

    #insertar
    #insert_icono = Image.open("Imagenes/Iconos/insertar.jpg")   
    #insert_icono = insert_icono.resize((20, 20), Image.Resampling.LANCZOS)
    #insert_icono = ImageTk.PhotoImage(insert_icono)

    #consulta
    #consult_icono = Image.open("Imagenes/Iconos/consulta.png")   
    #consult_icono = consult_icono.resize((20, 20), Image.Resampling.LANCZOS)
    #consult_icono = ImageTk.PhotoImage(consult_icono)

    #modificar
    #modifi_icono = Image.open("Imagenes/Iconos/modificar.png")   
    #modifi_icono = modifi_icono.resize((20, 20), Image.Resampling.LANCZOS)
    #modifi_icono = ImageTk.PhotoImage(modifi_icono)

 # Obtener el tamaño de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Establecer la ventana con un porcentaje del tamaño de la pantalla
    window_width = int(screen_width * 0.8)   # 80% del ancho de la pantalla
    window_height = int(screen_height * 0.8)  # 80% del alto de la pantalla

    # Centrar la ventana
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    ventana.geometry(f'{window_width}x{window_height}+{x}+{y}') 
    
    # Título centrado
    titulo = tk.Label(ventana, text="Agregar Actividad", font=("Arial", 16))
    titulo.pack(pady=10)

    # Crear el marco principal
    main_frame = tk.Frame(ventana)
    main_frame.pack(pady=20)

    # Panel derecho
    derecha_frame = tk.Frame(main_frame)
    derecha_frame.pack(side=tk.RIGHT, padx=20)

    # Panel izquierdo
    izquierda_frame = tk.Frame(main_frame)
    izquierda_frame.pack(side=tk.LEFT, padx=20)

    # Etiqueta y entrada para Nombre
    tk.Label(izquierda_frame, text="Nombre:").pack(anchor=tk.W)
    nombre_entry = tk.Entry(izquierda_frame, width=30)
    nombre_entry.pack(pady=5)

    # Etiqueta y área de texto para Descripción
   # tk.Label(izquierda_frame, text="Descripción:").pack(anchor=tk.W)
    #descripcion_text = scrolledtext.ScrolledText(izquierda_frame, width=30, height=10)
    #descripcion_text.pack(pady=5)

    # Botón para cargar imagen
    cargar_imagen_btn = tk.Button(derecha_frame, text="Cargar Imagen", command=cargar_imagen)
    cargar_imagen_btn.pack(pady=10)

    # Etiqueta para mostrar la imagen cargada
    img_label = tk.Label(derecha_frame, text="No hay imagen cargada")
    img_label.pack(pady=5)

    # Botones para agregar, modificar y salir
    botones_frame = tk.Frame(ventana)
    botones_frame.pack(side=tk.BOTTOM, pady=20)

    # Botones para consultas
    consultas_frame = tk.Frame(ventana)
    consultas_frame.pack(side=tk.BOTTOM, pady=40)

    # Botón de Altas
    altas_btn = tk.Button(botones_frame, text="Altas", command=agregar_objeto)
    altas_btn.pack(side=tk.LEFT, padx=10)

    # Botón de Bajas
    bajas_btn = tk.Button(botones_frame, text="Bajas", command=ventana_bajas)
    bajas_btn.pack(side=tk.LEFT, padx=10)

    # Botón de Modificaciones
    modificaciones_btn = tk.Button(botones_frame, text="Modificaciones", command=ventana_ingreso_id)
    modificaciones_btn.pack(side=tk.LEFT, padx=10)
    
     # Botón de Consultar
    consultar_btn = tk.Button(botones_frame, text="Consultar General",command=consultar_datos)
    consultar_btn.pack(side=tk.LEFT, padx=10)
    
     # Botón de Consultar
    consultar_btn = tk.Button(botones_frame, text="Consultar Individual", command=ventana_ingreso_id2)
    consultar_btn.pack(side=tk.LEFT, padx=10)

    # Botón de Salir
    salir_btn = tk.Button(botones_frame, text="Salir", command=ventana.destroy)
    salir_btn.pack(side=tk.LEFT, padx=10)

    # Variables para manejar la carga de objetos
    global current_index
    global objetos
    current_index = 0  # Inicializar índice
    objetos = []  # Lista de objetos

    def cargar_objetos():
        global objetos
        try:
            # Establecer la conexión a la base de datos
            db_controlador = ControladorDB('localhost', 'roger', '1234', 'Conocimiento3')

            # Consulta para obtener todos los objetos
            query = "SELECT Nombre, Imagen FROM Actividads"
            objetos = db_controlador.obtener_datos(query)  # Supone que este método devuelve una lista de tuplas

            if objetos:
                mostrar_objeto(current_index)  # Muestra el primer objeto

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los Actividads: {e}")
        finally:
            db_controlador.cerrar_conexion()

    def mostrar_objeto(index):
        if 0 <= index < len(objetos):
            nombre, imagen = objetos[index]

            nombre_entry.config(state='normal')  # Habilitar para poder mostrar
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, nombre)

            #descripcion_text.config(state='normal')  # Habilitar para poder mostrar
            #descripcion_text.delete("1.0", tk.END)
            #descripcion_text.insert("1.0", descripcion)

            # Cargar imagen
            cargar_imagen(imagen)

    def cargar_imagen(imagen_path):
        try:
            img = Image.open(imagen_path)
            img = img.resize((250, 250), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk)
            img_label.image = img_tk  # Mantener una referencia a la imagen
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
            

    def mostrar_siguiente():
        cargar_objetos()
        global current_index
        if current_index + 1 < len(objetos):
            current_index += 1
            mostrar_objeto(current_index)

    def mostrar_anterior():
        cargar_objetos()
        global current_index
        if current_index - 1 >= 0:
            current_index -= 1
            mostrar_objeto(current_index)

    def mostrar_inicio():
        cargar_objetos()
        global current_index
        current_index = 0
        mostrar_objeto(current_index)

    def mostrar_final():
        cargar_objetos()
        global current_index
        current_index = len(objetos) - 1
        mostrar_objeto(current_index)

    # Cargar los objetos al iniciar
    cargar_objetos()
    
    # Que haga como consultas estos botones el siguiente vaya recorriendo al siguiente objeto en la base de datos  y lo muestre en esta ventana
    consultaSiguiente_btn = tk.Button(consultas_frame, text="Siguiente", command=mostrar_siguiente)
    consultaSiguiente_btn.pack(side=tk.LEFT, padx=10)
    
    # El anterior se recorra al de atrás y pss lo muestre
    consultaAnterior_btn = tk.Button(consultas_frame, text="Anterior", command=mostrar_anterior)
    consultaAnterior_btn.pack(side=tk.LEFT, padx=10)
    
    # El Inicio se vaya al primer valor de la tabla
    consultaGeneral_btn = tk.Button(consultas_frame, text="Inicio", command=mostrar_inicio)
    consultaGeneral_btn.pack(side=tk.LEFT, padx=10)

    # El Fin vaya al último objeto de la tabla
    consultaFinal_btn = tk.Button(consultas_frame, text="Final", command=mostrar_final)
    consultaFinal_btn.pack(side=tk.LEFT, padx=10)

    # Crear botón para regresar
    volver_btn = tk.Button(ventana, text="Regresar", command=volverPantalla)
    volver_btn.pack(side=tk.BOTTOM, pady=10)

    ventana.protocol("WM_DELETE_WINDOW", volverPantalla)  # Para manejar el cierre de la ventana

