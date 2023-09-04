def generar():
    
    import json

    lista_personas = []

    diccionario_temporal = {
        'nombre':[],
        'edad':[],
        'ciudad':[]
    } # Para guardar las claves y valores temporales

    cont = 0

    with open("personas.txt", "r") as fichero:
            lines = fichero.readlines()
        
            for line in lines:
                line = line.strip()
                            
                if not line:
                    continue
                if line.startswith('Archivo') or line.startswith('-'):
                    continue

                #print(line)
                    
                clave, valor = line.split(':') # Divide la linea actual una vez por ":" haciendo que lo primero sea la clave y lo demas se mantiene en valor

                #print(clave,valor)

                if line.startswith('nombre'):
                    diccionario_temporal['nombre'] = valor.strip()
                    cont+=1
                if line.startswith('edad'):
                    diccionario_temporal['edad'] = valor.strip()
                    cont+=1
                if line.startswith('ciudad'):
                    diccionario_temporal['ciudad'] = valor.strip()
                    cont+=1
                    
                #print(cont)
                
                if cont == 3:
                    #print("el contador llego a 3")
                    cont = 0
                    #print(diccionario_temporal)
                    lista_personas.append(diccionario_temporal.copy()) # Muy importante hacer copia, por que se apunta al objeto como tal,  para no modificar el objeto

                    

    print(lista_personas)

    with open("personas.json", "w") as jsonfile:
        json.dump(lista_personas,jsonfile)