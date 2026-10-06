from app.models.pago import Pago

class Cuota:
    def __init__(self, id_cuota, id_cliente, id_servicio, periodo, importe, fecha_vencimiento, estado="PENDIENTE"):
        self.id_cuota = id_cuota
        self.id_cliente = id_cliente
        self.id_servicio = id_servicio
        self.periodo = periodo
        self.importe = importe
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.pagos = []

    def agregar_pago(self, pago: Pago):
        self.pagos.append(pago)

    def calcular_saldo(self):
        total_pagado = sum(float(pago.monto) for pago in self.pagos)
        return float(self.importe) - total_pagado
    