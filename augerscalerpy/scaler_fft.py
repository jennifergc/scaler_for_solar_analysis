import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import astropy
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_body
import astropy.units as u
from augerscalerpy.scaler_cleaning import scaler_clean, plot_data
from augerscalerpy.plot_config import configure_plots
from scipy.stats import norm
import matplotlib.ticker as mticker


##### FAST FOURIER TRANSFORM

def scalerfft_frec(sample,dataframe,marks,name,scalercol):
    data = dataframe[scalercol]
    fft_result = np.fft.fft(data)
    power_spectrum = np.abs(fft_result)**2
    sampling_rate = sample  # Unidad de tiempo entre mediciones
    n = len(data)  # Número de puntos de datos
    frequencies = np.fft.fftfreq(n, d=sampling_rate)
    
    # INGRESAR LISTA DE VALORES PARA MARCAR EN LA GRÁFICA (OPCIONAL) esto es si mark=1
    frequencies_to_mark = []
    
    # Pedir al usuario que ingrese valores hasta que deseen detenerse
    if marks==1:
        while True:
            valor = input("Ingresa un valor de frecuencia (en nHz) o escribe 'fin' para detenerte: ")
            # Verificar si el usuario desea detenerse
            if valor.lower() == 'fin':
                break
            try:
                # Convertir el valor ingresado a un número de punto flotante
                valor_frecuencia = float(valor)
                frequencies_to_mark.append(valor_frecuencia)
            except ValueError:
                print("¡Valor no válido! Ingresa un número válido o 'fin' para detenerte.")
        
        # Imprimir la lista de valores ingresados
        print("Valores ingresados:", frequencies_to_mark)
        
    # Escalar las frecuencias a nanohertz (µHz)
    frequencies_nanohertz = frequencies * 1e9  # 1e9 nanohertz en 1 hertz
    # PLOTTING______________Crear la gráfica del espectro de potencias
    configure_plots()
    plt.scatter(frequencies_nanohertz, power_spectrum,s=1)
    plt.yscale('log')  # Configurar el eje horizontal en escala logarítmica
    plt.xscale('log')  # Configurar el eje horizontal en escala logarítmica
    plt.xlabel('Frecuencia (nHz)')
    plt.ylabel('Potencia')
    #plt.title('Espectro de Potencias con Frecuencias en nHz')
    # Agregar líneas verticales y etiquetas
    if marks==1:
        for freq in frequencies_to_mark:
            plt.axvline(x=freq, color='red', linestyle='--', label=f'Frecuencia {freq} nHz')
            plt.text(freq, 1e-4, f'{freq} nHz', rotation=90, va='bottom', ha='center')
    
    plt.grid()
    # Nombre del archivo de salida
    archivo_salida = f'{name}.png' #f-string{name}.png para formatear el nombre del archivo de salida.
    plt. savefig(archivo_salida)
    plt.show()

def scalerfft_OLD(sample,dataframe,marks,name,scalercol):
    data = dataframe[scalercol]
    fft_result = np.fft.fft(data)
    power_spectrum = np.abs(fft_result)**2
    
    sampling_rate = sample  # Unidad de tiempo entre mediciones
    n = len(data)  # Número de puntos de datos
    frequencies = np.fft.fftfreq(n, d=sampling_rate)

    periods = 1 / frequencies  # Calculamos el período en segundos
    # Escalar los períodos a días
    periods_days = periods / 86400  # 86400 segundos en un día
    periods_to_mark = []
    # Pedir al usuario que ingrese valores hasta que deseen detenerse
    if marks==1:
        while True:
            valor = input("Ingresa un valor de periodo (en días) o escribe 'fin' para detenerte: ")
            # Verificar si el usuario desea detenerse
            if valor.lower() == 'fin':
                break
            try:
                # Convertir el valor ingresado a un número de punto flotante
                valor_periodo = float(valor)
                periods_to_mark.append(valor_periodo)
            except ValueError:
                print("¡Valor no válido! Ingresa un número válido o 'fin' para detenerte.")
    # Imprimir la lista de valores ingresados
    print("Valores ingresados:", periods_to_mark)
    
   # Ordenar los períodos de mayor a menor
    periods_days_sorted = sorted(periods_days, reverse=True)
    power_spectrum_sorted = [power_spectrum[i] for i in np.argsort(periods_days)[::-1]]
    # PLOTTING______________Crear la gráfica del espectro de potencias
    plt.figure(figsize=(10, 6))
    plt.plot(periods_days_sorted, power_spectrum_sorted, color='teal') # SIN SMOOTH ACTIVE ESTO
    ############################################## SI SE REQUIERE SMOOTH ACTIVE ESTO
    #x = periods_days_sorted
    #y = power_spectrum_sorted
    #Definir el tamaño de la ventana para el promedio móvil
    #window_size =5
    #Calcular el promedio móvil
    #y_smooth = np.convolve(y, np.ones(window_size)/window_size, mode='same')
    #plt.plot(x, y_smooth, label='Suavizado', color='teal')
    ##############################################
    plt.yscale('log')
    plt.ylim(10**0, 10**11)
    #plt.yticks([10**1, 10**3, 10**5, 10**7, 10**9, 10**11])
    plt.xscale('log')
    plt.gca().invert_xaxis()
    #plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0e'))
    plt.xlabel('Período (días)', fontsize=14)
    plt.ylabel('PSD', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    
    #plt.title('PSD', fontsize=16, pad=20)
    
    # Agregar líneas verticales y etiquetas
    if marks==1:
        for period in periods_to_mark:
            plt.axvline(x=period, color='red', linestyle='--', label=f'Frecuencia {period} nHz', alpha=0.5)
            plt.text(period, 1.1, f'{period} d', rotation=50, va='top', ha='center', fontsize=12)

    
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    #plt.gca().xaxis.set_major_formatter(mticker.ScalarFormatter())
    #plt.gca().xaxis.set_minor_formatter(mticker.NullFormatter())
    
    archivo_salida = f'{name}.pdf'
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    plt.show()
    return periods_days_sorted, power_spectrum_sorted

def scalerfft_period(sample, dataframe, marks, name, scalercol, smooth=False):
    data = dataframe[scalercol]
    fft_result = np.fft.fft(data)
    power_spectrum = np.abs(fft_result)**2
    
    sampling_rate = sample  # Unidad de tiempo entre mediciones
    n = len(data)  # Número de puntos de datos
    frequencies = np.fft.fftfreq(n, d=sampling_rate)

    periods = 1 / frequencies  # Calculamos el período en segundos
    # Escalar los períodos a días
    periods_days = periods / 86400  # 86400 segundos en un día
    periods_to_mark = []
    # Pedir al usuario que ingrese valores hasta que deseen detenerse
    if marks==1:
        while True:
            valor = input("Ingresa un valor de periodo (en días) o escribe 'fin' para detenerte: ")
            # Verificar si el usuario desea detenerse
            if valor.lower() == 'fin':
                break
            try:
                # Convertir el valor ingresado a un número de punto flotante
                valor_periodo = float(valor)
                periods_to_mark.append(valor_periodo)
            except ValueError:
                print("¡Valor no válido! Ingresa un número válido o 'fin' para detenerte.")
    # Imprimir la lista de valores ingresados
    print("Valores ingresados:", periods_to_mark)
    
   # Ordenar los períodos de mayor a menor
    periods_days_sorted = sorted(periods_days, reverse=True)
    power_spectrum_sorted = [power_spectrum[i] for i in np.argsort(periods_days)[::-1]]
    # PLOTTING______________Crear la gráfica del espectro de potencias
    plt.figure(figsize=(10, 6))
    if smooth:
        x = periods_days_sorted
        y = power_spectrum_sorted
        #Definir el tamaño de la ventana para el promedio móvil
        window_size =5
        #Calcular el promedio móvil
        y_smooth = np.convolve(y, np.ones(window_size)/window_size, mode='same')
        plt.plot(x, y_smooth, label='Suavizado', color='teal')
    else:
        plt.plot(periods_days_sorted, power_spectrum_sorted, color='teal') # SIN SMOOTH ACTIVE ESTO
    plt.yscale('log')
    #plt.ylim(10**0, 10**11)
    plt.xscale('log')
    plt.gca().invert_xaxis()
    plt.xlabel('Período (días)', fontsize=14)
    plt.ylabel('PSD', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    
    # Agregar líneas verticales y etiquetas
    if marks==1:
        for period in periods_to_mark:
            plt.axvline(x=period, color='red', linestyle='--', label=f'Frecuencia {period} nHz', alpha=0.5)
            plt.text(period, 1.1, f'{period} d', rotation=50, va='top', ha='center', fontsize=12)

    
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    
    archivo_salida = f'{name}.pdf'
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    plt.show()
    return periods_days_sorted, power_spectrum_sorted
