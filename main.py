import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
 
from sensors import SensorCVD, SensorConfig
from database import DataBase
 
# Configuración de la página
st.set_page_config(
   page_title="Monitor CVD",
   page_icon="🔧",
   layout="wide",
   initial_sidebar_state="expanded"
)
 
# Configuración de sensores
SENSORES_CONFIG = {
   'temperatura': SensorConfig(
       nombre="Temperatura de Cámara",
       unidad="°C",
       rango=(200, 800),
       precision=1,
       color="#FF4B4B",
       limites_alarma={'bajo': 250, 'alto': 750}
   ),
   'presion': SensorConfig(
       nombre="Presión de Proceso",
       unidad="mTorr",
       rango=(1, 1000),
       precision=2,
       color="#4B4BFF",
       limites_alarma={'bajo': 10, 'alto': 900}
   ),
   'flujo_gas': SensorConfig(
       nombre="Flujo de Gas Precursor",
       unidad="sccm",
       rango=(0, 100),
       precision=1,
       color="#4BFF4B",
       limites_alarma={'bajo': 5, 'alto': 90}
   )
}
 
class MonitorCVD:
   def __init__(self):
       self.db = DataBase('data/sensor_data.db')
       self.sensores = {
           nombre: SensorCVD(config)
           for nombre, config in SENSORES_CONFIG.items()
       }
  
   def ejecutar(self):
       st.title("Monitor de Proceso CVD")
      
       # Panel de control en sidebar
       with st.sidebar:
           st.header("Panel de Control")
           intervalo = st.slider("Intervalo de actualización (s)", 1, 10, 2)
           modo_demo = st.checkbox("Modo Demostración", True)
          
           st.divider()
           st.markdown("""
               ### Información del Proceso
               Este sistema monitorea los parámetros críticos en el proceso
               de Deposición Química de Vapor (CVD) para la fabricación de
               semiconductores.
           """)
 
       # Layout principal
       col1, col2, col3 = st.columns(3)
       graficas = st.container()
      
       # Contenedores para actualización en tiempo real
       contenedores = {
           'temperatura': col1.empty(),
           'presion': col2.empty(),
           'flujo_gas': col3.empty()
       }
      
       while modo_demo:
           for nombre, sensor in self.sensores.items():
               # Lectura del sensor
               valor = sensor.leer()
               estado = sensor.verificar_alarma(valor)
              
               # Guardar en base de datos
               self.db.guardar_lectura(nombre, valor, estado)
              
               # Actualizar visualización
               contenedor = contenedores[nombre]
               config = SENSORES_CONFIG[nombre]
              
               contenedor.metric(
                   label=config.nombre,
                   value=f"{valor} {config.unidad}",
                   delta=f"{valor - sensor.valor_base:.1f}",
                   delta_color="inverse" if estado != 'normal' else "normal"
               )
          
           # Actualizar gráficas
           with graficas:
               self.actualizar_graficas()
          
           time.sleep(intervalo)
  
   def actualizar_graficas(self):
       # Crear tabs para diferentes vistas
       tab1, tab2 = st.tabs(["Tiempo Real", "Histórico"])
      
       with tab1:
           # Gráfica en tiempo real
           fig = go.Figure()
           for nombre, sensor in self.sensores.items():
               datos = self.db.obtener_historico(nombre, 100)
               config = SENSORES_CONFIG[nombre]
              
               fig.add_trace(go.Scatter(
                   x=datos['timestamp'],
                   y=datos['valor'],
                   name=config.nombre,
                   line=dict(color=config.color)
               ))
          
           fig.update_layout(
               title="Monitoreo en Tiempo Real",
               height=400,
               margin=dict(l=0, r=0, t=30, b=0)
           )
          
           st.plotly_chart(fig, use_container_width=True)
 
if __name__ == "__main__":
   monitor = MonitorCVD()
   monitor.ejecutar()