import psycopg2

from app.config.settings import settings


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connection = None
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        try:
            self._connection = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
            print("Conexion a la base de datos establecida exitosamente.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise e

    def get_connection(self):
        if self._connection is None or self._connection.closed != 0:
            self._connect()
        return self._connection

    def close_connection(self):
        if self._connection is not None and self._connection.closed == 0:
            self._connection.close()
            print("Conexion a la base de datos cerrada exitosamente.")
