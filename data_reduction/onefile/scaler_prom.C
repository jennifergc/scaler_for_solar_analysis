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
#include "TROOT.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TVectorT.h"
#include "TSystemDirectory.h"
#include "TMath.h"
#include "TH1F.h"

int main() {
    TCanvas *c1 = new TCanvas();

    // Variables
    int val = 0;
    Double_t mean;
    Double_t stdv;
    UInt_t tmp_gps;
    Double_t tmp_mean;
    Double_t err;
    Float_t tmp_press;
    Double_t tmp_station;
    UInt_t gpstime;
    UInt_t gps;
    Float_t press;
    UInt_t stations;
    vector<UInt_t> gpsInterval;
    vector<Double_t> meanInterval;
    vector<Double_t> mean_err;
    vector<Float_t> pressInterval;
    vector<Double_t> statInterval;
    
    int cantArchivos = 0;
    bool primerArchivo = true;

    // Create an output file
    ofstream salida;
    salida.open("scaler_prom.csv", ios::out);

    // Prompt user for interval time (in seconds)
    int intervalSeconds;
    cout << "Ingrese el intervalo de tiempo deseado (en segundos, múltiplo de 300): ";
    cin >> intervalSeconds;

    // Check if the interval is a multiple of 300 seconds
    if (intervalSeconds % 300 != 0) {
        cerr << "El intervalo debe ser un múltiplo de 300 segundos." << endl;
        return 1;
    }

    TString datos;  // File location
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

            // Reading the file and checking empty files
            cantArchivos++;
            cout << "Leyendo archivo:" << cantArchivos << endl;

            // Reading the file
            TFile *input = new TFile(fname.Data(), "READ");
            int test = input->GetNkeys();
            cout << "NKeys: " << test << endl;

            // Extracting variable info
            cout << "new TFIle READ" << endl;
            TTree *tree = (TTree *)input->Get("sdst::ScalerSummaryDataTree");
            cout << "Tree extraido" << endl;
            input->GetListOfKeys()->Print();

            if (test == 0) {
                continue;
            } else {
                tree->SetBranchAddress("fCorrectedScalerArrayMean", &mean);
                tree->SetBranchAddress("fGPSSecond", &gpstime);
                tree->SetBranchAddress("fMeanPressure", &press);
                tree->SetBranchAddress("fNumberOfStationsUsedInMean", &stations);
                int entries = tree->GetEntries();
                cout << "Cantidad de entradas: " << entries << endl;

                TH1F *histM = new TH1F("histM", "Histogram", 100, 1600, 1800);
                TH1F *histP = new TH1F("histP", "Histogram", 20, 850, 890);
                TH1F *histS = new TH1F("histS", "Histogram", 20, 600, 1660);

                for (int i = 0; i < entries; i++) {
                    tree->GetEntry(i);
                    gpsInterval.push_back(gpstime);
                    meanInterval.push_back(mean);
                    pressInterval.push_back(press);
                    statInterval.push_back(stations);
                }
                cout << "Creados vectores con los datos del tree" << endl;

                for (int i = 0; i < meanInterval.size(); i = i + (intervalSeconds / 300)) {
                	if (i + (intervalSeconds / 300) <= meanInterval.size()) {
        			for (int j = 0; j < (intervalSeconds / 300); j++) {
            				val = i + j;
            				tmp_mean = tmp_mean + meanInterval.at(val);
            				tmp_press = tmp_press + pressInterval.at(val);
            				tmp_station = tmp_station + statInterval.at(val);
            				histM->Fill(meanInterval.at(val));
        			}    
		tmp_gps = gpsInterval.at(i + ((intervalSeconds / 300) / 2));
                tmp_mean = tmp_mean / (intervalSeconds / 300);
                tmp_press = tmp_press / (intervalSeconds / 300);
                tmp_station = tmp_station / (intervalSeconds / 300);
                Double_t err = histM->GetRMS();
                mean_err.push_back(err);
                gpsInterval.push_back(tmp_gps);
                meanInterval.push_back(tmp_mean);
                pressInterval.push_back(tmp_press);
                statInterval.push_back(tmp_station);
                histM->Reset();
                tmp_gps = 0;
                tmp_mean = 0;
                tmp_press = 0;
                tmp_station = 0;
                }else{
			//Si el índice exede el tamaño del vector se sale
			break;
		}
		}
                cout << "Creados vectores para el intervalo deseado" << endl;

                if (salida.is_open()) {
                    cout << "Escribiendo el archivo de salida..." << endl;
                    UInt_t gps;
                    Double_t vmean;
                    Double_t vmerr;
                    Double_t vpres;
                    Double_t vstat;

		    //copia
		    //
			vector<UInt_t> gpsCopy = gpsInterval;
    			vector<Double_t> meanCopy = meanInterval;
    			vector<Double_t> meanErrCopy = mean_err;
    			vector<Float_t> pressCopy = pressInterval;
    			vector<Double_t> statCopy = statInterval;

                    for (int i = 0; i < meanCopy.size(); i++) {
                        gps = gpsCopy.at(i);
        		vmean = meanCopy.at(i);
        		vmerr = meanErrCopy.at(i);
        		vpres = pressCopy.at(i);
        		vstat = statCopy.at(i);
			salida << gps << "," << vmean << "," << vmerr << "," << vpres << "," << vstat << endl;
                    }
                    gpsInterval.clear();
                    meanInterval.clear();
                    mean_err.clear();
                    pressInterval.clear();
                    statInterval.clear();
                    cout << "Archivo creado con éxito :)" << endl;
                }
            }
        }
    }
    salida.close();
    return 0;
}

