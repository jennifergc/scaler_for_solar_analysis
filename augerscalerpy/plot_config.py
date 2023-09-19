# plot_config.py

import matplotlib.pyplot as plt

def configure_plots():
    '''
    Configure_plots

    Establece la configuración global de Matplotlib para el estilo de las gráficas.
    Puedes llamar a esta función al inicio de tus scripts de visualización para aplicar un estilo coherente.

    Ejemplo de uso:
    PARA IMPORTAR:
    >>> from augerscalerpy.plot_config import configure_plots 

    configure_plots()
    plt.plot(x, y)
    plt.show()
    '''
    # Configuración global de Matplotlib
    plt.rcParams['figure.figsize'] = (8, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

def configure_plot_scaler():
    '''
    Configure_plots

    Establece la configuración global de Matplotlib para el estilo de las gráficas.
    Puedes llamar a esta función al inicio de tus scripts de visualización para aplicar un estilo coherente.

    Ejemplo de uso:
    PARA IMPORTAR:
    >>> from augerscalerpy.plot_config import configure_plot_scaler

    configure_plot_scaler()
    plt.plot(x, y)
    plt.show()
    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    # Configuración global de Matplotlib para el estilo de la gráfica
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    
    # Configuración de colores
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#333333'])
    
    # Configuración de cuadrícula
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.5
    
    # Configurar el formato de las fechas en el eje x (cada año)
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Rotar las etiquetas del eje x para una mejor visualización
    plt.xticks(rotation=45)

    # Añadir una cuadrícula menor para las fechas mensuales
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())

def configure_histograms():
    '''
    Configure_plots

    Establece la configuración global de Matplotlib para el estilo de los histogramas.
    Puedes llamar a esta función al inicio de tus scripts de visualización para aplicar un estilo coherente.

    Ejemplo de uso:
    PARA IMPORTAR:
    >>> from augerscalerpy.plot_config import configure_histograms

    configure_histograms()
    plt.plot(x, y)
    plt.show()
    '''
    # Configuración de colores para los histogramas y barras de error
    hist_color = '#1E90FF'  # Color primario para los histogramas
    error_color = '#FF6F61'  # Color primario para las barras de error

    # Configuración global de Matplotlib
    plt.rcParams['figure.figsize'] = (8, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

    # Configuración de colores de histogramas
    plt.rcParams['hist.facecolor'] = hist_color
    plt.rcParams['hist.edgecolor'] = 'black'

    # Configuración de colores de barras de error
    plt.rcParams['errorbar.capsize'] = 5
    plt.rcParams['errorbar.color'] = error_color

