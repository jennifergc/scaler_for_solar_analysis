import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def scaler_clean(file):
    '''
    Función --scaler_clean-- 
                                scaler_clean(file)
    
    Realiza la limpieza y de los datos corregidos a través de 
    scaler analysis para su correcta visualización.
    Se eliminan los valores cero y los valores atípicos.
    Finalmente se convierte la hora gps de los datos a UTC.

    Para usar la función escriba: nuevo_dataframe = scaler_clean(file)
    
                -file = nombre del archivo entre comillas con su respectiva dirección.
                
                Ejemplo: df = scaler_clean('scaler_datasets/scaler_300s_FINAL.csv')

    Para graficar use -plot_data- usando la salida de esta función.
    '''
    df = pd.read_csv(file) 
    scalerC = df.sort_values(by=['Date']) # Ordena el dataframe  según la columna Date en orde ascendente
    scalerC.set_index('Date', inplace=True) # Convierto la columna Date en índices esto los preserva
    scalerC[scalerC == 0] = None # Convierto los valores cero en NaN para que no afecten el promedio
    scalerC[scalerC > 1800] = None # Convierto los EXCESOS en NaN para que no afecten el promedio
    mean = scalerC.mean() #EL promedio de cada columna
    scalerC.fillna(mean, inplace=True) ## Reemplazo en todos los NAN por el valor promedio...
    # Transformación de tiempo GPS a UTC
    scalerC.reset_index(inplace=True) # Vuelvo a convertir Date en una columna para poder trabajar con ella...
    gps_to_utc_offset = 315964786  # Ajusta esto según la diferencia real
    scalerC['Date'] = pd.to_datetime(scalerC['Date'] + gps_to_utc_offset, unit='s', origin='unix')
    return scalerC

########################################### 
def plot_data(data_frame,name,scalercol):
    '''
    Función ---plot_data--- 
                                plot_data(data_frame,name,scalercol)    
    
    Grafica los scaler previamente limpiados. 
    Recuerde utilizar el archivo de configuración ---configure_plot_scaler()--- de -plot_config-
    Para usar la función escriba: plot_data(data_frame,name,scalercol)
    
                -nuevo_dataframe = nombre de dataframe de salida de la función -scaler_clean(file)-
                -'name' = nombre del archivo .png de la imagen de salida que se guardará en el directorio de trabajo.
                -scalercol= nombre de la columna donde están los valores de CRI que se van a graficar.
                
                Ejemplo: plot_data(scaler300s,'scaler_300s_N8','ScalerCorr')
    
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
    user_legend = input("Ingrese el legend de la gráfica: (si no quiere aparezca ingrese un espacio): ")
    user_xlabel = input("Ingrese el nombre del eje x: ")
    user_ylabel = input("Ingrese el nombre del eje y: ")
    user_title = input("Ingrese el título de la gráfica (si no quiere título ingrese un espacio): ")
    plt.scatter(dates, intensity, s=1, label=user_legend)
    
    # Configurar ejes, título y leyenda
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel(user_xlabel)
    plt.ylabel(user_ylabel)
    plt.title(user_title)
    
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
