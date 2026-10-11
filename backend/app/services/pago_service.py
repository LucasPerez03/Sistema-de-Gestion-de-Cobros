from decimal import Decimal
from fastapi import HTTPException, status
from app.repositories.pago_repository import PagoRepository
from app.services.cuota_service import CuotaService
from app.schemas.pago import PagoCreate


class PagoService:
    def __init__(self):
        self.pago_repo = PagoRepository()
        self.cuota_service = CuotaService()

    def registrar_pago(self, datos_pago: PagoCreate, id_usuario_cobrador: int) -> dict:
        cuota = self.cuota_service.obtener_cuota_por_id(datos_pago.id_cuota)
        
        pagos_previos = self.pago_repo.obtener_por_cuota(datos_pago.id_cuota)
        total_pagado = sum(Decimal(str(p["monto"])) for p in pagos_previos)
        saldo_actual = Decimal(str(cuota["importe"])) - total_pagado

        if datos_pago.monto <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El monto a pagar debe ser mayor a cero."
            )

        if Decimal(str(datos_pago.monto)) > saldo_actual:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El monto excede el saldo restante de la cuota (${saldo_actual:.2f})."
            )

        datos_dict = datos_pago.model_dump()
        datos_dict["id_usuario"] = id_usuario_cobrador

        nuevo_pago = self.pago_repo.crear(datos_dict)

        nuevo_saldo = saldo_actual - Decimal(str(datos_pago.monto))
        self.cuota_service.actualizar_estado_cuota(
            id_cuota=cuota["id_cuota"],
            saldo_restante=nuevo_saldo,
            importe_total=Decimal(str(cuota["importe"]))
        )

        return nuevo_pago