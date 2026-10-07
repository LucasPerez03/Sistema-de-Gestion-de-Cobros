from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BYPay API",
    description="API REST para gestion de clientes, servicios y cuotas"
)

origins = [
    "http://localhost:5173", 
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "message": "Bienvenido a la API de ByPay 🚀"
    }