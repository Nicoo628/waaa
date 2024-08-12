import random
import numpy as np

class Simulador:
    def __init__(self, umbral_infeccion=1):
        self.susceptibles = np.array([])
        self.infectados = np.array([])
        self.recuperados = np.array([])
        self.umbral_infeccion = umbral_infeccion  # Umbral de interacciones necesarias para infectar

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad
        self.susceptibles = np.array([c for c in comunidad.ciudadanos if c.estado == 'S'])
        self.infectados = np.array([c for c in comunidad.ciudadanos if c.estado == 'I'])
        self.recuperados = np.array([c for c in comunidad.ciudadanos if c.estado == 'R'])

    def run(self, pasos):
        for _ in range(pasos):
            self.comunidad.actualizar_contactos_diarios()  # Actualizar los contactos diarios
            self.simular_paso()

    def simular_paso(self):
        tasa_infeccion = self.comunidad.enfermedad.infeccion_probable
        for infectado in self.infectados:
            for contacto in infectado.contactos_diarios:
                if contacto.estado == 'S':
                    interacciones_infectados = len([i for i in contacto.contactos_diarios if i.estado == 'I'])
                    if interacciones_infectados >= self.umbral_infeccion and random.random() < tasa_infeccion:
                        self.infectar_contacto(contacto)

        tasa_recuperacion = self.comunidad.enfermedad.recuperacion_probable
        for infectado in list(self.infectados):  # Crear una copia para evitar problemas durante la iteración
            infectado.pasos_infectado += 1
            if infectado.pasos_infectado >= 15 or random.random() < tasa_recuperacion:
                self.recuperar_infectado(infectado)

    def infectar_contacto(self, contacto):
        if contacto in self.susceptibles:
            self.susceptibles = np.array([c for c in self.susceptibles if c != contacto])
            contacto.estado = 'I'
            contacto.pasos_infectado = 0
            self.infectados = np.append(self.infectados, contacto)

    def recuperar_infectado(self, infectado):
        if infectado in self.infectados:
            self.infectados = np.array([c for c in self.infectados if c != infectado])
            infectado.estado = 'R'
            self.recuperados = np.append(self.recuperados, infectado)
