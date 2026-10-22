from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional

class MedioPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    TRANSFERENCIA = "TRANSFERENCIA"
    MERCADO_PAGO = "MERCADO_PAGO"
    TARJETA = "TARJETA"

class Pago:
    def __init__(
        self, 
        id_pago: int, 
        id_cuota: int, 
        id_usuario: int, 
        monto: Decimal, 
        fecha_pago: datetime, 
        medio_pago: MedioPago | str, 
        comprobante_ref: Optional[str] = None
    ):
        self.id_pago = id_pago
        self.id_cuota = id_cuota
        self.id_usuario = id_usuario
        self.monto = Decimal(str(monto))
        self.fecha_pago = fecha_pago
        self.medio_pago = MedioPago(medio_pago) if isinstance(medio_pago, str) else medio_pago
        self.comprobante_ref = comprobante_ref

    def validar_monto(self) -> bool:
        return self.monto > Decimal("0.00")