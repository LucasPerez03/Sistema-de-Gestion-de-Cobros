import bcrypt
from decimal import Decimal
from datetime import date, timedelta
from backend.app.config.database import DatabaseConnection

def hash_password(password: str) -> str:
    """Encripta la contraseña para que el login reconozca el hash."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def sembrar_datos():
    db = DatabaseConnection()
    conn = db.get_connection()
    
    try:
        with conn.cursor() as cursor:
            print("Iniciando carga de datos de prueba...")

            # 1. Crear Usuario Admin y Entrenador por defecto
            pass_default = hash_password("admin123")
            cursor.execute("""
                INSERT INTO usuarios (email, password, nombre, apellido, rol, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING id_usuario;
            """, ("admin@bypay.com", pass_default, "Lucas", "Pérez", "ADMIN", True))
            print("-> Usuario Admin asegurado (Email: admin@bypay.com | Pass: admin123)")

            cursor.execute("""
                INSERT INTO usuarios (email, password, nombre, apellido, rol, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
            """, ("entrenador@bypay.com", pass_default, "Carlos", "Gómez", "ENTRENADOR", True))
            print("-> Usuario Entrenador asegurado (Email: entrenador@bypay.com | Pass: admin123)")

            # 2. Crear Cliente de prueba (ON CONFLICT sobre dni)
            cursor.execute("""
                INSERT INTO clientes (nombre, apellido, dni, telefono, email, fecha_nacimiento, estado)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                ON CONFLICT (dni) DO NOTHING
                RETURNING id_cliente;
            """, ("Juan", "Pérez", "40123456", "1122334455", "juan.perez@example.com", date(1998, 5, 12)))
            
            row_cliente = cursor.fetchone()
            if row_cliente:
                id_cliente = row_cliente[0]
            else:
                cursor.execute("SELECT id_cliente FROM clientes WHERE dni = %s;", ("40123456",))
                id_cliente = cursor.fetchone()[0]
            print(f"-> Cliente de prueba asegurado (ID: {id_cliente}).")

            # 2b. Crear Usuario con rol CLIENTE vinculado al cliente de prueba
            cursor.execute("""
                INSERT INTO usuarios (email, password, nombre, apellido, rol, estado, id_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
            """, ("juan.perez@example.com", pass_default, "Juan", "Pérez", "CLIENTE", True, id_cliente))
            print("-> Usuario Cliente asegurado (Email: juan.perez@example.com | Pass: admin123)")

            # 3. Crear Servicio de prueba
            cursor.execute("""
                INSERT INTO servicios (nombre, precio, descripcion, estado)
                VALUES (%s, %s, %s, TRUE)
                ON CONFLICT (nombre) DO NOTHING
                RETURNING id_servicio;
            """, ("Pase Libre Gimnasio", Decimal("15000.00"), "Acceso ilimitado a sala de musculación"))
            
            row_servicio = cursor.fetchone()
            if row_servicio:
                id_servicio = row_servicio[0]
            else:
                cursor.execute("SELECT id_servicio FROM servicios WHERE nombre = %s;", ("Pase Libre Gimnasio",))
                id_servicio = cursor.fetchone()[0]
            print(f"-> Servicio de prueba asegurado (ID: {id_servicio}).")

            # 4. Crear Cuota de prueba (ON CONFLICT sobre cliente, servicio y periodo)
            cursor.execute("""
                INSERT INTO cuotas (id_cliente, id_servicio, periodo, importe, fecha_vencimiento, estado)
                VALUES (%s, %s, %s, %s, %s, 'PENDIENTE')
                ON CONFLICT (id_cliente, id_servicio, periodo) DO NOTHING;
            """, (id_cliente, id_servicio, "2026-10", Decimal("15000.00"), date.today() + timedelta(days=10)))
            print("-> Cuota de prueba asociada asegurada.")

            conn.commit()
            print("\n¡Datos iniciales cargados con éxito!")
    except Exception as e:
        conn.rollback()
        print(f"Error cargando datos semilla: {e}")
        raise

if __name__ == "__main__":
    sembrar_datos()