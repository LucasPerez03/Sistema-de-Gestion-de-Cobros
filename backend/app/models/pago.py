from decimal import Decimal
from datetime import datetime
from typing import Optional

class Pago:
    def __init__(
        self, 
        id_pago: int, 
        id_cuota: int, 
        id_usuario: int, 
        monto: Decimal, 
        fecha_pago: datetime, 
        medio_pago: str, 
        comprobante_ref: Optional[str] = None
    ):
        self.id_pago = id_pago
        self.id_cuota = id_cuota
        self.id_usuario = id_usuario
        self.monto = Decimal(str(monto))
        self.fecha_pago = fecha_pago
        self.medio_pago = medio_pago
        self.comprobante_ref = comprobante_ref