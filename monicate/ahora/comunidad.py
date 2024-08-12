from ciudadano import Ciudadano
import random
import numpy as np

class Comunidad:
    def __init__(self, num_ciudadanos, enfermedad, num_infectados):
        self.enfermedad = enfermedad
        self.ciudadanos = self.crear_ciudadanos(num_ciudadanos, num_infectados)
        self.crear_contactos_fijos()

    def crear_ciudadanos(self, num_ciudadanos, num_infectados):
        ciudadanos = np.array([Ciudadano(id=i, comunidad=self) for i in range(num_ciudadanos)])

        # Infectar los primeros num_infectados ciudadanos
        infectados_iniciales = random.sample(list(ciudadanos), num_infectados)
        for infectado in infectados_iniciales:
            infectado.estado = 'I'

        return ciudadanos

    def crear_contactos_fijos(self):
        for ciudadano in self.ciudadanos:
            num_contactos = random.randint(0, 8)
            contactos = random.sample(list(self.ciudadanos[self.ciudadanos != ciudadano]), k=num_contactos)
            for contacto in contactos:
                ciudadano.agregar_contacto(contacto)
                contacto.agregar_contacto(ciudadano)

    def actualizar_contactos_diarios(self):
        for ciudadano in self.ciudadanos:
            num_contactos_diarios = random.randint(0, len(ciudadano.contactos))
            ciudadano.contactos_diarios = random.sample(ciudadano.contactos, k=num_contactos_diarios)
