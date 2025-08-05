from typing import Annotated
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

db_users = {
    "gregory" : {
        "id":"0",
        "username":"Gregory",
        "password":"12345#hash"
    },
    "melani": {
        "id":"1",
        "username":"melani",
        "password":"54321#hash"
    }    
}

app = FastAPI()

# Instanciamos Jinja2 para darle como directorio la carpeta "templates"
jinja2_template = Jinja2Templates(directory="templates")

def get_user(username:str, db:list):
    if username in db:
        return db[username]
    
def authenticate_user(password:str, password_plane:str):
    password_clean = password.split("#")[0]
    if password_plane == password_clean:
        return True
    return False
            

#Aca definimos la página inicial
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return jinja2_template.TemplateResponse("index.html", {"request": request})

#Definimos un dashboard
@app.get("/users/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return jinja2_template.TemplateResponse("dashboard.html", {"request": request})

## Importamos "Form" desde FastApi para indicar que el dato viene desde un formulario HTML.
## El Annotated importado desde Typing le permite a FastAPI saber de dónde sacar el dato y qué tipo es

@app.post("/users/login")
def username(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_data = get_user(username, db_users)
    if user_data == None:
        raise HTTPException(
            status_code=401,
            detail= "No está autorizado"
        )
    if not authenticate_user(user_data["password"], password):
        raise HTTPException(
            status_code=401,
            detail="No está autorizado"
        )
    return {
        "username" : username,
        "password" : password
    }