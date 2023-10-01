#!/bin/bash
echo Corriendo archivo por años...
DIR="/home/jennifer/Documentos/Master/TESIS/scaler-outputs/Downloads/scaler-output/scalar_analysis"
for i in {2006..2020..1}
do
    for j in {10..12..1}
    do 
        cp 20MAR3600s "$DIR/$i/$j/"
       	cd $DIR/$i/$j/
       	./20MAR3600s
    done
done
