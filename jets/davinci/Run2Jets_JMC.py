#!/bin/env python

# Data type configuration.
from GaudiKernel import SystemOfUnits as Units
Type     = 'MC'
JetPtMin = 10 * Units.GeV

### Data.
#from GaudiConf import IOHelper
#IOHelper('ROOT').inputFiles([
##'/eos/lhcb/grid/prod/lhcb/MC/Dev/LDST/00042952/0000/00042952_00000001_1.ldst' #/tmp/dcraik/00042952_00000002_1.ldst' #/data/dst/MC15.MD.49000004.1.00.dst'
##    '/eos/lhcb/grid/prod/lhcb/MC/Dev/LDST/00042982/0000/00042982_00000002_1.ldst'#light
#    '/eos/lhcb/grid/prod/lhcb/MC/Dev/LDST/00042950/0000/00042950_00000001_1.ldst'#charm
##    '/eos/lhcb/grid/prod/lhcb/MC/Dev/LDST/00042972/0000/00042972_00000003_1.ldst'#beauty
#    ],
#    clear = True)
##Type = 'MC'

# Create the generated jets.
from Configurables import McParticleFlow, McJetBuilder
genPF = McParticleFlow('genPF')
genPF.Inputs = [
    ['PID',        'ban',       '12,-12,14,-14,16,-16'],
    ['PID',        'particle',  '321,211,130,3222,310,3122,3112,3312,3322,'
     '30221,9010221,-321,-211,-130,-3222,-310,-3122,-3112,-3312,-3322,-30221,'
     '-9010221,443,-443'],
    ['MCParticle', 'daughters', 'MC/Particles']
    ]
genPF.Output = 'Phys/PF/MCParticles'
genJB = McJetBuilder('genJB')
genJB.JetPtMin = JetPtMin
genJB.JetR = 0.5
genJB.ChrVrt = True
genJB.NeuVrt = True
genJB.Inputs = [genPF.Output]
genJB.Output = 'Phys/JB/MCParticles'

# Create the reconstructed jets.
from Configurables import HltParticleFlow, HltJetBuilder
from StandardParticles import (StdLooseKsDD, StdLooseKsLL, StdLooseKsLD,
                               StdLooseLambdaDD, StdLooseLambdaLL, 
                               StdLooseLambdaLD)
recPF = HltParticleFlow('recPF')
recPF.Inputs = [
    ['Particle',       'particle', StdLooseKsDD.outputLocation()],
    ['Particle',       'particle', StdLooseKsLL.outputLocation()],
    ['Particle',       'particle', StdLooseKsLD.outputLocation()],
    ['Particle',       'particle', StdLooseLambdaDD.outputLocation()],
    ['Particle',       'particle', StdLooseLambdaLL.outputLocation()],
    ['Particle',       'particle', StdLooseLambdaLD.outputLocation()],
    ['ProtoParticle',  'best',     'Rec/ProtoP/Charged'],
    ['ProtoParticle',  'gamma',    'Rec/ProtoP/Neutrals']
    ]
recPF.Output = 'Phys/PF/Particles'
recPF.ProBestNames = ['mu+', 'e+', 'p+', 'K+', 'pi+']
recPF.ProBestKeys  = [701,   700,  704,  703,  702]
recPF.ProBestMins  = [0.5,   0.5,  0.5,  0.5,  0.5]
recPF.EcalBest = True
recPF.SprRecover = False
recPF.TrkLnErrMax = 10
recPF.TrkUpErrMax = 10
recPF.TrkDnErrMax = 10
recJB = HltJetBuilder('recJB')
recJB.JetEcPath = ''
recJB.Inputs = [recPF.Output]
recJB.Output = 'Phys/JB/Particles'
recJB.JetPtMin = JetPtMin

from commonSelections import *

from PhysSelPython.Wrappers import SelectionSequence
#recSVs_seq = SelectionSequence('recSVs_Seq', TopSelection=recSVs)
#recMus_seq = SelectionSequence('recMus_Seq', TopSelection=recMus)

D0_seq = SelectionSequence('D0_Seq', TopSelection=recD0)
Dp_seq = SelectionSequence('Dp_Seq', TopSelection=recDp)
Ds_seq = SelectionSequence('Ds_Seq', TopSelection=recDs)
Lc_seq = SelectionSequence('Lc_Seq', TopSelection=recLc)
D02K3pi_seq = SelectionSequence('D2K3pi0_Seq', TopSelection=recD02K3pi)

# Turbo/DaVinci configuration.
from Configurables import DstConf, TurboConf, DaVinci
DaVinci().Simulation = True
DaVinci().appendToMainSequence([genPF, genJB, recPF, recJB])
DaVinci().appendToMainSequence([recSVs_seq.sequence(), recMus_seq.sequence()])
DaVinci().appendToMainSequence([D0_seq.sequence(), Dp_seq.sequence(), Ds_seq.sequence(),  Lc_seq.sequence(), D02K3pi_seq.sequence()])
DaVinci().DataType = '2015'
#DaVinci().EventPreFilters = fltrs.filters ('Filters')

# Configure the BDT tagger.
from Configurables import LoKi__BDTTag
tagger = LoKi__BDTTag()
tagger.NbvSelect = False

# Access to classes.
from collections import OrderedDict
import ROOT, array, GaudiPython
from GaudiPython.Bindings import gbl
STD  = gbl.std
LHCB = gbl.LHCb

from Ntuple import Ntuple

## Simple ntuple class.
#class Ntuple:
#    """
#    Class to store an ntuple.
#    """
#    def __init__(self, name, tes, toolSvc, detSvc):
#        """
#        Initialize the ntuple with the needed tools.
#        """
#        ROOT.gInterpreter.ProcessLine(
#            "#include \"/cvmfs/lhcb.cern.ch/lib/lhcb/HLT/"
#            "HLT_v25r4/Hlt/HltDisplVertices/Kernel/"
#            "IMatterVeto.h\"")
#        self.pvrTool = toolSvc.create(
#            'GenericParticle2PVRelator<_p2PVWithIPChi2, '
#            'OfflineDistanceCalculatorName>/P2PVWithIPChi2',
#            interface = 'IRelatedPVFinder')
#        self.tagTool = toolSvc.create(
#            'LoKi::BDTTag',
#            interface = 'IJetTagTool')
#        self.genTool = toolSvc.create(
#            'DaVinciSmartAssociator',
#            interface = 'IParticle2MCWeightedAssociator')
#        self.mtrTool = toolSvc.create(
#            'MatterVetoTool',
#            interface = 'IMatterVeto')
#        self.velTool = toolSvc.create(
#            'VeloExpectation',
#            interface = 'IVeloExpectation')
#        self.dstTool = toolSvc.create(
#            'LoKi::TrgDistanceCalculator',
#            interface = 'IDistanceCalculator')
#        self.ltTool = toolSvc.create(
#            'LoKi::LifetimeFitter',
#            interface = 'ILifetimeFitter')
#        self.trkTool = toolSvc.create(
#            'TrackMasterExtrapolator',
#            interface = 'ITrackExtrapolator')
#        self.pidTool = toolSvc.create(
#            'ANNGlobalPID::ChargedProtoANNPIDTool',
#            interface = 'ANNGlobalPID::IChargedProtoANNPIDTool')
#        self.detTool = detSvc[
#            '/dd/Structure/LHCb/BeforeMagnetRegion/Velo']
#        self.stable = [11,-11,13,-13,211,-211,321,-321,2212,-2212,2112,-2112,22,111,310,130,311,-311]
#        self.Ds = [411,-411,421,-421,431,-431,4122,-4122]
#        self.tes     = tes
#        self.saved   = {}
#        self.ntuple  = OrderedDict()
#        self.tfile   = ROOT.TFile('output.root', 'RECREATE')
#        self.ttree   = ROOT.TTree('data', 'data')
#        self.vrs     = {}
#        mom = ['px', 'py', 'pz', 'e']
#        pos = ['x', 'y', 'z']
#        cov = ['dx', 'dy', 'dz', 'chi2', 'ndof']
#        self.init('gen', ['idx_pvr', 'idx_jet', 'idx_prnt', 'pid', 'q'] + mom + pos + ['prnt_pid', 'res_pid', 'from_sig'])#, 'prnt_key', 'key'])
#        self.init('pvr', pos + cov)
#        self.init('svr', ['idx_pvr', 'idx_jet'] + [
#                'idx_trk%i' % i for i in range(0, 10)] + 
#                  mom + pos + ['m', 'm_cor', 'm_cor_err', 'm_cor_err_full', 'pt', 'fd_min', 'fd_chi2', 'chi2', 'ip_chi2_sum', 'abs_q_sum', 'tau', 'ntrk', 'ntrk_jet', 'jet_dr', 'jet_pt', 'pass', 'bdt0', 'bdt1'])
#        self.init('jet', ['idx_pvr', 'ntrk', 'nneu'] + mom)
#        self.init('trk', ['idx_gen', 'idx_pvr', 'idx_jet'] + mom +
#                  ['pid', 'q', 'ip', 'ip_chi2', 'pnn_e', 'pnn_mu', 'pnn_pi',
#                   'pnn_k', 'pnn_p', 'pnn_ghost', 'ecal', 'hcal', 'prb_ghost', 'type', 'is_mu',
#                   'vid', 'x', 'y', 'z'])# + ['vhit%i' % i for i in range(0, 61)])# + [
#                   #'vz%i' % i for i in range(0, 61)])
#        self.init('neu', ['idx_gen', 'idx_jet'] + mom + ['pid'])
#        self.init('d0', ['idx_pvr','idx_jet'] + mom + pos + ['m', 'ip', 'ip_chi2', 'vtx_chi2', 'vtx_ndof', 'fd', 'fd_chi2', 'tau', 'tau_err', 'tau_chi2', 'ntrk_jet'] + ['idx_trk%i' % i for i in range(0, 2)]) 
#        self.init('dp', ['idx_pvr','idx_jet'] + mom + pos + ['m', 'ip', 'ip_chi2', 'vtx_chi2', 'vtx_ndof', 'fd', 'fd_chi2', 'tau', 'tau_err', 'tau_chi2', 'ntrk_jet'] + ['idx_trk%i' % i for i in range(0, 3)]) 
#        self.init('ds', ['idx_pvr','idx_jet'] + mom + pos + ['m', 'ip', 'ip_chi2', 'vtx_chi2', 'vtx_ndof', 'fd', 'fd_chi2', 'tau', 'tau_err', 'tau_chi2', 'ntrk_jet'] + ['idx_trk%i' % i for i in range(0, 3)]) 
#        self.init('lc', ['idx_pvr','idx_jet'] + mom + pos + ['m', 'ip', 'ip_chi2', 'vtx_chi2', 'vtx_ndof', 'fd', 'fd_chi2', 'tau', 'tau_err', 'tau_chi2', 'ntrk_jet'] + ['idx_trk%i' % i for i in range(0, 3)]) 
#        self.init('k3pi', ['idx_pvr','idx_jet'] + mom + pos + ['m', 'ip', 'ip_chi2', 'vtx_chi2', 'vtx_ndof', 'fd', 'fd_chi2', 'tau', 'tau_err', 'tau_chi2', 'ntrk_jet'] + ['idx_trk%i' % i for i in range(0, 4)]) 
#        self.ntuple['evt_pvr_n'] = array.array('d', [-1])
#        self.ntuple['evt_trk_n'] = array.array('d', [-1])
#        for key, val in self.ntuple.iteritems():
#            if type(val) is array.array: self.ttree.Branch(key, val, key + '/D')
#            else: self.ttree.Branch(key, val)
#    def init(self, pre, vrs):
#        """
#        Initialize a set of variables.
#        """
#        self.saved[pre] = {}
#        self.vrs[pre]   = vrs
#        for v in vrs: self.ntuple['%s_%s' % (pre, v)] = ROOT.vector('double')()
#    def key(self, obj):
#        """
#        Generate the key for an object.
#        """
#        key = None
#        try: 
#            key = (obj.momentum().Px(), obj.momentum().Py(), 
#                   obj.momentum().Pz())
#            try:
#                trk = obj.proto().track()
#                key = (trk.momentum().X(), trk.momentum().Y(), 
#                       trk.momentum().Z())
#            except:
#                try:
#                    pos = obj.proto().calo()[0].position()
#                    key = (pos.x(), pos.y(), pos.z(), pos.e())
#                except: pass
#        except:
#            try: key = (obj.position().X(), obj.position().Y(),
#                        obj.position().Z())
#            except: pass
#        return key
#    def close(self):
#        """
#        Close the ntuple.
#        """
#        self.tfile.Write(); self.tfile.Close()
#    def clear(self):
#        """
#        Clear the ntuple.
#        """
#        for key, val in self.saved.iteritems(): val.clear()
#        for key, val in self.ntuple.iteritems():
#            if type(val) is array.array: val[0] = -1
#            else: val.clear()
#    def lookupVeloStation(self, z):
#        return {   4 :  0,   6 :  1,  19 :  2,  21 :  3,  34 :  4,  36 :  5,
#                  49 :  6,  51 :  7,  64 :  8,  66 :  9,  79 : 10,  81 : 11,
#                  93 : 12,  96 : 13, 109 : 14, 111 : 15, 123 : 16, 126 : 17,
#                 139 : 18, 141 : 19, 153 : 20, 156 : 21, 169 : 22, 171 : 23,
#                 184 : 24, 186 : 25, 198 : 26, 201 : 27, 214 : 28, 216 : 29,
#                 229 : 30, 231 : 31, 244 : 32, 246 : 33, 258 : 34, 261 : 35,
#                 273 : 36, 276 : 37, 289 : 38, 291 : 39, 434 : 40, 436 : 41,
#                 449 : 42, 451 : 43, 584 : 44, 586 : 45, 599 : 46, 601 : 47,
#                 634 : 48, 636 : 49, 648 : 50, 651 : 51, 684 : 52, 686 : 53,
#                 699 : 54, 701 : 55, 734 : 56, 736 : 57, 748 : 58, 751 : 59
#               }.get(int(floor(z)),-1)
#
#    def children(self, gen):
#        parts = []
#        for vtx in gen.endVertices():
#            for part in vtx.products():
#                parts += [part]
#        return parts
#
# # Return the final charged children of a generated particle.
#    def finalChildren(self, gen):
#        inters = []
#        finals = []
#        if not gen: return []
#        final = []
#        decay = self.children(gen)
#        while len(decay) > 0:
#            tmp = self.children(decay[-1])
#            pid = int(decay[-1].particleID().abspid())
#            if (len(tmp) == 0 or pid in self.stable):
#                if pid != 22: finals += [pid]
#                final += [decay[-1]]
#                decay.pop()
#            else:
#                if pid != 22: inters += [pid]
#                decay.pop()
#                decay += tmp
#        if gen.particleID().abspid() == 15:
#            while finals[-1] != 16:
#                final.pop(); finals.pop()
#        finals.sort()
#        inters.sort()
#        return (final, inters, finals)
#
#    def fill(self, key = None, val = None, idx = None, vrs = None):
#        """
#        Fill the ntuple for either an event or an object.
#        """
#        if key == None and val == None and idx == None and vrs == None:
#            self.tfile.Cd(''); self.ttree.Fill()
#        elif vrs != None and key != None:
#            pre = key
#            for key in self.vrs[pre]:
#                val = vrs[key] if key in vrs else -1
#                self.ntuple[pre + '_' + key].push_back(val)
#        elif key in self.ntuple: 
#            if idx == None: self.ntuple[key].push_back(val)
#            elif idx < len(self.ntuple[key]): self.ntuple[key][idx] = val
#    def fillMom(self, obj, vrs):
#        if not obj: return
#        vrs['px'] = obj.Px()
#        vrs['py'] = obj.Py()
#        vrs['pz'] = obj.Pz()
#        vrs['e' ] = obj.E()
#    def fillPid(self, obj, vrs):
#        if not obj: return
#        vrs['pid'] = obj.pid()
#        vrs['q'  ] = float(obj.threeCharge())/3.0
#    def fillPro(self, obj, vrs):
#        if not obj: return
#        if obj.muonPID(): vrs['is_mu'] = obj.muonPID().IsMuon()
#        vrs['pnn_e' ] = self.pidTool.annPID(obj, ROOT.LHCb.ParticleID(11),   "MC15TuneV1").value #obj.info(700, -100)
#        vrs['pnn_mu'] = self.pidTool.annPID(obj, ROOT.LHCb.ParticleID(13),   "MC15TuneV1").value #obj.info(701, -100)
#        vrs['pnn_pi'] = self.pidTool.annPID(obj, ROOT.LHCb.ParticleID(211),  "MC15TuneV1").value #obj.info(702, -100)
#        vrs['pnn_k' ] = self.pidTool.annPID(obj, ROOT.LHCb.ParticleID(321),  "MC15TuneV1").value #obj.info(703, -100)
#        vrs['pnn_p' ] = self.pidTool.annPID(obj, ROOT.LHCb.ParticleID(2212), "MC15TuneV1").value #obj.info(704, -100)
#        vrs['pnn_ghost' ] = self.pidTool.annPID(obj, ROOT.LHCb.ParticleID(0),"MC15TuneV1").value
#        vrs['ecal']   = obj.info(332, -100)
#        vrs['hcal']   = obj.info(333, -100)
#    def fillTrk(self, obj, pid, vrs):
#        if not obj or not pid: return
#        vrs['prb_ghost'] = obj.ghostProbability()
#        vrs['type'] = obj.type()
#        vrs['vid'] = 1.0
#        vids = []
#        for vid in obj.lhcbIDs():
#            if vid.isVelo():
#                vrs['vid'] *= float(vid.veloID().channelID())/1000000.0
#                vids += [(self.detTool.sensor(vid.veloID()).z(), 
#                          vid.veloID().channelID())]
#                #station = self.lookupVeloStation(vids[-1][0])
#                #vrs['vz%i' % (station)] = vids[-1][0]
#                #vrs['vhit%i' % (station)] = vids[-1][1]
#        vids.sort()
#        sta = LHCB.StateVector()
#        if len(vids) > 0: self.trkTool.propagate(obj, vids[0][0], sta, pid)
#        vrs['x'] = sta.x()
#        vrs['y'] = sta.y()
#        vrs['z'] = sta.z()
#    def fillDst(self, obj, pvr, dst, vrs):
#        if not obj or not pvr: return
#        val, valChi2 = ROOT.Double(-1), ROOT.Double(-1)
#        self.dstTool.distance(obj, pvr, val, valChi2)
#        vrs[dst] = val;
#        vrs[dst + '_chi2'] = valChi2;
#    def fillLifetime(self, obj, pvr, vrs):
#        if not obj or not pvr: return
#        val, valErr, valChi2 = ROOT.Double(-1), ROOT.Double(-1), ROOT.Double(-1)
#        self.ltTool.fit(pvr, obj, val, valErr, valChi2)
#        vrs['tau'] = val;
#        vrs['tau_err'] = valErr;
#        vrs['tau_chi2'] = valChi2;
#    def fillVtx(self, obj, vrs):
#        vrs['vtx_chi2'] = obj.chi2()
#        vrs['vtx_ndof'] = obj.nDoF()
#    def fillPos(self, obj, vrs):
#        if not obj: return
#        pos = obj.position()
#        vrs['x'] = pos.X()
#        vrs['y'] = pos.Y()
#        vrs['z'] = pos.Z()
#        vrs['in_mtr'] = self.mtrTool.isInMatter(pos)
#    def fillCov(self, obj, vrs):
#        try:
#            cov = obj.covMatrix()
#            vrs['ndof'] = obj.nDoF()
#            vrs['chi2'] = obj.chi2()
#            vrs['dx']   = cov[0][0]
#            vrs['dy']   = cov[1][1]
#            vrs['dz']   = cov[2][2]
#        except: pass
#    def fillPvr(self, obj, vrs):
#        if not obj: return
#        vrs['idx_pvr'] = self.addPvr(obj)
#    def fillGen(self, obj, vrs):
#        if not obj: return
#        gen = None; wgt = 0; rels = self.genTool.relatedMCPs(obj)
#        for rel in rels: gen = rel.to() if rel.weight() > wgt else gen
#        if gen: vrs['idx_gen'] = self.addGen(gen) 
#
#    def addDHad(self, obj, pre="d0"):
#        vrs = {}
#        trks = []
#        try:
#            jets = tes[recJB.Output]
#            nInBest = 0
#            bestJet = -1
#            for idx, jet in enumerate(jets):
#                jetTrkKeys = [ self.key(dau) for dau in jet.daughters() ]
#                nIn=0
#                for dau in obj.daughters():
#                    key = self.key(dau)
#                    #if key in self.saved['trk']:
#                    #    trks.append(self.saved['trk'][key])
#                    #else :
#                    #    trks.append(self.addTrk(dau))
#                    if key in jetTrkKeys:
#                        nIn+=1
#                if nIn>nInBest:
#                    nInBest=nIn
#                    bestJet=idx
#            
#            for dau in obj.daughters():
#                trks.append(self.addTrk(dau))
#            pvr = self.pvrTool.relatedPV(obj, 'Rec/Vertex/Primary')
#            self.fillPvr(pvr, vrs)
#            self.fillDst(obj, pvr, 'ip', vrs)
#            self.fillDst(obj.endVertex(), pvr, 'fd', vrs)
#            self.fillLifetime(obj, pvr, vrs)
#            self.fillMom(obj.momentum(), vrs)
#            self.fillPos(obj.endVertex(), vrs)
#            self.fillVtx(obj.vertex(), vrs)
#            vrs['m'] = obj.momentum().M()
#            vrs['idx_jet'] = bestJet
#            vrs['ntrk_jet'] = nInBest
#            for idx, trk in enumerate(trks):
#                vrs['idx_trk%i' % idx] = trk
#
#            self.fill(pre, vrs = vrs)
#        except:
#            pass
#
#    def addGen(self, obj, jet = -1, pre = 'gen', par = None):
#        key = self.key(obj)
#        if key in self.saved[pre]: return self.saved[pre][key]
#        parent = obj.mother()
#        res = None
#        if par and parent.particleID().pid()!=par.particleID().pid(): #if they don't match we have a resonance
#            res = parent
#            parent = par
#        parKey = -1
#        parIdx = -1
#        fromSig=0
#        if obj.fromSignal(): fromSig = 1
#        vrs = {}
#        idx = len(self.saved[pre])
#        self.fillPid(obj.particleID(), vrs)
#        self.fillMom(obj.momentum(), vrs)
#        self.fillPos(obj.originVertex(), vrs)
#        self.fillPvr(obj.primaryVertex(), vrs)
#        vrs['idx_jet'] = jet
#        vrs['from_sig'] = fromSig
#        if res:
#            vrs['res_pid'] = res.particleID().pid()
#        if parent:
#            parKey = self.key(parent)
#            if parKey in self.saved[pre]: parIdx = self.saved[pre][parKey]
#            vrs['idx_prnt'] = parIdx
#            vrs['prnt_pid'] = parent.particleID().pid()
#        self.saved[pre][key] = idx
#        self.fill(pre, vrs = vrs)
#        pid = obj.particleID()
#        if pid.isHadron() and (pid.hasCharm() or pid.hasBottom()):
#            if pid.abspid() in self.Ds:
#                for part in self.finalChildren(obj)[0]:
#                    self.addGen(part,par=obj)
#            else:
#                for part in self.children(obj):
#                    self.addGen(part)
#        return idx
#    def addPvr(self, obj, pre = 'pvr'):
#        key = self.key(obj)
#        if key in self.saved[pre]: return self.saved[pre][key]
#        vrs = {}
#        idx = len(self.saved[pre])
#        self.fillPos(obj, vrs)
#        self.fillCov(obj, vrs)
#        self.saved[pre][key] = idx
#        self.fill(pre, vrs = vrs)
#        return idx
#    def addSvr(self, obj, pre = 'svr'):
#        vrs = {}
#        pvr = self.pvrTool.relatedPV(obj, 'Rec/Vertex/Primary')
#        self.fillMom(obj.momentum(), vrs)
#        self.fillPos(obj.endVertex(), vrs)
#        self.fillCov(obj.endVertex(), vrs)
#        self.fillPvr(pvr, vrs)
#        self.fillDst(obj.endVertex(), pvr, 'fd', vrs)
#        trks = []
#        for dtr in obj.daughters():
#            if not dtr.proto() or not dtr.proto().track(): continue
#            trks += [[self.addTrk(dtr), dtr.proto().track()]]
#            vrs['idx_trk%i' % (len(trks) - 1)] = trks[-1][0]
#        self.fill(pre, vrs = vrs)
#    def addTags(self, obj, jet = -1, pre = 'svr'):
#        tags = STD.map('string', 'double')()
#        if not self.tagTool.calculateJetProperty(obj, tags): return
#        ntag = int(tags['Tag'])
#        for itag in range(0, ntag):
#            vrs = {}
#            vrs['idx_pvr'] = self.addPvr(self.tes['Rec/Vertex/Primary']
#                                         [int(tags['Tag%i_idx_pvr' % itag])])
#            vrs['idx_jet'] = jet
#            ntrk = int(tags['Tag%i_nTrk' % itag])
#            for itrk in range(0, ntrk): vrs['idx_trk%i' % itrk] = self.addTrk(
#                self.tes['Phys/StdAllNoPIDsPions/Particles']
#                [int(tags['Tag%i_idx_trk%i' % (itag, itrk)])]);
#            for vr in ['x', 'y', 'z', 'px', 'py', 'pz', 'e']:
#                vrs[vr] = tags['Tag%i_%s' % (itag, vr)]
#            vrs['m']  = tags['Tag%i_m' % itag]
#            vrs['m_cor']  = tags['Tag%i_mCor' % itag]
#            vrs['m_cor_err']  = tags['Tag%i_mCorErr' % itag]
#            vrs['m_cor_err_full']  = tags['Tag%i_mCorErrFull' % itag]
#            vrs['pt']  = tags['Tag%i_pt' % itag]
#            vrs['fd_min'] = tags['Tag%i_fdrMin' % itag]
#            vrs['fd_chi2']  = tags['Tag%i_fdChi2' % itag]
#            vrs['chi2']  = tags['Tag%i_chi2' % itag]
#            vrs['ip_chi2_sum']  = tags['Tag%i_ipChi2Sum' % itag]
#            vrs['abs_q_sum']  = tags['Tag%i_absQSum' % itag]
#            vrs['tau']  = tags['Tag%i_tau' % itag]
#            vrs['ntrk']  = tags['Tag%i_nTrk' % itag]
#            vrs['ntrk_jet']  = tags['Tag%i_nTrkJet' % itag]
#            vrs['jet_dr']  = tags['Tag%i_drSvrJet' % itag]
#            vrs['jet_pt']  = tags['Tag%i_ptSvrJet' % itag]
#            vrs['pass']  = tags['Tag%i_pass' % itag]
#            vrs['bdt0']  = tags['Tag%i_bdt0' % itag]
#            vrs['bdt1']  = tags['Tag%i_bdt1' % itag]
#            self.fill(pre, vrs = vrs)
#    def addJet(self, obj, pre = 'jet'):
#        vrs = {}
#        idx = self.ntuple['jet_idx_pvr'].size();
#        pvr = self.pvrTool.relatedPV(obj, 'Rec/Vertex/Primary')
#        self.fillMom(obj.momentum(), vrs)
#        self.fillPvr(pvr, vrs)
#        trks = []
#        nneu=0
#        for dtr in obj.daughters():
#            try:
#                #TODO honestly no idea what's going on here
#                # if we add recSVs and recMus to the main sequence then obj.daughters contains Particles
#                # if we don't, it contains smart poniters to Particles
#                # try to treat them as pointers and if that fails assume they're particles
#                dtr = dtr.target()
#            except:
#                pass
#            if not dtr.proto() or not dtr.proto().track():
#                self.addNeu(dtr, idx)
#                nneu+=1
#            else:
#                trks += [[self.addTrk(dtr, idx), dtr.proto().track()]]
#        vrs['ntrk'] = len(trks)
#        vrs['nneu'] = nneu
#        self.addTags(obj, idx)
#        self.fill(pre, vrs = vrs)
#    def addNeu(self, obj, jet = -1, pre = 'neu'):
#        vrs = {}
#        self.fillMom(obj.momentum(), vrs)
#        self.fillPid(obj.particleID(), vrs)
#        self.fillGen(obj, vrs)
#        vrs['idx_jet'] = jet
#        self.fill(pre, vrs = vrs)
#    def addTrk(self, obj, jet = -1, pre = 'trk'):
#        key = self.key(obj)
#        if key in self.saved[pre]: return self.saved[pre][key]
#        vrs = {}
#        idx = len(self.saved[pre])
#        pvr = self.pvrTool.relatedPV(obj, 'Rec/Vertex/Primary')
#        self.fillMom(obj.momentum(), vrs)
#        self.fillPid(obj.particleID(), vrs)
#        self.fillPro(obj.proto(), vrs)
#        self.fillDst(obj, pvr, 'ip', vrs)
#        self.fillTrk(obj.proto().track(), obj.particleID(), vrs)
#        self.fillPvr(pvr, vrs)
#        self.fillGen(obj, vrs)
#        vrs['idx_jet'] = jet
#        self.saved[pre][key] = idx
#        self.fill(pre, vrs = vrs)
#        return idx

# GaudiPython configuration.
gaudi = GaudiPython.AppMgr()
tes   = gaudi.evtsvc()

# Run.
import sys, ROOT
from math import floor
evtmax = -1
#try: evtmax = int(sys.argv[1])
#except: evtmax = float('inf')
evtnum = 0
ntuple = Ntuple('output.root', tes, gaudi.toolsvc(), gaudi.detSvc(), recJB.Output, recSVs.outputLocation(), recMus.algorithm().Output)
while evtmax < 0 or evtnum < evtmax:
    gaudi.run(1)
    if not bool(tes['/Event']): break
    evtnum += 1
    ntuple.clear()

    # Fill event info.
    try: ntuple.ntuple['evt_pvr_n'][0] = len(tes['Rec/Vertex/Primary'])
    except: continue
    try: ntuple.ntuple['evt_trk_n'][0] = len(tes['Phys/StdAllNoPIDsPions/Particles'])
    except: continue

    # Fill generator level info.
    fill = False;
    gens = tes['MC/Particles']
    try:
        ntuple.addGen(gens[0])
        ntuple.addGen(gens[1])
    except: pass
    try:
        for gen in gens:
            pid = gen.particleID()
            if pid.isHadron() and (pid.hasCharm() or pid.hasBottom()):
                ntuple.addGen(gen); fill = True
    except: pass
    try:
        jets = tes[genJB.Output]
        for jet in jets: ntuple.addGen(jet); fill = True
    except: pass

    # Fill reconstructed.
    try:
        jets = tes[recJB.Output]
        for jet in jets:
            ntuple.addJet(jet); fill = True;
    except: pass

    # fill other tracks
    try:
        for trk in tes['Phys/StdAllNoPIDsPions/Particles']:
            ntuple.addTrk(trk);
    except: pass

    # fill D's
    try:
        d0s = tes[recD0.algorithm().Output]
        for d0 in d0s:
            ntuple.addDHad(d0,"d0")
        dps = tes[recDp.algorithm().Output]
        for dp in dps:
            ntuple.addDHad(dp,"dp")
        dss = tes[recDs.algorithm().Output]
        for ds in dss:
            ntuple.addDHad(ds,"ds")
        lcs = tes[recLc.algorithm().Output]
        for lc in lcs:
            ntuple.addDHad(lc,"lc")
        d0s = tes[recD02K3pi.algorithm().Output]
        for d0 in d0s:
            ntuple.addDHad(d0,"k3pi")
    except: pass

    # Fill the ntuple.
    if fill: ntuple.fill();
ntuple.close()
