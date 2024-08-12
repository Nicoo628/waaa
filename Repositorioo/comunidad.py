import numpy as np
from ciudadano import Ciudadano
from nombres_apellidos import NombresApellidosManager
import pandas as pd

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica, archivo_nombres):
        self.num_ciudadanos = num_ciudadanos
        self.ciudadanos = []
        self.enfermedad = enfermedad
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica

        # cargar los nombres y apellidos desde archivo csv usando pandas
        self.nombres_apellidos_manager = NombresApellidosManager(archivo_nombres)
        self.__crear_comunidad(num_infectados)  # se crea la comunidad con ciudadanos
        self.interacciones_diarias = []  # Nuevo atributo para almacenar interacciones diarias

    def __crear_comunidad(self, num_infectados):
        for _ in range(self.num_ciudadanos):
            nombre, apellido = self.nombres_apellidos_manager.obtener_nombre_apellido()
            ciudadano = Ciudadano(nombre, apellido, self.enfermedad)
            self.ciudadanos.append(ciudadano) 
        self.inicializar_infectados_aleatorios(num_infectados)  # se inicializa con los infectados aleatorioos

    def simular_dia(self):
        self.interacciones_diarias = []  # Resetear las interacciones diarias
        for ciudadano in self.ciudadanos:
            ciudadano.procesar_dia()  # Procesar el estado diario de cada ciudadano
        self.propagar_infeccion()  # Propagar la infección entre ciudadanos

    def agrupar_por_familia(self):
        familias = {}
        for ciudadano in self.ciudadanos:
            if ciudadano.apellido not in familias:
                familias[ciudadano.apellido] = []
            if len(familias[ciudadano.apellido]) < 5:  # se limitar el tamaño de las familias a un maximo de5 personas
                familias[ciudadano.apellido].append(ciudadano)
        return familias

    def propagar_infeccion(self):
        familias = self.agrupar_por_familia()
        
        for ciudadano in self.ciudadanos:
            if ciudadano.estado == "Infectado":
                interacciones = []  # Lista para almacenar las interacciones del día
                # aca se implementan los contactos estrechos (familia)
                if ciudadano.apellido in familias:
                    for miembro in familias[ciudadano.apellido]:
                        if miembro != ciudadano and miembro.estado == "Susceptible":
                            ciudadano.intentar_infectar(miembro, 0.8)  # 80% probabilidad para contactos estrechos
                            interacciones.append(f"{miembro.nombre} {miembro.apellido}")
                
                # las conexiones aleatorias de lo ciudadanos ademas de los contactos estrechos 
                for _ in range(np.random.poisson(self.probabilidad_conexion_fisica)):
                    otro_ciudadano = np.random.choice(self.ciudadanos)
                    if ciudadano.intentar_infectar(otro_ciudadano, self.enfermedad.infeccion_probable):
                        interacciones.append(f"{otro_ciudadano.nombre} {otro_ciudadano.apellido}")
                
                # Registrar las interacciones del día para el ciudadano infectado
                self.interacciones_diarias.append(f"{ciudadano.nombre} {ciudadano.apellido} ({', '.join(interacciones)})")

    def contar_estado(self, estado):
        return sum(1 for ciudadano in self.ciudadanos if ciudadano.estado == estado) 
    
    def generar_muestra_aleatoria(self, tamano_muestra):
        return np.random.choice(self.ciudadanos, tamano_muestra, replace=False)  # Generar una muestra aleatoria de ciudadanos

    def inicializar_infectados_aleatorios(self, num_infectados):
        muestra = self.generar_muestra_aleatoria(num_infectados) 
        for ciudadano in muestra:
            ciudadano.infectar()  # Infectar a los ciudadanos en la muestra
