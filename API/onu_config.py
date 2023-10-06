from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import json



#Onu no autenticadas
def unauthenticated_onu():

    #Abre el archivo json para simular la respuesta y ya nadamas hay que mostrarla en la pagina.
    with open ("uncfg_onus.json") as jsonfile:
        response = json.load(jsonfile)

    return response



#Estado de la interface gpon
def state_onu(shelf:int, slot:int, pon:int):
    
    print(shelf,slot,pon) #Este nomas pa que veas los datos que se meten jsjs

    #Abre el archivo json para simular la respuesta y ya nadamas hay que mostrarla en la pagina.
    with open ("json_onu_state.json") as jsonfile:
        response = json.load(jsonfile)

    return response




# #Crear contrato de internet
# def onu_create(shelf:int,slot:int,pon:int,id:int,name:str,sn:str,vlan:int):

    # telnet_client = TelnetConnection()

    # if telnet_client.connect():
    #     try:
            
    #         #Privilegios de configuracion global
    #         telnet_client.send_command("conf ter")
    #         print("\tEstas en la configuracion global...")

    #         print(f"Se ingresa a la Interface: {shelf}/{slot}/{pon} ")

    #         command = f"interface gpon-olt_{shelf}/{slot}/{pon}"
    #         telnet_client.send_command(command)


    #         #Asignando id y numero de serie y tipo de onu
    #         #sn = "GPON00AC7F68"
    #         type = 'ZTE-F625' 

    #         command = f"onu {id} type {type} sn {sn}"

    #         telnet_client.send_command(command)

    #         print(f"Se ingreso el id {id} y el sn {sn}")


    #         #Saliendo de la interfaz
    #         print("\tSaliendo de la configuracion de interfaz")
    #         telnet_client.send_command("exit")


    #         #Ingresar a la onu con el id que se acaba de crear
    #         telnet_client.send_command(f"interface gpon-onu_{shelf}/{slot}/{pon}:{id}")
    #         print("\tSe ingreso a la interfaz de la onu especifica con su id...")

    #         #Asignando nombre y descripcion a la interfaz de la ONU
    #         descripcion = name

    #         telnet_client.send_command(f"name {name}")
    #         telnet_client.send_command(f"description {descripcion}")

    #         print(f"Se agrego el nombre {name} y la descripcion {descripcion}")


    #         #Asignando ancho de banda y perfiles de subida y bajada
    #         telnet_client.send_command("sn-bind enable sn")

    #         telnet_client.send_command(f"tcont 1 name {name} profile 5Mb")
            
    #         telnet_client.send_command(f"gemport 1 name {name} unicast tcont 1 dir both")
            
    #         telnet_client.send_command("gemport 1 traffic-limit downstream 5Mb upstream 5Mb")

    #         telnet_client.send_command("switchport mode hybrid vport 1")

    #         print("Se ingreso el ancho de banda y el trafico de subida y bajada")


    #         #Ingresando la vlan
    #         #vlan = 601

    #         telnet_client.send_command(f"service-port 1 vport 1 user-vlan {vlan} vlan {vlan}")
            
    #         telnet_client.send_command(f"service-port 1 description {name}")
            
    #         #Saliendo de la configuracion de la interfaz
    #         telnet_client.send_command(f"exit")
            
    #         #Configurar la administracion de la ONU
    #         telnet_client.send_command(f"pon-onu-mng gpon-onu_{shelf}/{slot}/{pon}:{id}")

    #         telnet_client.send_command(f"service {name} type internet gemport 1 vlan {vlan}")

    #         #Saliendo de la administracion de la ONU
    #         telnet_client.send_command("exit")

    #         #Ingresar a la onu con el id que se acaba de crear
    #         telnet_client.send_command(f"interface gpon-onu_{shelf}/{slot}/{pon}:{id}")
            
    #         #Activando el servicion de internet
    #         telnet_client.send_command("state ready")
    #         #telnet_client.send_command("state deactive") #desactiva el servicion de internet



    #         server_response = json_onu_register()

    #         return server_response


    #         telnet_client.close()
        
        # except Exception as e:
        #     raise HTTPException(status_code=400, detail="Error de validacion de datos...")



# def onu_destroy(shelf:int,slot:int,pon:int,id:int):
#     telnet_client = TelnetConnection()

#     if telnet_client.connect():
#         try:

#             #Privilegios de configuracion global
#             telnet_client.send_command("conf ter")
#             print("\tEstas en la configuracion global...")

#             print(f"Se ingresa a la Interface: {shelf}/{slot}/{pon} ")

#             command = f"interface gpon-olt_{shelf}/{slot}/{pon}"
#             telnet_client.send_command(command)


#             #Eliminando la configuracion de la ONU
#             command = f" no onu {id}"

#             #Enviando datos
#             telnet_client.send_command(command)

#             server_response = json_onu_destroy()

#             return server_response

#             telnet_client.close()
        
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))


# if __name__ == "__main__":
#     onu_register(1,1,7,10,"3312_IVAN")