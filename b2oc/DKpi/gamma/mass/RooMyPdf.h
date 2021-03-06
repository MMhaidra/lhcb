/*****************************************************************************
 * Project: RooFit                                                           *
 * Package: RooFitModels                                                     *
 *    File: $Id: RooMyPdf.rdl,v 1.9 2005/02/25 14:25:06 wverkerke Exp $
 * Authors:                                                                  *
 *   GR, Gerhard Raven,   UC San Diego,        raven@slac.stanford.edu       *
 *   DK, David Kirkby,    UC Irvine,         dkirkby@uci.edu                 *
 *   WV, Wouter Verkerke, UC Santa Barbara, verkerke@slac.stanford.edu       *
 *                                                                           *
 * Copyright (c) 2000-2005, Regents of the University of California          *
 *                          and Stanford University. All rights reserved.    *
 *                                                                           *
 * Redistribution and use in source and binary forms,                        *
 * with or without modification, are permitted according to the terms        *
 * listed in LICENSE (http://roofit.sourceforge.net/license.txt)             *
 *****************************************************************************/
#ifndef ROO_MY_KEYS
#define ROO_MY_KEYS

#include "RooAbsPdf.h"
#include "RooRealProxy.h"

class RooRealVar;

class RooMyPdf : public RooAbsPdf {
    public:
        enum Mirror { NoMirror, MirrorLeft, MirrorRight, MirrorBoth,
            MirrorAsymLeft, MirrorAsymLeftRight,
            MirrorAsymRight, MirrorLeftAsymRight,
            MirrorAsymBoth };
        RooMyPdf() {}
        RooMyPdf(const char *name, const char *title,
                RooAbsReal& x, RooAbsReal& shift, RooDataSet& data, Mirror mirror= NoMirror,
                Double_t rho=1);
        RooMyPdf(const RooMyPdf& other, const char* name=0);
        virtual TObject* clone(const char* newname) const {return new RooMyPdf(*this,newname); }
        virtual ~RooMyPdf();

        void LoadDataSet( RooDataSet& data);

    protected:

        RooRealProxy _x ;
        RooRealProxy _shift ;
        Double_t evaluate() const;

    private:

        Double_t evaluateFull(Double_t x) const;

        Int_t _nEvents;
        Double_t *_dataPts; //!
        Double_t *_weights; //!
        Double_t *_dataWgts; //[_nEvents]
        Double_t _sumWgt ;

        enum { _nPoints = 10000 };
        Double_t _lookupTable[_nPoints+1];

        Double_t g(Double_t x,Double_t sigma) const;

        Bool_t _mirrorLeft, _mirrorRight;
        Bool_t _asymLeft, _asymRight;

        // cached info on variable
        Char_t _varName[128];
        Double_t _lo, _hi, _binWidth;
        Double_t _rho;

        ClassDef(RooMyPdf,2) // Non-Parametric KEYS PDF
};

#endif
