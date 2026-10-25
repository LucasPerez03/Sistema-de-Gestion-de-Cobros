from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import (
    auth_router,
    cliente_router,
    cuota_router,
    pago_router,
    servicio_router,
    usuario_router,
)

app = FastAPI(
    title="BYPay API",
    description="Sistema de gestión de cuotas y pagos",
    version="1.0.0",
)

# Configuración de CORS para conectar con el Frontend 
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(auth_router.router)
app.include_router(cliente_router.router)
app.include_router(cuota_router.router)
app.include_router(pago_router.router)
app.include_router(servicio_router.router)
app.include_router(usuario_router.router)

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "BYPay API funcionando correctamente"}