#!/bin/bash

# Definir la ruta de la carpeta base
SCALER="/media/jennifer/jennifer/TESIS/scaler-outputs/Downloads/scaler-output/scalar_analysis"

# Iterar a través de cada subcarpeta correspondiente a los años del 2006 al 2022
for YEAR in {2006..2020}; do
  YEAR_DIR="$SCALER/$YEAR"

  # Iterar a través de cada subsubcarpeta correspondiente a los meses del 01 al 12
  for MONTH in {01..12}; do
    MONTH_DIR="$YEAR_DIR/$MONTH"
 

    # Entrar en la subsubcarpeta y correr el script "11abr3600s" que está en el directorio SCALER
    cd "$MONTH_DIR"
    "$SCALER/11abr3600s"
  done
done
