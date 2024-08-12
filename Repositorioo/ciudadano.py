import numpy as np
class Ciudadano:
    def __init__(self, nombre, apellido, enfermedad):
        self.nombre = nombre
        self.apellido = apellido
        self.enfermedad = enfermedad
        self.estado = "Susceptible"  # Estado
        self.dias_infectado = 0  # contador de cuantos dias lleva infectado


    def procesar_dia(self):
        if self.estado == "Infectado":
            self.dias_infectado += 1  
            if self.dias_infectado >= self.enfermedad.promedio_pasos:
                self.estado = "Recuperado"  # recuperarse si alcanza el promedio de pasos
    
    def infectar(self):
        self.estado = "Infectado"   
        self.dias_infectado = 0  

    def intentar_infectar(self, otro_ciudadano, probabilidad_infeccion):
        if self.estado == "Infectado" and otro_ciudadano.estado == "Susceptible":
            if np.random.poisson() < probabilidad_infeccion:
                otro_ciudadano.infectar()  # Infectar al otro ciudadano con cierta probabilidad