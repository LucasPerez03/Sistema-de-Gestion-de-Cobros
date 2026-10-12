import bcrypt
from decimal import Decimal
from datetime import date, timedelta
from backend.app.config.database import DatabaseConnection

def hash_password(password: str) -> str:
    """Encripta la contraseña para que el login reconozca la hash."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def sembrar_datos():
    db = DatabaseConnection()
    conn = db.get_connection()
    
    with conn.cursor() as cursor:
        print("Iniciando carga de datos de prueba...")

        # 1. Crear Usuario Admin por defecto
        pass_admin = hash_password("admin123")
        cursor.execute("""
            INSERT INTO usuarios (email, password, nombre, apellido, rol, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING id_usuario;
        """, ("admin@bypay.com", pass_admin, "Administrador", "Sistema", "ADMIN", True))
        
        row_admin = cursor.fetchone()
        print("-> Usuario Admin creado (Email: admin@bypay.com | Pass: admin123)")

        # 2. Crear Cliente de prueba
        cursor.execute("""
            INSERT INTO clientes (nombre, apellido, dni, telefono, email, fecha_nacimiento, estado)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            ON CONFLICT (email) DO NOTHING
            RETURNING id_cliente;
        """, ("Juan", "Pérez", "40123456", "1122334455", "juan.perez@example.com", date(1998, 5, 12)))
        
        row_cliente = cursor.fetchone()
        id_cliente = row_cliente[0] if row_cliente else 1
        print("-> Cliente de prueba creado.")

        # 3. Crear Servicio de prueba
        cursor.execute("""
            INSERT INTO servicios (nombre, precio, descripcion, estado)
            VALUES (%s, %s, %s, TRUE)
            RETURNING id_servicio;
        """, ("Pase Libre Gimnasio", Decimal("15000.00"), "Acceso ilimitado a sala de musculación"))
        
        row_servicio = cursor.fetchone()
        id_servicio = row_servicio[0] if row_servicio else 1
        print("-> Servicio de prueba creado.")

        # 4. Crear Cuota de prueba
        cursor.execute("""
            INSERT INTO cuotas (id_cliente, id_servicio, periodo, importe, fecha_vencimiento, estado)
            VALUES (%s, %s, %s, %s, %s, 'PENDIENTE');
        """, (id_cliente, id_servicio, "2026-10", Decimal("15000.00"), date.today() + timedelta(days=10)))
        print("-> Cuota de prueba asociada creada.")

        conn.commit()
        print("\n¡Datos iniciales cargados con éxito!")

if __name__ == "__main__":
    sembrar_datos()