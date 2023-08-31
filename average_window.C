//C++
#include <algorithm>
#include <vector>
#include <cstring>
#include <string>
#include <cstdlib>
#include <fstream>
#include <iostream>
using namespace std;

//ROOT
#include "TTree.h"
#include "TFile.h"
#include "TROOT.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TVectorT.h"
#include "TSystemDirectory.h"
#include "TMath.h"
#include "TH1F.h"
//
//
//----------------------THIS CODE CALCULATES THE AVERAGE OF A DAY OF SECONDLY DATA
//----------------------MAKING A MOVING WINDOW

int main(){
    TCanvas *c1 = new TCanvas();
//create variables
	Double_t mean;
	Double_t meanVM;
	Double_t stdvVM;
	Float_t pressVM;
	UInt_t tmp_gps;
	Double_t err;
	UInt_t gpstime;
	UInt_t gps;
	Float_t press;
	UInt_t stations;
	vector<Double_t> mean900;
	vector<Double_t> mean_err;
	vector<Float_t> press900;
	vector<Double_t> stat900;
	vector<UInt_t> gps300;
	vector<Double_t> mean300;
	vector<Float_t> press300;
	vector<Double_t> stat300;
	//Creando banderas para más adelante:
	int cantArchivos = 0;
	bool primerArchivo =true;
        //Creando un archivo de salida:
	ofstream salida;
	salida.open("VM_PRUEBA.csv",ios::out);
        //Configuración para abrir los archivos y leerlos
	TString datos; // ID para el código
    	datos = "./";  // Localización
	TSystemDirectory dir(datos, datos); 
	//
	//Lectura de los archivos
	TList *files = dir.GetListOfFiles();
	if(files){
		TSystemFile *file;
		TString fname;
		TString archivo;
		TIter next(files);
		while((file=(TSystemFile*)next())){//Inicia el while
			fname = file->GetName(); //Se extrae el nombre del archivo para poderlo evaluar
			if (!file->IsDirectory() && fname.EndsWith(".root")){
				archivo = datos + fname;
				cout << archivo << endl; //Imprimo el nombre del archivo en pantalla
			}else{
				continue; //Si no cumple continua con el siguiente archivo y así...
			}
		//Lectura del archivo y Checking empty files...
			cantArchivos++;
			cout << "Leyendo archivo:"<<cantArchivos<<endl;
		// Lectura del archivo
			TFile *input = new TFile(fname.Data(),"READ");
		//PRUEBA filtrar los archivos vacíos
			int test = input->GetNkeys();
			cout <<"NKeys: "<<test<<endl;
		//Extrayendo info de variables...
			cout<<"new TFIle READ"<<endl;
			TTree *tree = (TTree*)input->Get("sdst::ScalerSummaryDataTree");
			cout<<"Tree extraido"<<endl;
			input->GetListOfKeys()->Print();
		//Si el test es cero se sigue buscando líneas
			if(test == 0){
				continue;
			}else{ 
		//Si no está vacío entonces se extraen las variables todas con &mean &gpstime &press &stations
				tree->SetBranchAddress("fCorrectedScalerArrayMean",&mean);
	                        tree->SetBranchAddress("fGPSSecond",&gpstime);
				tree->SetBranchAddress("fMeanPressure",&press);
				tree->SetBranchAddress("fNumberOfStationsUsedInMean",&stations);
				int entries = tree->GetEntries();
	        		cout <<"Cantidad de entradas: "<< entries << endl; //Se imprime la cantidad de entradas
		//Se crean histogramas que ahorita se llenan
				TH1F *histM = new TH1F("histM", "Histogram",100,1600,1800); 
				TH1F *histP = new TH1F("histP", "Histogram",20,850,890);
				TH1F *histS = new TH1F("histS", "Histogram",20,600,1660);
		//Vamos a llenar vectores con las variables que se están leyendo
				for(int i=0; i<entries;i++){  //ESTAS SON LAS ENTRADAS CADA 300S
					tree->GetEntry(i);
					gps300.push_back(gpstime);
					mean300.push_back(mean);
					press300.push_back(press);
					stat300.push_back(stations);
					//cout << "Línea numero: "<< i <<" Scaler value: "<<mean300.at(i)<<endl;
				}
				cout << "Creados vectores de 300s"<<endl;
		//--VM--Rutina para calcular el promedio móvil
				for(int i=0;i<entries;i= i+1){ //COMIENZO FOR VM
					for(int a=i; a<(i+3); a=a+1){
						meanVM = meanVM + gps300.at(a);
						pressVM = pressVM + press300.at(a);
						stdvVM = stdvVM + stat300.at(a);
					}
					meanVM = meanVM/3;
					pressVM = pressVM/3;
					stdvVM = stdvVM/3;
					mean900.push_back(meanVM);
					press900.push_back(pressVM);
					stat900.push_back(stdvVM);
					meanVM = 0;
					pressVM = 0;
					stdvVM = 0;
		//--VM--fin rutina
					histM->Fill(mean900.at(i)); //ERROR
					Double_t err = histM->GetRMS();//ERROR (CÁLCULO DEL RMS DE CADA VARIABLE)
					mean_err.push_back(err);//ERROR
					histM->Reset();//ERROR
				}
		//FIN DEL FOR VM
		//
				cout << "Creados vectores de 900s"<<endl;
		//
				if (salida.is_open()){
					cout <<"Escribiendo el archivo de salida..."<<endl;
					UInt_t gps;
					Double_t vmean;
					Double_t vmerr;//ERROR
					Double_t vpres;
					Double_t vstat;
					for(int i=0; i < press900.size(); i++){
						gps = gps900.at(i);
						vmean = mean900.at(i);
						vmerr = mean_err.at(i);
						vpres = press900.at(i);
						vstat = stat900.at(i);
						salida << gps<<","<< vmean <<","<< vmerr <<","<<vpres<<","<< vstat<<endl;
					}
					gps900.clear();
        				mean900.clear();
        				mean_err.clear();
        				press900.clear();
        				stat900.clear();
        				gps300.clear();
        				mean300.clear();
        				press300.clear();
        				stat300.clear();
					cout << "Archivo creado con éxito :)"<<endl;
				}
				return 0;
				}
			salida.close();
			}
	return 0;
}
