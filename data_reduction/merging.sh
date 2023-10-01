#!/bin/bash
echo Corriendo archivo por años...
LIN=""
DIR="/media/jennifer/jennifer/TESIS/scaler-outputs/Downloads/scaler-output/scalar_analysis"
for i in {2006..2020..1}
do
	for j in {1..12..1}
	do
		if [ $j -lt 10 ]
		then
		       LIN=$LIN"$i/0$j/VM_MOD3600.csv "
	        else
		       LIN=$LIN"$i/$j/VM_MOD3600.csv "
		fi
        done
done
cat $LIN > scaler_ALL_hourly_11abril.csv
