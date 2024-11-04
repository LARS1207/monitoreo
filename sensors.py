import random 
import time 
from  dataclasses import dataclass
from typing import Tuple, Dict

@dataclass
class SensorConfig:
    nombre: str 
    unidad: str
    rango: Tuple[float, float]
    precision: int
    color: str 
    limites_alarma: Dict[str,float]

    class SensorCVD:
        def __init__(self, config: SensorConfig):
            self.config = config
            self.valor_base = sum (config.rango)/2

        def leer(self) -> float:
            ruido = random.gauss(0, (self.config.rango[1] - self.config.rango[0])* 0.02)
            tendencia = math.sin(time.time( * 0.1)*(self.config.rango[1] - self.config.rango[0])*0.5)
            valor = self.valor_base + ruido + tendencia
            return round (valor,self.config.precision)

        def verificar_alarma(self,valor: float)-> str:
            if valor < self.config.limites_alarma ['bajo']:
                return 'bajo'

             elif valor > self.config.limites_alarma ['alto']:
                return 'alto'
            return 'normal'
    