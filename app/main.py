from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.usuario_router import router as usuario_router
from app.routers.cliente_router import router as cliente_router
from app.routers.servicio_router import router as servicio_router
from app.routers.cuota_router import router as cuota_router

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

# Registro de routers
app.include_router(usuario_router)
app.include_router(cliente_router)
app.include_router(servicio_router)
app.include_router(cuota_router)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "message": "Bienvenido a la API de ByPay 🚀"
    }