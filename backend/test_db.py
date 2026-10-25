from backend.app.config.database import DatabaseConnection
from backend.app.models.usuario import Admin, Entrenador, ClienteUsuario
from backend.app.models.cliente import Cliente
from backend.app.models.servicio import Servicio
from backend.app.models.cuota import Cuota
from backend.app.models.pago import Pago

def probar_todo():
    print(" 1. Probando conexión a la Base de Datos (Singleton)...")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    assert db1 is db2, "Error: El patrón Singleton devolvió instancias distintas."
    print("    ¡Singleton funcionando! db1 y db2 son exactamente la misma instancia.")

    conn = db1.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT current_database();")
    db_nombre = cursor.fetchone()
    print(f"    Conectado exitosamente a PostgreSQL: '{db_nombre[0]}'")
    cursor.close()

    print("\n 2. Probando creación de Clases del Modelo POO...")
    admin = Admin(1, "admin@bypay.com", "pass123", "Lucas", "Perez")
    cliente = Cliente(1, "Juan", "Gomez", "40123456", "1122334455", "juan@mail.com", "1998-05-10")
    servicio = Servicio(1, "Pase Libre", 25000.00, "Entrenamiento libre")
    cuota = Cuota(1, cliente.id_cliente, servicio.id_servicio, "2026-10-01", servicio.precio, "2026-10-10")
    
    pago1 = Pago(1, cuota.id_cuota, admin.id_usuario, 15000.00, "2026-10-05", "TRANSFERENCIA", "REF-998877")
    cuota.agregar_pago(pago1)

    print(f"    Admin creado: {admin.nombre} {admin.apellido} - Menú: {admin.obtener_menu()}")
    print(f"    Cliente: {cliente.nombre_completo()}")
    print(f"    Cuota Importe: ${cuota.importe} | Pago registrado: ${pago1.monto} | Saldo Pendiente: ${cuota.calcular_saldo()}")
    print("\n ¡TODOS LOS MODELOS FUNCIONAN PERFECTAMENTE!")

if __name__ == '__main__':
    probar_todo()
    