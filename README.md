# Salud Digna: Propuestas de Mejora

# Fila de Espera

En entornos clínicos, el tiempo de espera es un factor crítico para la experiencia del paciente y la eficiencia operativa. Las filas suelen procesarse bajo esquemas simples como FIFO (primero en llegar, primero en pasar), sin considerar:
- El tipo de paciente (citado, general, con movilidad limitada),
- El tiempo que ya lleva esperando,
- Y la duración real de su atención.

Este algoritmo combina principios de **priorización, deadline handling y duración real** para minimizar el tiempo de espera y distribuir mejor los recursos de atención.


## Descripción del algoritmo

El algoritmo es una variación del modelo **Earliest Deadline First (EDF)** modificado con:

- **Priorización por turno:**  
  - `C` = Citados → prioridad alta (duración breve, 1 min)  
  - `P` = Embarazadas, adultos mayores y personas con poco movilidad → prioridad media  
  - Otros = prioridad baja

- **Deadline dinámico:**  
  Cada paciente tiene un "límite de espera aceptable" de 20 minutos. El algoritmo intenta evitar que cualquier paciente supere ese tiempo.

- **Duración real de atención:**  
  Se usa la columna `TAPRrecepcionMinutos` para conocer cuánto ocupará cada paciente en caja, lo que permite una simulación más precisa. Para los casos en el que no teniamos esta información, se considero un tiempo promedio de atención en caja 1 minuto para pacientes con cita y 5 minutos para los demás paciente.

- **Asignación de cajas disponibles:**  
  Por cada instante de tiempo (minuto o segundo), se asignan pacientes a cajas libres considerando deadline y prioridad.


## 🧠 Lógica del algoritmo

1. **Preparación:** Se ordenan los pacientes por hora de llegada (`TurnoHoraInicioDT`) y se calcula su prioridad, duración estimada y deadline (hora + 20 min).
2. **Simulación:**  
   - A cada instante (ej. minuto), se revisan todas las cajas.
   - Si una caja está libre, se elige el paciente con:
     - Deadline más cercano  
     - Y, en caso de empate, mayor prioridad  
   - Se asigna a la caja, se registra el tiempo de espera y se actualiza su tiempo de liberación.
3. **Final:** Se genera una tabla con los tiempos reales de espera, hora en la que pasó a caja y caja asignada.

---

## Beneficios de implementar el algoritmo

- **Reducción significativa del tiempo de espera promedio**
- **Minimiza pacientes con espera > 20 minutos** (Value at Risk)
- **Respeta la prioridad de pacientes citados**
- **Permite simular distintas configuraciones (cajas, turnos, horarios)**
- **Escalable y adaptable por sucursal o por hora**
- **Mejora la calidad percibida del servicio sin aumentar recursos**

---

## Complejidad computacional

| Variable | Significado |
|----------|-------------|
| `P` | Número de pacientes |
| `C` | Número de cajas |
| `T` | Intervalos simulados (minutos o segundos del día) |

### Complejidad teórica:
El peor caso posible del algoritmo en términos de crecimiento del tiempo de ejecución o uso de memoria, en función del tamaño de entrada es
$$O(T × C × P log P)$$

### Complejidad práctica:
En pruebas reales con 1200 pacientes y simulación por minuto, el algoritmo corre en 1 segundo o menos.
$$O(P log P + C × T)$$

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

- Mayor rango temporal (más de 1 mes de análisis)
- Con un mayor rango se puede predecir con base a distribuciones
- Análisis por turnos (mañana, tarde, noche)


## Uso
Clona el repositorio y los requerimientos
```python
git clone git clone https://github.com/mayradlu/Salud_Digna_Propuesta.git
pip install -r requirements.txt
```



# Ruta crítica de servicios

En muchas clínicas, los pacientes deben recibir múltiples servicios (laboratorio, rayos X, nutrición, etc.) durante una sola visita. Sin embargo, el orden de atención no está optimizado, lo que provoca:
-Tiempos de espera innecesarios
-Uso subóptimo de recursos (salas)
-Cuellos de botella y saturación del sistema

Este proyecto propone un algoritmo que asigna dinámicamente el orden y sala de atención para cada paciente, considerando:
-Lista personalizada de servicios por paciente
-Múltiples salas por tipo de servicio
-Disponibilidad de recursos en tiempo real
-Minimización del tiempo total de permanencia (makespan)

## Metodología

Este problema se modela como una extensión del Job Shop Scheduling Problem (JSSP), donde:
-Cada paciente = un “trabajo”
-Cada servicio = una “máquina”
-Objetivo = minimizar el makespan (tiempo total en clínica)

Por ello, el enfoque combina:
-Rolling Horizon Scheduling (decisiones paso a paso)
-Simulación Discreta de Eventos (DES)
-Sistemas de colas con múltiples servidores (salas por servicio)

## Algoritmo: DES-Rolling

Se implementa una simulación discreta basada en eventos con programación dinámica tipo rolling.  

### Etapas del algoritmo:

1. **Inicialización**
   -Se definen M salas por servicio con disponibilidad inicial a partir de la hora de apertura.
   -Se genera una cola de eventos, incluyendo la llegada de pacientes (cada 5 minutos en simulación).

3. **Cola de eventos**
  -Arrival: El paciente entra al sistema y se programa su primer servicio.
  -Service: Al finalizar un servicio, se evalúa y agenda el siguiente de forma óptima.

4. **Procesamiento de Eventos**
   - Si el evento es "arrival", se programa el primer servicio
   - Si el evento es "service", se asigna la sala más pronta disponible
   - Se calcula el tiempo estimado de finalización + buffer y se agenda el siguiente servicio

5. **Rolling Decision**
   - En cada paso, se evalúa el siguiente servicio óptimo para cada paciente en función de:
     - Su estado actual
     - La disponibilidad de salas
     - El menor tiempo de terminación proyectado


## Complejidad Computacional

Para un conjunto de `n` pacientes, cada uno con `k` servicios, se tienen:

- O(nk) eventos simulados  
- Cada evento puede requerir analizar hasta `k` servicios disponibles  

**Complejidad total:**  
O(nk^2)

Este enfoque es **eficiente y escalable** para clínicas con volumen moderado (hasta cientos de pacientes por día).

## Requisitos
-Python 3.8+
-`numpy`
-`heapq`
-`pandas` 
-`matplotlib` 


## Uso
Clona el repositorio y los requerimientos
```python
git clone git clone https://github.com/mayradlu/Salud_Digna_Propuesta.git
pip install -r requirements.txt
```
