import pandas as pd
from datetime import datetime, timedelta

"""
Esta función se utiliza para cuando no se tiene información de la duración en caja del paciente. Así que se utilizan tiempos promedios.
"""

def fila_espera(df_dia, inicio_jornada, jornada_trabajo, tiempo_atencion_default, step, num_cajas):

    df_dia['TurnoHoraInicioDT'] = pd.to_datetime(df_dia['TurnoHoraInicio'], format='%H:%M:%S')
    df_dia['TurnoHoraInicioDT'] = df_dia['TurnoHoraInicioDT'].apply(
        lambda t: inicio_jornada.replace(hour=t.hour, minute=t.minute, second=t.second))
    
    pacientes = df_dia.sort_values(by='TurnoHoraInicioDT').reset_index(drop=True)

    paciente_queue = []
    for _, row in pacientes.iterrows():
        prioridad = row['PrioridadBase']
        duracion = timedelta(minutes=1) if prioridad == 1 else tiempo_atencion_default
        paciente_queue.append({
            'Orden': row['Orden'],
            'Prioridad': prioridad,
            'TurnoHoraInicioDT': row['TurnoHoraInicioDT'],
            'Deadline': row['TurnoHoraInicioDT'] + timedelta(minutes=20),
            'DuracionAtencion': duracion
        })

    cajas = [inicio_jornada for _ in range(num_cajas)]
    resultados = []

    current_time = inicio_jornada
    end_time = inicio_jornada + jornada_trabajo

    while current_time <= end_time and paciente_queue:
        for caja_idx in range(num_cajas):
            if cajas[caja_idx] <= current_time:
                elegibles = [p for p in paciente_queue if p['TurnoHoraInicioDT'] <= current_time]
                if not elegibles:
                    continue

                elegibles.sort(key=lambda x: (x['Deadline'], x['Prioridad']))
                paciente = elegibles[0]
                paciente_queue.remove(paciente)

                tiempo_espera = (current_time - paciente['TurnoHoraInicioDT']).total_seconds() / 60.0

                resultados.append({
                    'Orden': paciente['Orden'],
                    'Prioridad': paciente['Prioridad'],
                    'TiempoEsperaMin': tiempo_espera,
                    'HoraLlegada': paciente['TurnoHoraInicioDT'].time(),
                    'HoraPasoCaja': current_time.time(),
                    'CajaAsignada': caja_idx + 1  
                })

                cajas[caja_idx] = current_time + paciente['DuracionAtencion']

        current_time += step

    return pd.DataFrame(resultados)

"""
Esta función se utiliza para cuando se tiene información de la duración en caja del paciente.
"""

def fila_espera_sim(df_dia, inicio_jornada, jornada_trabajo, step, num_cajas):
    df_dia['TurnoHoraInicioDT'] = pd.to_datetime(df_dia['TurnoHoraInicio'], format='%H:%M:%S')
    df_dia['TurnoHoraInicioDT'] = df_dia['TurnoHoraInicioDT'].apply(
        lambda t: inicio_jornada.replace(hour=t.hour, minute=t.minute, second=t.second))
    
    pacientes = df_dia.sort_values(by='TurnoHoraInicioDT').reset_index(drop=True)

    paciente_queue = []
    for _, row in pacientes.iterrows():
        prioridad = row['PrioridadBase']
        minutos_atencion = row['TAPRecepcionMinutos']
        duracion = timedelta(minutes=minutos_atencion)

        paciente_queue.append({
            'Orden': row['Orden'],
            'Prioridad': prioridad,
            'TurnoHoraInicioDT': row['TurnoHoraInicioDT'],
            'Deadline': row['TurnoHoraInicioDT'] + timedelta(minutes=20),
            'DuracionAtencion': duracion
        })

    cajas = [inicio_jornada for _ in range(num_cajas)]
    resultados = []

    current_time = inicio_jornada
    end_time = inicio_jornada + jornada_trabajo

    while current_time <= end_time and paciente_queue:
        for caja_idx in range(num_cajas):
            if cajas[caja_idx] <= current_time:
                elegibles = [p for p in paciente_queue if p['TurnoHoraInicioDT'] <= current_time]
                if not elegibles:
                    continue

                elegibles.sort(key=lambda x: (x['Deadline'], x['Prioridad']))
                paciente = elegibles[0]
                paciente_queue.remove(paciente)

                tiempo_espera = (current_time - paciente['TurnoHoraInicioDT']).total_seconds() / 60.0

                resultados.append({
                    'Orden': paciente['Orden'],
                    'Prioridad': paciente['Prioridad'],
                    'TiempoEsperaMin': tiempo_espera,
                    'HoraLlegada': paciente['TurnoHoraInicioDT'].time(),
                    'HoraPasoCaja': current_time.time(),
                    'CajaAsignada': caja_idx + 1
                })

                cajas[caja_idx] = current_time + paciente['DuracionAtencion']

        current_time += step

    return pd.DataFrame(resultados)

