class Pago:
    def __init__(self, id_pago, id_cuota, id_usuario, monto, fecha_pago, medio_pago, comprobante_ref=None):
        self.id_pago = id_pago
        self.id_cuota = id_cuota
        self.id_usuario = id_usuario 
        self.monto = monto 
        self.fecha_pago = fecha_pago
        self.medio_pago = medio_pago
        self.comprobante_ref = comprobante_ref
        