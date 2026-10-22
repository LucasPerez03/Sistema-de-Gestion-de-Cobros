from decimal import Decimal
from datetime import date
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from backend.app.models.pago import Pago
    from backend.app.models.servicio import Servicio

class EstadoCuota(str, Enum):
    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    VENCIDA = "VENCIDA"
    ANULADA = "ANULADA"
    PARCIAL = "PARCIAL"

class Cuota:
    def __init__(
        self, 
        id_cuota: int, 
        id_cliente: int, 
        id_servicio: int, 
        periodo: str, 
        importe: Decimal, 
        fecha_vencimiento: date, 
        estado: EstadoCuota | str = EstadoCuota.PENDIENTE,
        servicio: Optional["Servicio"] = None  # Agregación con Servicio
    ):
        self.id_cuota = id_cuota
        self.id_cliente = id_cliente
        self.id_servicio = id_servicio
        self.periodo = periodo
        self.importe = Decimal(str(importe))
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = EstadoCuota(estado) if isinstance(estado, str) else estado
        self.servicio = servicio
        self.pagos: List["Pago"] = []          # Composición con Pago

    def agregar_pago(self, pago: "Pago") -> None:
        if not pago.validar_monto():
            raise ValueError("El monto del pago debe ser mayor a cero.")
        self.pagos.append(pago)
        self.actualizar_estado()

    def calcular_saldo(self) -> Decimal:
        total_pagado = sum((Decimal(str(pago.monto)) for pago in self.pagos), Decimal("0.00"))
        return self.importe - total_pagado

    def marcar_pagada(self) -> None:
        self.estado = EstadoCuota.PAGADA

    def marcar_vencida(self) -> None:
        if self.estado != EstadoCuota.PAGADA:
            self.estado = EstadoCuota.VENCIDA

    def actualizar_estado(self) -> None:
        saldo = self.calcular_saldo()
        if saldo <= Decimal("0.00"):
            self.marcar_pagada()
        elif saldo < self.importe:
            self.estado = EstadoCuota.PARCIAL
        elif self.fecha_vencimiento < date.today():
            self.marcar_vencida()
        else:
            self.estado = EstadoCuota.PENDIENTE