from decimal import Decimal
from datetime import date
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.pago import Pago

class Cuota:
    def __init__(
        self, 
        id_cuota: int, 
        id_cliente: int, 
        id_servicio: int, 
        periodo: str, 
        importe: Decimal, 
        fecha_vencimiento: date, 
        estado: str = "PENDIENTE"
    ):
        self.id_cuota = id_cuota
        self.id_cliente = id_cliente
        self.id_servicio = id_servicio
        self.periodo = periodo
        self.importe = Decimal(str(importe))
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.pagos: List["Pago"] = []

    def agregar_pago(self, pago: "Pago") -> None:
        self.pagos.append(pago)
        self.actualizar_estado()

    def calcular_saldo(self) -> Decimal:
        total_pagado = sum((Decimal(str(pago.monto)) for pago in self.pagos), Decimal("0.00"))
        return self.importe - total_pagado

    def actualizar_estado(self) -> None:
        saldo = self.calcular_saldo()
        if saldo <= 0:
            self.estado = "PAGADA"
        elif saldo < self.importe:
            self.estado = "PARCIAL"
        else:
            self.estado = "PENDIENTE"