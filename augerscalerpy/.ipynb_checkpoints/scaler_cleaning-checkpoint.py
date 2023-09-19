import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plotscaler(file, name):
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
    SDOK = taste[taste['ScalerCorr'] > 1580  ]
    SDOK = SDOK[SDOK['ScalerCorr'] < 1700 ]

    #Ajuste de la secuencia temporal
    fixed =SDOK.assign(Group=315964786)
    fixed.shape
    #
    fixed2=  fixed["Date"]+fixed["Group"]
    fixed2.head()
    #
    datetime = pd.to_datetime(fixed2, unit = 's')
    SDOK["Date"] = datetime.values
    
    # Nombre del archivo de salida
    archivo_salida = f'{name}.png' #f-string{name}.png para formatear el nombre del archivo de salida.
     
    #Plotting final dataset
    #SDOK.plot(kind='scatter', s= 2,x='Date',y='ScalerCorr',color='black', figsize =(20,10))
    #plt.legend(fontsize=20)
    #plt.savefig(archivo_salida)
    #plt.show()
    import matplotlib.pyplot as plt

    # Plotting final dataset
    SDOK.plot(kind='scatter', s=2, x='Date', y='ScalerCorr', color='black', figsize=(20, 10))

    # Ajustar tamaño de fuente de los ejes (etiquetas y números)
    plt.tick_params(axis='both', which='major', labelsize=20)

    # Ajustar tamaño de fuente de la leyenda
    plt.legend(fontsize=20)
    # Ajustar tamaño de fuente de las etiquetas de los ejes
    plt.xlabel('Fecha', fontsize=20)
    plt.ylabel('ScalerCorr', fontsize=20)

    # Guardar el gráfico en archivo_salida y mostrarlo
    plt.savefig(archivo_salida)
    plt.show()

    return SDOK