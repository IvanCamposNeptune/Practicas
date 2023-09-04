import sqlite3
from pydantic import BaseModel, ValidationError
import json
from generar_json import generar

if __name__ == '__main__': # Comprueba que la ejecucion del programa sea la principal
    generar()

# Define un modelo Pydantic para validar los datos de una persona
class PersonaModel(BaseModel):
    nombre: str
    edad: int
    ciudad: str

# # Lista de personas como diccionarios
# personas = [
#     {
#         'nombre': 'Fer',
#         'edad': 22,
#         'ciudad': 'Tehotihuacan'
#     },
#     {
#         'nombre': 'Ivan',
#         'edad': '25h',
#         'ciudad': 'Pachuca'
#     },
#     {
#         'nombre': 'Vanessa',
#         'edad': 25,
#         'ciudad': 'Pachuca'
#     }
# ]

# #Creando fichero json de la lista de diccionarios personas
# with open ("personas.json","w") as jsonfile:
#     json.dump(personas,jsonfile)


# Conectar a la base de datos SQLite
conn = sqlite3.connect('prueba.db')
cursor = conn.cursor()



# Crear una tabla para almacenar los datos de las personas (si no existe)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad INTEGER,
        ciudad TEXT
    )
''')




try:

    #Abriendo el fichero json creado
    with open ("personas.json") as jsonfile:
        datos = json.load(jsonfile)

    # for info in datos: # Buscando por nombre para verificar
    #     if info['nombre'] == 'Fer':
    #         print(info["nombre"],info["edad"],info["ciudad"]) 



    for persona_data in datos:
        
        try:
            # Valida con el modelo la estructura
            info_persona = PersonaModel(**persona_data) 

            cursor.execute('INSERT INTO personas (nombre, edad, ciudad) VALUES (?, ?, ?)', (info_persona.nombre, info_persona.edad, info_persona.ciudad))
            conn.commit()  # Commitea el registro si no hay errores

            print(f"Registro insertado: {info_persona}")

        except ValidationError as e:
            print(f"Error de validación: {e}")
        except sqlite3.Error as db_error:
            conn.rollback()  # Revierte los cambios en caso de error de base de datos
            print(f"Error de base de datos: {db_error}")



    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()

except Exception as e:
    print(f"Error: {e}")

finally:
    conn.close()



