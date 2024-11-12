import requests
import os
import re

# Reemplaza con tu clave de API de Pexels
api_key = 'RW7T1HOQ527gL7UXwwXhFWvrvlhcYcYwshNHZ4hWYG1cCCkTRmYci9Pt'

# Lista de términos de búsqueda para cada actividad
actividades = [
    'Correr', 'Saltar', 'Golpear', 'Observar', 'Pensar', 'Trabajo en equipo', 'Pasar la pelota', 
    'Patear', 'Nadar', 'Bucear', 'Defender', 'Atacar', 'Saltos de altura', 'Golpeo de balón', 
    'Sprints', 'Jugar al escondite', 'Control de balón', 'Marcar goles', 'Pasar la pelota con precisión', 
    'Atajar', 'Bloquear', 'Saltar obstáculos', 'Correr en intervalos', 'Desplazarse lateralmente', 'Agarre de balón', 
    'Concentrarse', 'Coordinar', 'Acelerar', 'Frenar', 'Realizar dribles', 'Tener reflejos rápidos', 
    'Tener resistencia', 'Entrenar', 'Hacer pesas', 'Zancadas', 'Escuchar al entrenador', 'Tomar decisiones rápidas', 
    'Jugar en equipo', 'Enfrentar al oponente', 'Poner resistencia', 'Ser paciente', 'Defender el gol', 
    'Tener agilidad', 'Mantener el enfoque', 'Girar', 'Correr sin parar', 'Aguantar dolor', 'Responder a la presión', 
    'Controlar la pelota con el pie', 'Driblar el balón', 'Interrumpir el pase', 'Reaccionar ante un pase', 
    'Mantener el equilibrio', 'Vencer la fatiga', 'Pase largo', 'Mantener la postura', 'Luchar por el balón', 
    'Hacer bloqueos', 'Realizar la defensa personal', 'Pase corto', 'Gritar indicaciones', 'Leer la jugada', 
    'Comer bien', 'Jugar bajo presión', 'Hacer una finta', 'Golpear la pelota de tenis', 'Hacer un saque', 
    'Estar atento', 'Tener reflejos', 'Correr con el balón', 'Tener velocidad', 'Entrar a la cancha', 
    'Luchar por la pelota', 'Atacar en equipo', 'Desplazarse rápido', 'Realizar un bloqueo efectivo', 
    'Dar instrucciones', 'Ganar confianza', 'Tener resistencia mental', 'Defender en el campo', 'Practicar tiros', 
    'Hacer movimientos tácticos', 'Tener disciplina', 'Colaborar en equipo', 'Posicionarse bien', 
    'Vigilar al oponente', 'Ayudar al compañero', 'Superar obstáculos', 'Rebotar el balón', 'Mantener la calma', 
    'Realizar un pase largo con precisión', 'Mantener una buena postura durante el juego', 
    'Afrontar una jugada de riesgo con calma'
]

# Función para limpiar el nombre de actividad y asegurarse de que es un nombre de archivo válido
def limpiar_nombre_archivo(nombre):
    return re.sub(r'[<>:"/\\|?*]', '_', nombre).replace(' ', '_')

# Crea la carpeta de imágenes si no existe
output_dir = "D:\\9no. Semestre ZACA\\Inteligencia Artificial\\SEG py\\Enfermedades-SistemaExperto\\Imagenes\\Actividad"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Buscar y descargar imágenes de Pexels
for actividad in actividades:
    # Agregar términos más deportivos en las búsquedas para mejorar la relevancia
    # Combina las actividades con palabras como "deportista", "entrenamiento", "deporte", etc.
    query = f"{actividad} deporte entrenamiento"

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=5"  # Obtener más imágenes
    headers = {'Authorization': api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'photos' in data and data['photos']:
            for i, photo in enumerate(data['photos']):
                image_url = photo['src']['original']
                image_data = requests.get(image_url).content

                # Limpiar el nombre del archivo
                nombre_archivo = f"{limpiar_nombre_archivo(actividad)}_{i+1}.jpg"

                # Guardar la imagen
                with open(os.path.join(output_dir, nombre_archivo), 'wb') as file:
                    file.write(image_data)
                print(f"Imagen de {actividad} descargada correctamente.")
        else:
            print(f"No se encontraron imágenes para {actividad}.")
    else:
        print(f"No se pudo obtener imagen para {actividad}.")
