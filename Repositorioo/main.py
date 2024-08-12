from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador
 
 

 
# se crea una instancia de Enfermedad
covid = Enfermedad(infeccion_probable=0.3, promedio_pasos=18)

# se crea una instancia de Comunidad con ciudadanos con lo
talca = Comunidad(num_ciudadanos=2000, promedio_conexion_fisica=8, enfermedad=covid, num_infectados=10, probabilidad_conexion_fisica=0.8, archivo_nombres="nombres_apellidos.csv")


sim = Simulador()
sim.set_comunidad(comunidad=talca)  # Establecer la comunidad en el simulador
sim.run(pasos=45)  # Ejecutar la simulación por un número de días