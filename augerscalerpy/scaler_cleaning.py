import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def scaler_clean(file, name):
    '''
    --scaler_clean--
    scaler_clean(file, name)
    Realiza la limpieza y de los datos corregidos a través de 
    scaler analysis para su correcta visualización.
    Se eliminan los valores cero y los valores atípicos.
    Finalmente se convierte la hora gps de los datos a UTC.

    Para usar la función escriba: nuevo_dataframe = scaler_clean(file, name)
    '''
    #Lectura y filtrado de valores nulos
    df = pd.read_csv(file)
    scalerC = df.sort_values(by=['Date'])
    nocero = scalerC[scalerC['ScalerCorr'] != 0 ]
    taste = nocero
    #Cuántos valores cero hay? --No relevante
    EMPTY =scalerC[scalerC['ScalerCorr'] == 0 ]
    print("Hay ", EMPTY.shape, "líneas vacías")

    #AJUSTE EXCESOS
    #SDBAD1 =taste[taste['ScalerCorr'] > 1900 ]
    #SDBAD2 =taste[taste['ScalerCorr'] < 1500 ]
    #SDOK = taste[taste['ScalerCorr'] > 1580  ]
    #SDOK = SDOK[SDOK['ScalerCorr'] < 1700 ]
    #SDOK = taste
    SDOK = taste[taste['ScalerCorr'] < 1800  ]
    #Ajuste de la secuencia temporal del GPS de los tanques a UTC
    fixed =SDOK.assign(Group=315964786)
    fixed.shape
    #
    fixed2=  fixed["Date"]+fixed["Group"]
    fixed2.head()
    #
    datetime = pd.to_datetime(fixed2, unit = 's')
    SDOK["Date"] = datetime.values
    return SDOK

###########################################
import matplotlib.pyplot as plt
########################################### 
def plot_data(data_frame,name,scalercol):
    '''
    ---plot_data---
    plot_data(data_frame,'name')
    Grafica los scaler previamente limpiados. 
    Recuerde utilizar el archivo de configuración ---configure_plot_scaler()--- de -plot_config-
    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    from augerscalerpy.plot_config import configure_plot_scaler
    configure_plot_scaler()
    
    # Asegúrate de que la columna 'Date' sea de tipo datetime
    #data_frame['Date'] = pd.to_datetime(data_frame['Date'])
    
    # Convertir las columnas en arreglos de NumPy
    dates = data_frame['Date'].values
    intensity = data_frame[scalercol].values

    # Crear el gráfico de puntos
    plt.scatter(dates, intensity, s=1, label='5min average data')
    
    # Configurar ejes, título y leyenda
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Scaler')
    plt.title('Auger scaler over the years')
    
    # Añadir una cuadrícula menor para las fechas mensuales
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())
    plt.legend()

    # Nombre del archivo de salida
    archivo_salida = f'{name}.png' #f-string{name}.png para formatear el nombre del archivo de salida.
    plt. savefig(archivo_salida)
    
    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()
    
##########################################
