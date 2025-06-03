# Salud Digna: Propuesta de Mejora

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
# Ejecutar el análisis con tus parámetros personalizados
archivo_excel = "coyoacan.xlsx"
analisis_cajas(archivo_excel, sucursal='COYOACAN', max_cajas=10)
```

## Escalabilidad


# Ruta crítica de servicios
