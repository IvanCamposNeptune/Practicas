from fastapi import FastAPI, HTTPException, Query
import uvicorn
from onu_config import unauthenticated_onu, state_onu

app = FastAPI()

#Ver onu no autenticadas
@app.get("/onu/unauthenticated/")
async def onu_unauthenticated():
    try:
        response = unauthenticated_onu()
        return response
    except Exception as e:
        raise e

#Ver id ocupados en una interfaz
@app.get("/onu/state_gpon_olt/")
async def onu_state_gpon_olt(shelf: int = Query(1),slot: int = Query(...,ge=1,le=2),pon: int = Query(...,ge=1,le=16)):
    try:
        response = state_onu(shelf,slot,pon)
        return response
    except Exception as e:
        raise e

# #Registro de onu
# @app.post("/onu/onu_register/")
# async def onu_register(shelf: int = Query(1),slot: int = Query(...,ge=1,le=2),pon: int = Query(...,ge=1,le=16),id: int = Query(...,ge=1,le=128),name: str = Query(...,min_length=1),sn: str = Query(...,min_length=1),vlan: int = Query(...,ge=1)):
#     try:
#         response = onu_create(shelf,slot,pon,id,name,sn,vlan)
#         return response
#     except Exception as e:
#         raise e
    
# #Registro de onu
# @app.delete("/onu/onu_delete/")
# async def onu_delete(shelf: int = Query(1),slot: int = Query(...,ge=1,le=2),pon: int = Query(...,ge=1,le=16),id: int = Query(...,ge=1,le=128)):
#     try:
#         response = onu_destroy(shelf,slot,pon,id)
#         return response
#     except Exception as e:
#         raise e
    

#Modulo de alta de internet

#Modulo de baja de internet



#Para conextarse directamente a esta ip localmente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)

# # Para que se conecte con la ip del servidor (Donde se ejecute)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)