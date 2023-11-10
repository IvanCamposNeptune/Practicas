from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Configura las plantillas de Jinja2
templates = Jinja2Templates(directory="templates")

# Define una ruta para la página de inicio
@app.get("/")
async def read_home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# Define una ruta para la página "hija"
@app.get("/hija")
async def read_hija(request: Request):
    return templates.TemplateResponse("hija.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

