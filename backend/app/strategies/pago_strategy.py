from abc import ABC, abstractmethod
from decimal import Decimal
from backend.app.models.pago import MedioPago

class EstrategiaMedioPago(ABC):
    @abstractmethod
    def calcular_monto_final(self, monto_base: Decimal) -> Decimal:
        pass

class PagoEfectivoStrategy(EstrategiaMedioPago):
    """Efectivo: 10% de descuento"""
    DESCUENTO = Decimal("0.90")

    def calcular_monto_final(self, monto_base: Decimal) -> Decimal:
        return (monto_base * self.DESCUENTO).quantize(Decimal("0.01"))

class PagoTransferenciaStrategy(EstrategiaMedioPago):
    """Transferencia / Mercado Pago: Precio de lista sin recargo"""
    def calcular_monto_final(self, monto_base: Decimal) -> Decimal:
        return monto_base.quantize(Decimal("0.01"))

class PagoTarjetaStrategy(EstrategiaMedioPago):
    """Tarjeta: 10% de recargo"""
    RECARGO = Decimal("1.10")

    def calcular_monto_final(self, monto_base: Decimal) -> Decimal:
        return (monto_base * self.RECARGO).quantize(Decimal("0.01"))

class ProcesadorPagoContext:
    _ESTRATEGIAS = {
        MedioPago.EFECTIVO: PagoEfectivoStrategy(),
        MedioPago.TRANSFERENCIA: PagoTransferenciaStrategy(),
        MedioPago.MERCADO_PAGO: PagoTransferenciaStrategy(),
        MedioPago.TARJETA: PagoTarjetaStrategy(),
    }

    @classmethod
    def obtener_estrategia(cls, medio_pago: MedioPago | str) -> EstrategiaMedioPago:
        medio = MedioPago(medio_pago) if isinstance(medio_pago, str) else medio_pago
        return cls._ESTRATEGIAS.get(medio, PagoTransferenciaStrategy())