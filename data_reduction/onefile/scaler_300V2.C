#include <vector>
#include <fstream>
#include <iostream>

// Incluye los encabezados de ROOT necesarios
#include "TFile.h"
#include "TTree.h"
#include "TSystemDirectory.h"
#include "TSystemFile.h"

int main() {
    // Creación de variables
    Double_t mean;
    Float_t press;
    UInt_t gpstime;
    UInt_t stations;
    Double_t arrmean;
    Double_t arrvar;
    Int_t nsdvar;
    Double_t errmean;
    std::vector<Double_t> mean300;
    std::vector<Float_t> press300;
    std::vector<Double_t> arrmean300;
    std::vector<Double_t> arrvar300;
    std::vector<Int_t> nsdvar300;
    std::vector<Double_t> errmean300;
    std::vector<UInt_t> stations300;
    std::vector<UInt_t> gpstime300;

    // Abre el archivo de salida
    std::ofstream salida;
    salida.open("scaler_300s.csv", std::ios::out);

    // Ubicación de los archivos ROOT
    TString datos = "./";

    // Lista de archivos en el directorio
    TSystemDirectory dir(datos, datos);
    TList *files = dir.GetListOfFiles();

    if (files) {
        TSystemFile *file;
        TString fname;
        TString archivo;

        // Itera a través de la lista de archivos
        TIter next(files);
        while ((file = (TSystemFile *)next())) {
            fname = file->GetName();
            if (!file->IsDirectory() && fname.EndsWith(".root")) {
                archivo = datos + fname;
                std::cout << archivo << std::endl;

                // Lectura del archivo ROOT
                TFile *input = new TFile(fname.Data(), "READ");
                int test = input->GetNkeys();

                // Verifica si el archivo tiene contenido
                if (test > 0) {
                    // Extracción de información del árbol
                    TTree *tree = (TTree *)input->Get("sdst::ScalerSummaryDataTree");
		    tree->SetBranchAddress("fCorrectedArrayMean", &arrmean);
		    tree->SetBranchAddress("fCorrectedArrayMeanSigma", &arrvar);
		    tree->SetBranchAddress("fCorrectedArrayVarianceOfMeanScalers", &errmean);
		    tree->SetBranchAddress("fNumberStationDeviation", &nsdvar);
                    tree->SetBranchAddress("fCorrectedScalerArrayMean", &mean);
                    tree->SetBranchAddress("fGPSSecond", &gpstime);
                    tree->SetBranchAddress("fMeanPressure", &press);
                    tree->SetBranchAddress("fNumberOfStationsUsedInMean", &stations);

                    int entries = tree->GetEntries();

                    for (int i = 0; i < entries; i++) {
                        tree->GetEntry(i);
                        // Agrega los valores al vector
                        mean300.push_back(mean);
                        press300.push_back(press);
			arrvar300.push_back(arrvar);
			errmean300.push_back(errmean);
			gpstime300.push_back(gpstime);
			stations300.push_back(stations);
			nsdvar300.push_back(nsdvar);
			arrmean300.push_back(arrmean);
                    }
                }

                // Cierra el archivo ROOT
                input->Close();
                delete input;
            }
        }
        
        // Escribe los datos en el archivo de salida
        if (salida.is_open()) {
            std::cout << "Escribiendo el archivo de salida..." << std::endl;
            for (size_t i = 0; i < mean300.size(); i++) {
                salida << gpstime300[i] << "," << mean300[i] << "," << errmean300[i]<< "," <<arrmean300[i]<< "," <<arrvar300[i]<< "," <<stations300[i]<< "," <<nsdvar300[i]<< "," << press300[i]  << std::endl;
            }
            std::cout << "Archivo creado con éxito :)" << std::endl;
        }

        // Limpia los vectores
        mean300.clear();
        press300.clear();
	arrvar300.clear();
	errmean300.clear();
	gpstime300.clear();
	stations300.clear();
	nsdvar300.clear();
	arrmean300.clear();
    }

    // Cierra el archivo de salida
    salida.close();

    return 0;
}

