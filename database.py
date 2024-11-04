import sqlite3
import pandas as pd
from datetime import datetime
import os

class DataBase:
    def __init__(self, db_path: str):
        self.db_path = db_path

        os.makedirs(os.path.dirname(self.db_path), exist_ok= True)
        self.inicializar_db()
        
    def inicializar_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS lecturas (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, 
                    sensor TEXT, 
                    valor REAL, 
                    estado TEXT)
                    """)
    def guardar_lectura(self, sensor: str, valor: float, estado: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                    INSERT INTO lecturas(timestamp, sensor, valor, estado)
                    VALUES (?, ?, ?, ?)
                        """, (datetime.now(), sensor, valor, estado))
    def obtener_historico(self, sensor: str, limite: int = 1000) -> pd.DataFrame:
        query = """
            SELECT timestamp, valor, estado
            FROM lecturas
            WHERE sensor = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn, params=(sensor, limite))