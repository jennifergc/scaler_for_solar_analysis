#include <iostream>
#include <fstream>
#include <vector>
#include <string>
using namespace std;

#include "TFile.h"
#include "TTree.h"
#include "TSystemDirectory.h"

// CÓDIGO PARA EXTRAER LOS VALORES DE SCALER DE LOS ARCHIVOS ROOT GENERADOS
// DESPUÉS DE LA CORRECCIÓN POR PRESIÓN Y TEMPERATURA

int main() {
    // Variables para almacenar datos
    vector<Double_t> mean;
    vector<UInt_t> gpstime;
    vector<Float_t> press;
    vector<UInt_t> stations;

    // Ruta al directorio que contiene los archivos .root
    TString dataPath = "./";

    // Abre el directorio y obtiene la lista de archivos .root
    TSystemDirectory dir(dataPath, dataPath);
    TList *files = dir.GetListOfFiles();

    if (files) {
        TSystemFile *file;
        TIter next(files);

        while ((file = (TSystemFile *)next())) {
            TString fname = file->GetName();

            if (!file->IsDirectory() && fname.EndsWith(".root")) {
                TString filePath = dataPath + fname;
                cout << "Leyendo archivo: " << filePath << endl;

                TFile *input = new TFile(filePath, "READ");
                TTree *tree = (TTree *)input->Get("sdst::ScalerSummaryDataTree");

                // Variables para almacenar los datos del archivo
                Double_t meanVal;
                UInt_t gpstimeVal;
                Float_t pressVal;
                UInt_t stationsVal;

                // Configura las ramas del árbol
                tree->SetBranchAddress("fCorrectedScalerArrayMean", &meanVal);
                tree->SetBranchAddress("fGPSSecond", &gpstimeVal);
                tree->SetBranchAddress("fMeanPressure", &pressVal);
                tree->SetBranchAddress("fNumberOfStationsUsedInMean", &stationsVal);

                int entries = tree->GetEntries();
                cout << "Cantidad de entradas: " << entries << endl;

                // Lee los datos del archivo y los almacena en vectores
                for (int i = 0; i < entries; i++) {
                    tree->GetEntry(i);
                    mean.push_back(meanVal);
                    gpstime.push_back(gpstimeVal);
                    press.push_back(pressVal);
                    stations.push_back(stationsVal);
                }

                input->Close();
                delete input;
            }
        }

        // Procesamiento posterior con los vectores de datos
        // ...

        // Limpia los vectores después de su uso si es necesario
        mean.clear();
        gpstime.clear();
        press.clear();
        stations.clear();
    } else {
        cerr << "Error al abrir el directorio." << endl;
        return 1;
    }

    return 0;
}

