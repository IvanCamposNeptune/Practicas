# import sqlite3
# from pydantic import BaseModel, ValidationError
# import json
# from generar_json import generar

# from fastapi import FastAPI, HTTPException
# import uvicorn


# if __name__ == '__main__': # Comprueba que la ejecucion del programa sea la principal
#     generar()



# # Define un modelo Pydantic para validar los datos de una persona
# class PersonaModel(BaseModel):
#     nombre: str
#     edad: int
#     ciudad: str

# # # Lista de personas como diccionarios
# # personas = [
# #     {
# #         'nombre': 'Fer',
# #         'edad': 22,
# #         'ciudad': 'Tehotihuacan'
# #     },
# #     {
# #         'nombre': 'Ivan',
# #         'edad': '25h',
# #         'ciudad': 'Pachuca'
# #     },
# #     {
# #         'nombre': 'Vanessa',
# #         'edad': 25,
# #         'ciudad': 'Pachuca'
# #     }
# # ]

# # #Creando fichero json de la lista de diccionarios personas
# # with open ("personas.json","w") as jsonfile:
# #     json.dump(personas,jsonfile)


# # Conectar a la base de datos SQLite
# conn = sqlite3.connect('prueba.db')
# cursor = conn.cursor()



# # Crear una tabla para almacenar los datos de las personas (si no existe)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS personas (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nombre TEXT,
#         edad INTEGER,
#         ciudad TEXT
#     )
# ''')




# try:

#     #Abriendo el fichero json creado
#     with open ("personas.json") as jsonfile:
#         datos = json.load(jsonfile)

#     # for info in datos: # Buscando por nombre para verificar
#     #     if info['nombre'] == 'Fer':
#     #         print(info["nombre"],info["edad"],info["ciudad"]) 



#     for persona_data in datos:
        
#         try:
#             # Valida con el modelo la estructura
#             info_persona = PersonaModel(**persona_data) 

#             cursor.execute('INSERT INTO personas (nombre, edad, ciudad) VALUES (?, ?, ?)', (info_persona.nombre, info_persona.edad, info_persona.ciudad))
#             conn.commit()  # Commitea el registro si no hay errores

#             print(f"Registro insertado: {info_persona}")

#         except ValidationError as e:
#             print(f"Error de validación: {e}")
#         except sqlite3.Error as db_error:
#             conn.rollback()  # Revierte los cambios en caso de error de base de datos
#             print(f"Error de base de datos: {db_error}")



#     # Guarda los cambios y cierra la conexión
#     conn.commit()
#     conn.close()

# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     conn.close()



# app = FastAPI()


# # Ruta para crear un nuevo usuario
# @app.post("/persona/")
# def create_user(nombre:str, edad:int, ciudad:str):
#     try:
#         cursor.execute('INSERT INTO personas (nombre, edad, ciudad) VALUES (?, ?, ?)', (info_persona.nombre, info_persona.edad, info_persona.ciudad))
#         conn.commit()  # Commitea el registro si no hay errores
#         print(f"Registro insertado: nombre:{nombre} edad:{edad} ciudad:{ciudad}")
#     except sqlite3.Error as db_error:
#             conn.rollback()  # Revierte los cambios en caso de error de base de datos
#             print(f"Error de base de datos: {db_error}")


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)



import sqlite3
import json
from pydantic import BaseModel, ValidationError
from fastapi import FastAPI, HTTPException, Query
from generar_json import generar

if __name__ == '__main__': # Comprueba que la ejecucion del programa sea la principal
    generar()




class PersonaModel(BaseModel):
    nombre: str
    edad: int
    ciudad: str



conn = sqlite3.connect('prueba.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad INTEGER,
        ciudad TEXT
    )
''')

try:
    with open("personas.json") as jsonfile:
        datos = json.load(jsonfile)

    for persona_data in datos:
        try:
            info_persona = PersonaModel(**persona_data)
            cursor.execute('INSERT INTO personas (nombre, edad, ciudad) VALUES (?, ?, ?)', (info_persona.nombre, info_persona.edad, info_persona.ciudad))
            conn.commit()
            print(f"Registro insertado: {info_persona}")
        except Exception as e:
            print(f"Error de validación o base de datos: {e}")

except Exception as e:
    print(f"Error al cargar datos desde JSON: {e}")

finally:
    conn.close()



app = FastAPI()

# Función para crear una nueva persona
@app.post("/persona/")
async def create_user(nombre: str = Query(..., min_length=1), edad: int = Query(..., ge=0), ciudad: str = Query(..., min_length=1)):
    try:
        persona_data = {"nombre": nombre, "edad": edad, "ciudad": ciudad}
        info_persona = PersonaModel(**persona_data)

        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()
        
        # Inserta la nueva persona en la base de datos
        cursor.execute('INSERT INTO personas (nombre, edad, ciudad) VALUES (?, ?, ?)', (info_persona.nombre, info_persona.edad, info_persona.ciudad))
        conn.commit()
        conn.close()
        
        return {"message": "Persona creada exitosamente"}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"Error de base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")






# Función decorada para mostrar las personas en la base de datos
@app.get("/mostrar_personas/")
def get_personas():
    try:
        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()
        
        # Consulta SQL para obtener todas las personas
        cursor.execute('SELECT nombre, edad, ciudad FROM personas')
        personas = cursor.fetchall()
        
        # Procesa los resultados de la consulta
        resultado = []
        for persona in personas:
            nombre, edad, ciudad = persona
            resultado.append({"nombre": nombre, "edad": edad, "ciudad": ciudad})
        
        conn.close()
        
        return resultado
    
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")




# Ruta para buscar personas por nombre
@app.get("/buscar_persona/")
def buscar_persona(nombre: str):
    try:
        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()
        
        # Consulta SQL para buscar personas por nombre
        cursor.execute('SELECT nombre, edad, ciudad FROM personas WHERE nombre = ?', (nombre,))
        personas = cursor.fetchall()
        
        conn.close()
        
        if not personas:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        
        # Procesa los resultados de la consulta
        resultado = []
        for persona in personas:
            nombre, edad, ciudad = persona
            resultado.append({"nombre": nombre, "edad": edad, "ciudad": ciudad})
        
        return resultado
    except Exception as e:
        print(f"Error al buscar en la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")



# Ruta para eliminar una persona por nombre
@app.delete("/eliminar_persona/")
def eliminar_persona(nombre: str):
    try:
        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()
        
        # Consulta SQL para eliminar una persona por nombre
        cursor.execute('DELETE FROM personas WHERE nombre = ?', (nombre,))
        conn.commit()
        
        conn.close()
        
        # Verifica si se eliminó alguna fila (persona)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        
        return {"message": f"Persona con nombre '{nombre}' eliminada exitosamente"}
    except Exception as e:
        print(f"Error al eliminar de la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")




# #Para escuchar las peticiones en esta ip especifica
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


#Para escuchar las peticiones en la ip de este equipo sobre ese puerto
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
