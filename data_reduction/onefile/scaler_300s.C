//C++
#include <algorithm>
#include <vector>
#include <cstring>
#include <string>
#include <cstdlib>
#include <fstream>
#include <iostream>
using namespace std;

// ROOT
#include "TTree.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TH1F.h"

int main() {
    TCanvas *c1 = new TCanvas();

    // Variables
    Double_t mean;
    UInt_t gpstime;
    Float_t press;
    UInt_t stations;
    vector<UInt_t> gps300;
    vector<Double_t> mean300;
    vector<Float_t> press300;
    vector<Double_t> stat300;
    
    int cantArchivos = 0;

    // Crear archivo de salida
    ofstream salida;
    salida.open("scaler_300s_rev.csv", ios::out);

    // Directorio de archivos ROOT
    TString datos; // Ubicación de archivos
    datos = "./";
    TSystemDirectory dir(datos, datos);
    TList *files = dir.GetListOfFiles();

    if (files) {
        TSystemFile *file;
        TString fname;
        TString archivo;
        TIter next(files);

        while ((file = (TSystemFile *)next())) {
            fname = file->GetName();
            if (!file->IsDirectory() && fname.EndsWith(".root")) {
                archivo = datos + fname;
                cout << archivo << endl;
            } else {
                continue;
            }

            // Leer archivo y verificar archivos vacíos
            cantArchivos++;
            cout << "Leyendo archivo:" << cantArchivos << endl;

            // Leer archivo ROOT
            TFile *input = new TFile(fname.Data(), "READ");
            
            // Filtrar archivos vacíos
            int test = input->GetNkeys();
            cout << "NKeys: " << test << endl;
            
            // Extraer información de variables
            cout << "Leyendo archivo ROOT" << endl;
            TTree *tree = (TTree *)input->Get("sdst::ScalerSummaryDataTree");
            input->GetListOfKeys()->Print();

            if (test == 0) {
                continue; // Archivo vacío, continuar con el siguiente
            } else {
                tree->SetBranchAddress("fCorrectedScalerArrayMean", &mean);
                tree->SetBranchAddress("fGPSSecond", &gpstime);
                tree->SetBranchAddress("fMeanPressure", &press);
                tree->SetBranchAddress("fNumberOfStationsUsedInMean", &stations);
                int entries = tree->GetEntries();
                cout << "Cantidad de entradas: " << entries << endl;

                TH1F *histM = new TH1F("histM", "Histogram", 100, 1600, 1800);
                
                for (int i = 0; i < entries; i++) {
                    tree->GetEntry(i);
                    gps300.push_back(gpstime);
                    mean300.push_back(mean);
                    press300.push_back(press);
                    stat300.push_back(stations);
                    cout << "Línea numero: " << i << " Scaler value: " << mean300.at(i) << endl;
                }
                cout << "Vectores creados para intervalos de 300 segundos" << endl;
                
                // Escribir datos en el archivo de salida
                if (salida.is_open()) {
                    cout << "Escribiendo el archivo de salida..." << endl;
                    for (int i = 0; i < press300.size(); i++) {
                        UInt_t gps = gps300.at(i);
                        Double_t vmean = mean300.at(i);
                        Float_t vpres = press300.at(i);
                        Double_t vstat = stat300.at(i);
                        salida << gps << "," << vmean << "," << vpres << "," << vstat << endl;
                    }
                    gps300.clear();
                    mean300.clear();
                    press300.clear();
                    stat300.clear();
                    cout << "Archivo creado con éxito :)" << endl;
                }
            }
        }
    }
    salida.close();
    return 0;
}

