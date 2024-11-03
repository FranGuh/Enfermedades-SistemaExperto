import tkinter as tk
from tkinter import ttk,messagebox, filedialog, scrolledtext
from PIL import Image,ImageTk
import subprocess
#from controlador.controlador import ControladorDB
import os
from agregar import menu_agregarObjeto
from Usuario import mostrar_interfaz_usuario
import shutil
from Sintomas.agregarS import menu_agregarSintoma

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema Experto Genérico")
root.geometry("1920x1080")  # Ajustar la resolución de la ventana

# Cargar la imagen de la flecha
#flecha_icono = Image.open("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/Iconos/flecha.png") 
flecha_icono = Image.open("Imagenes/Iconos/flecha.png")   
flecha_icono = flecha_icono.resize((20, 20), Image.Resampling.LANCZOS)
flecha_icono = ImageTk.PhotoImage(flecha_icono)
# Imagen personas.
# person_icono = Image.open("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/Iconos/person.png") 
person_icono = Image.open("Imagenes/Iconos/person.png") 
person_icono = person_icono.resize((20, 20), Image.Resampling.LANCZOS)
person_icono = ImageTk.PhotoImage(person_icono)
# Imagen persona.
#persona_icono = Image.open("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/Iconos/persona.png")
persona_icono = Image.open("Imagenes/Iconos/persona.png") 
persona_icono = persona_icono.resize((20, 20), Image.Resampling.LANCZOS)
persona_icono = ImageTk.PhotoImage(persona_icono)
# Imagen entrar.
#entrar_icono = Image.open("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/Iconos/entrar.png")
entrar_icono = Image.open("Imagenes/Iconos/entrar.png")
entrar_icono = entrar_icono.resize((20, 20), Image.Resampling.LANCZOS)
entrar_icono = ImageTk.PhotoImage(entrar_icono)
# Imagen salir.
#salir_icono = Image.open("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/Iconos/salir.png")
salir_icono = Image.open("Imagenes/Iconos/salir.png") 
salir_icono = salir_icono.resize((20, 20), Image.Resampling.LANCZOS)
salir_icono = ImageTk.PhotoImage(salir_icono)



# Función para cerrar la aplicación
def salir():
    root.quit()

# Función para mostrar la pantalla de bienvenida
def pantalla_bienvenida():
    limpiar_pantalla()

    # Fondo de imagen
    #ruta_fondo = "C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/imagen.png"
    ruta_fondo = "Imagenes/imagen.png"
    fondo = Image.open(ruta_fondo)
    fondo = fondo.resize((1920, 1080), Image.Resampling.LANCZOS)
    fondo = ImageTk.PhotoImage(fondo)
    label_fondo = tk.Label(root, image=fondo)
    label_fondo.image = fondo
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Logos en las esquinas superiores
    #agregar_imagen_bienvenida("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/tecnm.jpg", root, "nw")
    #agregar_imagen_bienvenida("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/itz.jpg", root, "ne")
    agregar_imagen_bienvenida("Imagenes/tecnm.jpg", root, "nw")
    agregar_imagen_bienvenida("Imagenes/itz.jpg", root, "ne")

    # Texto centrado
    lbl_bienvenida = ttk.Label(root, text="¡Bienvenidos!", font=("Arial", 32), background="#FFFFFF")
    lbl_bienvenida.place(relx=0.5, rely=0.4, anchor="center")

    lbl_itz = ttk.Label(root, text="I.T.Z", font=("Arial", 28), background="#FFFFFF")
    lbl_itz.place(relx=0.5, rely=0.45, anchor="center")

    lbl_sistema = ttk.Label(root, text="Sistema Experto para el Diagnóstico de Enfermedades", font=("Arial", 28), background="#FFFFFF")
    lbl_sistema.place(relx=0.5, rely=0.5, anchor="center")

    # Botón Salir en la esquina inferior izquierda
    btn_salir = ttk.Button(root, text="Salir", command=salir, image=salir_icono, compound="left")
    btn_salir.place(x=100, y=700)

    # Botones en la esquina inferior derecha
    btn_acerca_de = ttk.Button(root, text="Acerca de...", command=pantalla_acerca_de, image=person_icono, compound="left" )
    btn_acerca_de.place(x=1380, y=600)

    btn_entrar = ttk.Button(root, text="Entrar", command=ventana_interfaces, image=entrar_icono, compound="left")
    btn_entrar.place(x=1380, y=700)

# Función para centrar las ventanas adicionales en la pantalla
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Función para mostrar la ventana de "Interfaces"
def ventana_interfaces():
    ventana = tk.Toplevel(root)  # Crear una ventana adicional
    ventana.title("Interfaces")
    ventana.geometry("400x300")  # Tamaño de la ventana "Interfaces"
    centrar_ventana(ventana, 400, 300)  # Centrar la ventana

    lbl_titulo = ttk.Label(ventana, text="Interfaces", font=("Arial", 24))
    lbl_titulo.pack(pady=20)

    # Variable para almacenar la opción seleccionada
    opcion = tk.IntVar()

    # Radiobutton para seleccionar "Experto" (opción 1)
     # Necesito agregar una imagen pequeña al lado izquierdo de la opcion
    rbtn_experto = ttk.Radiobutton(ventana, text="Experto", variable=opcion, value=1)
    rbtn_experto.pack(pady=10)

    # Radiobutton para seleccionar "Usuario" (opción 2)
    # Necesito agregar una imagen pequeña al lado izquierdo de la opcion
    rbtn_usuario = ttk.Radiobutton(ventana, text="Usuario", variable=opcion, value=2)
    rbtn_usuario.pack(pady=10)

    # Función para manejar la opción seleccionada
    def manejar_opcion():
        if opcion.get() == 1:
            ventana.destroy()  # Cerrar la ventana de "Interfaces"
            ventana_contraseña()  # Abrir la ventana de contraseña
        elif opcion.get() == 2:
            messagebox.showinfo("Opción seleccionada", "Modo Usuario seleccionado")
            ventana.destroy()  # Cerrar la ventana de "Interfaces"
            mostrar_interfaz_usuario()
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar una opción")

    # Botón Aceptar
    btn_aceptar = ttk.Button(ventana, text="Aceptar", command=manejar_opcion)
    btn_aceptar.pack(pady=20)

# Función para mostrar la ventana de contraseña
def ventana_contraseña():
    ventana = tk.Toplevel(root)  # Crear una ventana pequeña adicional
    ventana.title("Contraseña")
    ventana.geometry("600x300")  # Tamaño de la ventana de contraseña
    centrar_ventana(ventana, 400, 200)  # Centrar la ventana

    lbl_titulo = ttk.Label(ventana, text="Ingrese la Contraseña", font=("Arial", 16))
    lbl_titulo.pack(pady=20)

    # Campo de texto para ingresar la contraseña (con asteriscos)
    lbl_contraseña = ttk.Label(ventana, text="Contraseña: ")
    lbl_contraseña.pack(pady=0)
    entry_contraseña = ttk.Entry(ventana, show="*")
    entry_contraseña.pack(pady=0)

    # Función para validar la contraseña
    def validar_contraseña():
        if entry_contraseña.get() == "1234":
            ventana.destroy()  # Cerrar la ventana de contraseña
            messagebox.showinfo("Contraseña Correcta", "La contraseña es correcta")  # Mostrar mensaje
            menu_experto()  # Abrir el menú experto después del mensaje
        else:
            ventana.destroy()
            messagebox.showerror("Contraseña Incorrecta", "La contraseña es incorrecta. Inténtelo de nuevo")
            ventana_contraseña()
            

    # Botón Aceptar
    btn_aceptar_contraseña = ttk.Button(ventana, text="Aceptar", command=validar_contraseña)
    btn_aceptar_contraseña.pack(pady=20)

def ejecutar_relacion():
    subprocess.run(["python", "cuadro.py"])  # Ejecuta relacion.py

# Función para el menú experto (si la contraseña es correcta)
def menu_experto():
    limpiar_pantalla()

   
    agregar_imagen_bienvenida("Imagenes/Iconos/imagen.jpg", root, "yo")
    agregar_imagen_bienvenida("Imagenes/Iconos/imagen.jpg", root, "yo1")
    agregar_imagen_bienvenida("Imagenes/Iconos/imagen.jpg", root, "yo2")

    lbl_titulo = ttk.Label(root, text="Menú Experto", font=("Arial", 24))
    lbl_titulo.pack(pady=20)


    btn_agregarObjeto = ttk.Button(root, text="Agregar Enfermedad", command=lambda: menu_agregarObjeto(root), image=flecha_icono, compound="left")
    btn_agregarObjeto.place(x=600, y=150)
    btn_agregarObjeto.config(width=30, padding=(200, 30))

    btn_agregarCaracteristicas = ttk.Button(root, text="Agregar Síntomas",  command=lambda: menu_agregarSintoma(root), image=flecha_icono, compound="left")
    btn_agregarCaracteristicas.place(x=600, y=350)
    btn_agregarCaracteristicas.config(width=30, padding=(200, 30))

    btn_agregarCuadro = ttk.Button(root, text="Agregar Cuadro-Relación", command=ejecutar_relacion, image=flecha_icono, compound="left")
    btn_agregarCuadro.place(x=600, y=550)
    btn_agregarCuadro.config(width=30, padding=(200, 30))

    btn_volver = ttk.Button(root, text="Regresar", command=pantalla_bienvenida, image=flecha_icono, compound="left")
    #   btn_volver = ttk.Button(root, text="Regresar", command=pantalla_bienvenida, image=flecha_icono, compound="left"
    btn_volver.place(x=1380, y=700)




# Función para mostrar la pantalla Acerca de...
def pantalla_acerca_de():
    limpiar_pantalla()

    # Texto "Acerca del Sistema"
    lbl_titulo = ttk.Label(root, text="Acerca del Sistema", font=("Arial", 24))
    lbl_titulo.pack(pady=20)

    # Imagen centrada debajo del título
    #ruta_logo = "C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/logo1.png"
    ruta_logo = "Imagenes/logo1.png"
    logo = Image.open(ruta_logo)
    logo = logo.resize((300, 300), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)
    lbl_logo = tk.Label(root, image=logo)
    lbl_logo.image = logo
    lbl_logo.pack(pady=10)

    # Texto "Versión 1" a la izquierda
    lbl_version = ttk.Label(root, text="Versión 1", font=("Arial", 16))
    lbl_version.place(x=50, y=550)

    # Texto centrado de descripción
    descripcion_texto = "Este software es para uso exclusivo de los alumnos de la materia de I.A.\n"
    descripcion_texto += "de la carrera de Ing. en Sistemas Computacionales, para el Instituto Tecnológico de Zacatepec."
    lbl_descripcion = ttk.Label(root, text=descripcion_texto, font=("Arial", 16), wraplength=1000, justify="center")
    lbl_descripcion.place(relx=0.5, rely=0.75, anchor="center")

    # Botones en la esquina inferior derecha
    btn_autores = ttk.Button(root, text="Autores", command=pantalla_autores, image=person_icono, compound="left")
    btn_autores.place(x=1380, y=600)

    btn_volver = ttk.Button(root, text="Regresar", command=pantalla_bienvenida, image=flecha_icono, compound="left")
    #   btn_volver = ttk.Button(root, text="Regresar", command=pantalla_bienvenida, image=flecha_icono, compound="left"
    btn_volver.place(x=1380, y=700)

# Función para mostrar la pantalla de Autores
def pantalla_autores():
    limpiar_pantalla()

    #agregar_imagen_bienvenida("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/yo.jpg", root, "yo")
    #agregar_imagen_bienvenida("C:/Users/tavo_/OneDrive/Documentos/Trabajos IA/10Septiembre/Imagenes/black.jpg", root, "yo1")
    agregar_imagen_bienvenida("Imagenes/yo.jpg", root, "yo")
    agregar_imagen_bienvenida("Imagenes/black.jpg", root, "yo1")

    lbl_autores = ttk.Label(root, text="Autores del sistema", font=("Arial", 24))
    lbl_autores.pack(pady=20)

    autores_texto = "Datos personales \n"
    autores_texto += "Nombre: Gustavo Francisco Salgado Andrade.\nDirección: U HAB. Jose Maria Morelos y Pavon, Morelos Jojutla.\nTeléfono: 7774933706\nE-mail: l20091177@zacatepec.tecnm.mx \n \n \n"
    lbl_autores_texto = ttk.Label(root, text=autores_texto, font=("Arial", 18))
    lbl_autores_texto.pack(pady=5)

    autores_texto1 = "Datos personales \n"
    autores_texto1 += "Nombre: Blacky Salgado Andrade.\nDirección: U HAB. Jose Maria Morelos y Pavon, Morelos Jojutla.\nTeléfono: 7874933706\nE-mail: elmasperron@gmail.com"
    lbl_autores_texto1 = ttk.Label(root, text=autores_texto1, font=("Arial", 18))
    lbl_autores_texto1.pack(pady=5)

    btn_acerca_de = ttk.Button(root, text="Regresar", command=pantalla_acerca_de, image=flecha_icono, compound="left")
    btn_acerca_de.place(x=1380, y=600)


    
# Función para agregar imágenes en las esquinas de la pantalla de bienvenida
def agregar_imagen_bienvenida(ruta, parent_frame, esquina):
    img = Image.open(ruta)
    img = img.resize((150, 150), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    panel = tk.Label(parent_frame, image=img, background="#FFFFFF")
    panel.image = img

    if esquina == "nw":  # Superior izquierda
        panel.place(x=10, y=10)
    elif esquina == "ne":  # Superior derecha
        panel.place(x=1360, y=10)
    elif esquina == "yo":
        panel.place(x=200 ,y=100)
    elif esquina == "yo1":
        panel.place(x=200 ,y=300)
    elif esquina == "yo2":
        panel.place(x=200 ,y=500)

# Función para limpiar la pantalla
def limpiar_pantalla():
    for widget in root.winfo_children():
        widget.destroy()

# Iniciar con la pantalla de bienvenida
pantalla_bienvenida()

# Ejecutar el loop principal
root.mainloop()
