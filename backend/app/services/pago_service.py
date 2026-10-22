from datetime import datetime
from decimal import Decimal
from typing import List
from fastapi import HTTPException, status
from backend.app.models.pago import Pago
from backend.app.repositories.pago_repository import PagoRepository
from backend.app.services.cuota_service import CuotaService
from backend.app.schemas.pago import PagoCreate
from backend.app.strategies.pago_strategy import ProcesadorPagoContext


class PagoService:
    def __init__(self):
        self.pago_repo = PagoRepository()
        self.cuota_service = CuotaService()

    def registrar_pago(self, datos_pago: PagoCreate, id_usuario_cobrador: int) -> dict:
        cuota_dict = self.cuota_service.obtener_cuota_por_id(datos_pago.id_cuota)
        cuota_entidad = self.cuota_service.construir_entidad_cuota(cuota_dict)
        
        saldo_actual = cuota_entidad.calcular_saldo()
        monto_imputado = Decimal(str(datos_pago.monto))

        # Creamos la instancia de dominio Pago para validar con su propio método
        nuevo_pago_entidad = Pago(
            id_pago=0,
            id_cuota=datos_pago.id_cuota,
            id_usuario=id_usuario_cobrador,
            monto=monto_imputado,
            fecha_pago=datetime.now(),
            medio_pago=datos_pago.medio_pago,
            comprobante_ref=datos_pago.comprobante_ref,
        )

        if not nuevo_pago_entidad.validar_monto():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El monto a pagar debe ser mayor a cero."
            )

        if monto_imputado > saldo_actual:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El monto excede el saldo restante de la cuota (${saldo_actual:.2f})."
            )

        # Aplicamos el Patrón Strategy según el medio de pago 
        estrategia = ProcesadorPagoContext.obtener_estrategia(datos_pago.medio_pago)
        monto_con_ajuste = estrategia.calcular_monto_final(monto_imputado)

        datos_dict = datos_pago.model_dump()
        datos_dict["id_usuario"] = id_usuario_cobrador

        pago_creado = self.pago_repo.crear(datos_dict)

        # Usamos la composición de nuestro modelo de dominio para actualizar el estado de la cuota
        cuota_entidad.agregar_pago(nuevo_pago_entidad)
        self.cuota_service.cuota_repo.actualizar(
            cuota_entidad.id_cuota, 
            {"estado": cuota_entidad.estado.value}
        )

        pago_creado["monto_cobrado_con_estrategia"] = monto_con_ajuste
        return pago_creado

    def obtener_historial_pagos(self) -> List[dict]:
        return self.pago_repo.obtener_todos()

    def obtener_pagos_por_cliente(self, id_cliente: int) -> List[dict]:
        return self.pago_repo.obtener_por_cliente(id_cliente)