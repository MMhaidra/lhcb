{
	gROOT->ProcessLine(".L lhcbStyle.C");
	lhcbStyle();
	gStyle->SetPalette(1,0);
	const Int_t NRGBs = 5;
	const Int_t NCont = 255;
	Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00};
	Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51};
	Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00};
	Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00};
	TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
	gStyle->SetNumberContours(NCont);
	gStyle->SetOptStat(0000);

	TFile* f = TFile::Open("hists/l0nothNew_sq5_all.root");
	TH2D* eff = (TH2D*)f->Get("efficiency");
	TH2D* errp = (TH2D*)f->Get("errorHi");
	TH2D* errm = (TH2D*)f->Get("errorLo");
	TH2D* errppc = errp->Clone("errorHiPc");
	TH2D* errmpc = errm->Clone("errorLoPc");

	TFile* f1 = TFile::Open("hists/l0h_sq5_Bs_errStat_asym.root");
	TH2D* errstatp = (TH2D*)f1->Get("errorHi");
	TH2D* errstatm = (TH2D*)f1->Get("errorLo");
	TH2D* errstatppc = errstatp->Clone("errorStatHiPc");
	TH2D* errstatmpc = errstatm->Clone("errorStatLoPc");

	TFile* f2 = TFile::Open("hists/l0h_sq5_errTable.root");
	TH2D* errtab = (TH2D*)f2->Get("error");
	TH2D* errtabpc = errtab->Clone("errorTabPc");

	errppc->Scale(100.);
	errppc->Divide(eff);
	errmpc->Scale(100.);
	errmpc->Divide(eff);
	errstatppc->Scale(100.);
	errstatppc->Divide(eff);
	errstatmpc->Scale(100.);
	errstatmpc->Divide(eff);
	errtabpc->Scale(100.);
	errtabpc->Divide(eff);

	TCanvas * canvas = new TCanvas("c2","c2");
	eff->SetLabelFont(62,"x");
	eff->SetLabelFont(62,"y");
	eff->SetTitleFont(62,"x");
	eff->SetTitleFont(62,"y");
	eff->SetTitleSize(0.06,"x");
	eff->SetTitleSize(0.06,"y");
	eff->SetLabelSize(0.05,"x");
	eff->SetLabelSize(0.05,"y");
	eff->SetXTitle("m'");
	eff->SetYTitle("#theta'");
	canvas->SetRightMargin(0.17);
	eff->GetZaxis()->SetRangeUser(0.95,1.10);
	eff->Draw("colztext30");
	canvas->SaveAs("../latex/figs/l0nothadCorr_eff.pdf");
	eff->Draw("colz");
	canvas->SaveAs("../latex/figs/l0nothadCorr_eff_nolabel.pdf");
	canvas->SaveAs("../ANAPlots/l0noth_eff.pdf");

	gStyle->SetPaintTextFormat("0.2f %%");

	errp->SetLabelFont(62,"x");
	errp->SetLabelFont(62,"y");
	errp->SetTitleFont(62,"x");
	errp->SetTitleFont(62,"y");
	errp->SetTitleSize(0.06,"x");
	errp->SetTitleSize(0.06,"y");
	errp->SetLabelSize(0.05,"x");
	errp->SetLabelSize(0.05,"y");
	errp->SetXTitle("m'");
	errp->SetYTitle("#theta'");
	canvas->SetRightMargin(0.17);
	errp->Draw("colz");
	errppc->Draw("text30same");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errp.pdf");

	errm->SetLabelFont(62,"x");
	errm->SetLabelFont(62,"y");
	errm->SetTitleFont(62,"x");
	errm->SetTitleFont(62,"y");
	errm->SetTitleSize(0.06,"x");
	errm->SetTitleSize(0.06,"y");
	errm->SetLabelSize(0.05,"x");
	errm->SetLabelSize(0.05,"y");
	errm->SetXTitle("m'");
	errm->SetYTitle("#theta'");
	canvas->SetRightMargin(0.17);
	errm->Draw("colz");
	errmpc->Draw("text30same");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errm.pdf");

	errstatp->SetLabelFont(62,"x");
	errstatp->SetLabelFont(62,"y");
	errstatp->SetTitleFont(62,"x");
	errstatp->SetTitleFont(62,"y");
	errstatp->SetTitleSize(0.06,"x");
	errstatp->SetTitleSize(0.06,"y");
	errstatp->SetLabelSize(0.05,"x");
	errstatp->SetLabelSize(0.05,"y");
	errstatp->SetXTitle("m'");
	errstatp->SetYTitle("#theta'");
	canvas->SetRightMargin(0.17);
	errstatp->Draw("colz");
	errstatppc->Draw("text30same");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errpStats.pdf");

	errstatm->SetLabelFont(62,"x");
	errstatm->SetLabelFont(62,"y");
	errstatm->SetTitleFont(62,"x");
	errstatm->SetTitleFont(62,"y");
	errstatm->SetTitleSize(0.06,"x");
	errstatm->SetTitleSize(0.06,"y");
	errstatm->SetLabelSize(0.05,"x");
	errstatm->SetLabelSize(0.05,"y");
	errstatm->SetXTitle("m'");
	errstatm->SetYTitle("#theta'");
	canvas->SetRightMargin(0.17);
	errstatm->Draw("colz");
	errstatmpc->Draw("text30same");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errmStats.pdf");

	errtab->SetLabelFont(62,"x");
	errtab->SetLabelFont(62,"y");
	errtab->SetTitleFont(62,"x");
	errtab->SetTitleFont(62,"y");
	errtab->SetTitleSize(0.06,"x");
	errtab->SetTitleSize(0.06,"y");
	errtab->SetLabelSize(0.05,"x");
	errtab->SetLabelSize(0.05,"y");
	errtab->SetXTitle("m'");
	errtab->SetYTitle("#theta'");
	canvas->SetRightMargin(0.17);
	errtab->Draw("colz");
	errtabpc->Draw("text30same");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errTable.pdf");

	errppc->Scale(0.01);
	errmpc->Scale(0.01);
	errstatppc->Scale(0.01);
	errstatmpc->Scale(0.01);
	errtabpc->Scale(0.01);

	gStyle->SetPaintTextFormat("g");

	errppc->SetLabelFont(62,"x");
	errppc->SetLabelFont(62,"y");
	errppc->SetTitleFont(62,"x");
	errppc->SetTitleFont(62,"y");
	errppc->SetTitleSize(0.06,"x");
	errppc->SetTitleSize(0.06,"y");
	errppc->SetLabelSize(0.05,"x");
	errppc->SetLabelSize(0.05,"y");
	errppc->SetXTitle("m'");
	errppc->SetYTitle("#theta'");
	errppc->GetZaxis()->SetRangeUser(0.01,0.035);
	canvas->SetRightMargin(0.17);
	errppc->Draw("colztext30");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errp_frac.pdf");
	errppc->Draw("colz");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errp_frac_nolabel.pdf");
	canvas->SaveAs("../ANAPlots/l0noth_errp.pdf");

	errmpc->SetLabelFont(62,"x");
	errmpc->SetLabelFont(62,"y");
	errmpc->SetTitleFont(62,"x");
	errmpc->SetTitleFont(62,"y");
	errmpc->SetTitleSize(0.06,"x");
	errmpc->SetTitleSize(0.06,"y");
	errmpc->SetLabelSize(0.05,"x");
	errmpc->SetLabelSize(0.05,"y");
	errmpc->SetXTitle("m'");
	errmpc->SetYTitle("#theta'");
	errmpc->GetZaxis()->SetRangeUser(0.01,0.035);
	canvas->SetRightMargin(0.17);
	errmpc->Draw("colztext30");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errm_frac.pdf");
	errmpc->Draw("colz");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errm_frac_nolabel.pdf");
	canvas->SaveAs("../ANAPlots/l0noth_errm.pdf");

	errstatppc->SetLabelFont(62,"x");
	errstatppc->SetLabelFont(62,"y");
	errstatppc->SetTitleFont(62,"x");
	errstatppc->SetTitleFont(62,"y");
	errstatppc->SetTitleSize(0.06,"x");
	errstatppc->SetTitleSize(0.06,"y");
	errstatppc->SetLabelSize(0.05,"x");
	errstatppc->SetLabelSize(0.05,"y");
	errstatppc->SetXTitle("m'");
	errstatppc->SetYTitle("#theta'");
	errstatppc->GetZaxis()->SetRangeUser(0.01,0.035);
	canvas->SetRightMargin(0.17);
	errstatppc->Draw("colztext30");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errpStat_frac.pdf");
	errstatppc->Draw("colz");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errpStat_frac_nolabel.pdf");
	canvas->SaveAs("../ANAPlots/l0noth_errp_stat.pdf");

	errstatmpc->SetLabelFont(62,"x");
	errstatmpc->SetLabelFont(62,"y");
	errstatmpc->SetTitleFont(62,"x");
	errstatmpc->SetTitleFont(62,"y");
	errstatmpc->SetTitleSize(0.06,"x");
	errstatmpc->SetTitleSize(0.06,"y");
	errstatmpc->SetLabelSize(0.05,"x");
	errstatmpc->SetLabelSize(0.05,"y");
	errstatmpc->SetXTitle("m'");
	errstatmpc->SetYTitle("#theta'");
	errstatmpc->GetZaxis()->SetRangeUser(0.01,0.035);
	canvas->SetRightMargin(0.17);
	errstatmpc->Draw("colztext30");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errmStat_frac.pdf");
	errstatmpc->Draw("colz");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errmStat_frac_nolabel.pdf");
	canvas->SaveAs("../ANAPlots/l0noth_errm_stat.pdf");

	errtabpc->SetLabelFont(62,"x");
	errtabpc->SetLabelFont(62,"y");
	errtabpc->SetTitleFont(62,"x");
	errtabpc->SetTitleFont(62,"y");
	errtabpc->SetTitleSize(0.06,"x");
	errtabpc->SetTitleSize(0.06,"y");
	errtabpc->SetLabelSize(0.05,"x");
	errtabpc->SetLabelSize(0.05,"y");
	errtabpc->SetXTitle("m'");
	errtabpc->SetYTitle("#theta'");
	errtabpc->GetZaxis()->SetRangeUser(0.0000,0.0002);
	canvas->SetRightMargin(0.17);
	errtabpc->Draw("colztext30");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errTable_frac.pdf");
	errtabpc->Draw("colz");
	canvas->SaveAs("../latex/figs/l0nothadCorr_errTable_frac_nolabel.pdf");
	canvas->SaveAs("../ANAPlots/l0noth_err_table.pdf");

   std::cout << eff->GetBinContent(eff->GetMinimumBin())       << "-" << eff->GetBinContent(eff->GetMaximumBin())       << std::endl;
   std::cout << errppc->GetBinContent(errppc->GetMinimumBin()) << "-" << errppc->GetBinContent(errppc->GetMaximumBin()) << std::endl;
   std::cout << errmpc->GetBinContent(errmpc->GetMinimumBin()) << "-" << errmpc->GetBinContent(errmpc->GetMaximumBin()) << std::endl;
   std::cout << errtabpc->GetBinContent(errtabpc->GetMinimumBin())     << "-" << errtabpc->GetBinContent(errtabpc->GetMaximumBin())     << std::endl;
   std::cout << errstatppc->GetBinContent(errstatppc->GetMinimumBin()) << "-" << errstatppc->GetBinContent(errstatppc->GetMaximumBin()) << std::endl;
   std::cout << errstatmpc->GetBinContent(errstatmpc->GetMinimumBin()) << "-" << errstatmpc->GetBinContent(errstatmpc->GetMaximumBin()) << std::endl;
}
