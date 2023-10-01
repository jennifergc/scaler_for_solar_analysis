#!/bin/bash
echo Corriendo archivo por años...
DIR="/media/jennifer/jennifer/TESIS/scaler-outputs/Downloads/scaler-output/scalar_analysis"
for i in {2006..2021..1}
do
    for j in {1..9..1}
    do 
        cp 20MAR3600s "$DIR/$i/0$j/"
       	cd $DIR/$i/0$j/
       	./20MAR3600s
    done
done
#!/bin/bash

# Definir la ruta de la carpeta base
SCALER="/media/jennifer/jennifer/TESIS/scaler-outputs/Downloads/scaler-output/scalar_analysis"

# Iterar a través de cada subcarpeta correspondiente a los años del 2006 al 2022
for YEAR in {2006..2022}; do
  YEAR_DIR="$SCALER/$YEAR"

  # Iterar a través de cada subsubcarpeta correspondiente a los meses del 01 al 12
  for MONTH in {01..12}; do
    MONTH_DIR="$YEAR_DIR/$MONTH"

    # Entrar en la subsubcarpeta y correr el script "analysis"
    cd "$MONTH_DIR"
    ./average_window.C
  done
done
