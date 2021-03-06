#include <TFile.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TString.h>

int main() {
   Int_t nBins(5);
   std::vector<TH1D*> hists;

   for(Int_t j=1; j<=nBins; ++j) {
      for(Int_t i=1; i<=nBins; ++i) {
         TString hName("h_");
	 hName += i;
	 hName += "_";
	 hName += j;

         hists.push_back(new TH1D(hName,"",100,0.8,1.2));
      }
   }

   for(Int_t i=0; i<1000; ++i) {
      TString fName("bootstrapped/l0h_sq_Bd_effs");
      fName += i;
      fName += ".root";

      TFile* f = TFile::Open(fName);
      TH2D* h = (TH2D*)f->Get("ratio");
   
      for(Int_t i=1; i<=nBins; ++i) {
         for(Int_t j=1; j<=nBins; ++j) {
            hists[(i-1)+nBins*(j-1)]->Fill(h->GetBinContent(i,j));
         }
      }
      f->Close();
   }

   TString fileName("l0h_sq_Bd_bootstrapped.root");
   TFile* outfile = new TFile(fileName,"RECREATE");
   for(Int_t j=1; j<=nBins; ++j) {
      for(Int_t i=1; i<=nBins; ++i) {
         hists[(i-1)+nBins*(j-1)]->Write();
      }
   }
   outfile->Close();
}
