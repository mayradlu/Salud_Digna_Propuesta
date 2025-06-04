# Salud Digna: Propuestas de Mejora

# Fila de Espera


# Apertura y Cierres de Cajas

Esta carpeta contiene una función llamada `analisis_cajas` que realiza un análisis predictivo del número de cajas que deben abrirse o cerrarse por hora, basándose en datos históricos de llegadas de clientes.

## ¿Qué hace este análisis?

La función:
- Agrupa datos por día de la semana y hora.
- Considera únicamente los últimos 4 días disponibles de cada día de la semana, es decir, un mes anterior.
- Calcula la cantidad óptima de cajas necesarias por hora, considerando el promedio histórico del mes anterior por hora y día de pacientes atendidos.
- Limita el número máximo de cajas a un valor configurable.
- Genera una visualización para poder planear la semana de trabajo: un heatmap con los días y cajas sugeridas por hora.

![imagen](https://github.com/user-attachments/assets/202c1b37-2298-4729-bc0d-4ebbcd6a31ef)


## Requisitos

- Python 3.7+
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- Un archivo Excel con las siguientes columnas:
  - `FechaID` (formato `YYYYMMDD`)
  - `TurnoHoraInicio` (formato `HH:MM:SS`)
  - `TurnoHoraFin` (formato `HH:MM:SS`)
  - `Sucursal`
---

## Parámetros de la función

```python
analisis_cajas(archivo_excel, sucursal='COYOACAN', max_cajas=10)
```
- archivo_excel: archivo a analizar 
- sucursal: sucursal que se desea analizar
- max_cajas: máximo número de cajas por sucursal

## Escalabilidad

## Uso


# Ruta crítica de servicios

En muchas clínicas, los pacientes deben recibir múltiples servicios (laboratorio, rayos X, nutrición, etc.) durante una sola visita. Sin embargo, el orden de atención no está optimizado, lo que genera:

- Tiempos de espera innecesarios  
- Uso subóptimo de recursos (salas)  
- Congestionamientos y cuellos de botella  

El objetivo del algoritmo es asignar de forma dinámica y eficiente el orden de servicios para cada paciente, considerando la disponibilidad de salas, la duración estimada de los servicios y la posibilidad de adaptación en tiempo real.

## Metodología

Este problema se modela como una extensión del clásico **Job Shop Scheduling Problem (JSSP)**, donde:

- Cada **paciente** representa *trabajo*  
- Cada **servicio** representa una *máquina*  
- Se busca minimizar el **makespan** (tiempo total de permanencia del paciente en la clínica)

## Algoritmo: DES-Rolling

Se implementa una simulación discreta basada en eventos con programación dinámica tipo rolling.  

### Etapas del algoritmo:

1. **Inicialización**
   - Se define un tiempo base (ej. 08:00 AM)
   - Se establece un mapa de duración promedio por servicio
   - Se inicializa el estado de ocupación de las salas

2. **Llegadas Programadas**
   - Cada paciente entra al sistema cada 5 minutos (simulado)
   - Se genera un evento de tipo "arrival" en la cola de eventos

3. **Procesamiento de Eventos**
   - Si el evento es "arrival", se programa el primer servicio
   - Si el evento es "service", se asigna la sala más pronta disponible
   - Se calcula el tiempo estimado de finalización + buffer y se agenda el siguiente servicio

4. **Rolling Decision**
   - En cada paso, se evalúa el siguiente servicio óptimo para cada paciente en función de:
     - Su estado actual
     - La disponibilidad de salas
     - El menor tiempo de terminación proyectado


## Complejidad Computacional

Para un conjunto de `n` pacientes, cada uno con `k` servicios, se tienen:

- O(nk) eventos simulados  
- Cada evento puede requerir analizar hasta `k` servicios disponibles  

**Complejidad total:**  
$$
\mathcal{O}(nk^2)
$$

Este enfoque es **eficiente y escalable** para clínicas con volumen moderado (hasta cientos de pacientes por día).

## Requisitos

## Uso
