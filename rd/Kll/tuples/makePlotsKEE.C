{

	TFile* f = TFile::Open("/Disk/ecdf-nfs-ppe/lhcb/dcraik/DATA_2011_2012_LPT_PreSel_addCorrMass_NNA_TrigVeto_NN95_hop4k.root");
	TTree* t = dynamic_cast<TTree*>(f->Get("DecayTree"));
	gROOT->ProcessLine(".L lhcbStyle.C");
	lhcbStyle();
	gStyle->SetOptStat(0);
	gStyle->SetOptStat(0000);
	gStyle->SetPalette(1,0);
	const Int_t NRGBs = 5;
	const Int_t NCont = 255;
	Double_t stops[NRGBs] = { 0.00, 0.25, 0.50, 0.75, 1.00};
	Double_t red[NRGBs]   = { 1.00, 1.00, 1.00, 1.00, 0.00};
	Double_t green[NRGBs] = { 1.00, 0.95, 0.50, 0.00, 0.00};
	Double_t blue[NRGBs]  = { 1.00, 0.00, 0.00, 0.00, 0.00};
	TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
	gStyle->SetNumberContours(NCont);

	TH1D h("h","",80,5170,5970);
	h.SetYTitle("Candidates / 10 MeV/#it{c}^{2}");
	h.SetXTitle("#it{m}(#it{Kee}) [MeV/#it{c}^{2}]");

	TH1D h2("h2","",100,0.,25.);
	h2.SetYTitle("Candidates / 0.25 GeV^{2}/#it{c}^{4}");
	h2.SetXTitle("#it{q}^{2} [GeV^{2}/#it{c}^{4}]");

	TH2D h3("h3","",80,5170,5570,100,0.,25.);
	h3.SetYTitle("#it{q}^{2} [GeV^{2}/#it{c}^{4}]");
	h3.SetXTitle("#it{m}(#it{Kee}) [MeV/#it{c}^{2}]");

	TCanvas can;

	t->Draw("B_DTF_PV_Mmeas>>h","JPs_M**2>1.1e6 && JPs_M**2<6.0e6","");
	can.SaveAs("Kee_mB_Q17.pdf");

	can.SetLogz();
	t->Draw("JPs_M**2./1.e6:B_DTF_PV_Mmeas>>h3","","col");
	can.SaveAs("Kee_q2_mB.pdf");

	can.SetLogy();
	t->Draw("JPs_M**2./1.e6>>h2","","");
	can.SaveAs("Kee_q2.pdf");
}
