#!/usr/bin/env python

import argparse
import os
import ROOT
import CombineHarvester.CombineTools.ch as ch

# Define categories with regions (ele_SR, ele_CR, muo_SR, muo_CR)
cats = [
    (1, "ele_SR"),
    (2, "ele_CR"),
    (3, "muo_SR"),
    (4, "muo_CR"),
]
cats_ele = [
    (1, "ele_SR"),
    (2, "ele_CR"),
]
cats_muo = [
    (1, "muo_SR"),
    (2, "muo_CR"),
]

# Systematic uncertainties (tau-related removed)
expUnc = {
    'unclMET': 'CMS_scale_met_unclustered',
    'efake': 'CMS_suu_efake',
    'mfake': 'CMS_suu_mfake',
    'eleES': 'CMS_scale_e',
    'muES': 'CMS_scale_m',
    'pileup': 'CMS_pileup',
    'l1prefire': 'CMS_l1prefire',
    'eleSmear': 'CMS_res_e',
    'JES': 'CMS_scale_j',
    'JER': 'CMS_res_j',
    'topPtWeight' : 'top_pt_reweighting'
}

def DecorrelateUncertainties(cb, year):
    for unc in expUnc:
        cb.cp().RenameSystematic(cb,unc,expUnc[unc]+"_"+year)

parser = argparse.ArgumentParser(description="Datacards producer")
parser.add_argument("-year", "--year", required=True, choices=["2016APV","2016", "2017", "2018", "Run2"])
parser.add_argument("-mass", "--mass", required=True, help="Signal mass (e.g., 3000)")
parser.add_argument("-folder", "--folder", default="datacards_JpTGt", help="Output folder", required = False)
parser.add_argument("-no_bbb", "--no_bbb", action="store_true", help="Disable bin-by-bin uncertainties")
parser.add_argument("-cat", "--cat", default="all", required=False, help="channels, ele or muo, all ")
parser.add_argument("-cut", "--cut", default="300", help="JetpT Cut", required = False)
parser.add_argument("-var", "--var", default="recoSuu_mass0", help="variable", required = False)
args = parser.parse_args()

year = args.year
mass = args.mass
cut = args.cut
var=args.var
folder = args.folder
folder = folder + cut
folder = folder.replace("datacards_", "datacards_"+var+"_")
auto_mc = not args.no_bbb
chn = args.cat
if chn == 'ele' : cats=cats_ele
if chn == 'muo' : cats=cats_muo
# Initialize CombineHarvester
cb = ch.CombineHarvester()


# ================== MAIN CONFIGURATION ==================
# 1. Add observations with dummy channel (real channel is in bin names)
cb.AddObservations([""], ["suu"], [year], [""], cats)


# 2. Add processes
signals = [f"signal_{mass}"]
btag_label="0btag"
backgrounds = ["WJets", "TT", "ST", "DY", "VV", "QCD"]
#backgrounds += ["CR_WJets", "CR_TT", "CR_ST", "CR_DY", "CR_VV", "CR_QCD"]
top=["TT"]
stop=["ST"]
qcd=["QCD"]
dy=["DY"]
vv=["VV"]
wjets=[""]
mc_bkgd = backgrounds

#    return self.__AddProcesses__(mass, analysis, era, channel, procs, bin, signal)
cb.AddProcesses([""], ["suu"], [year],  [""], signals, cats, True)
cb.AddProcesses([""], ["suu"], [year],  [""], backgrounds, cats, False)

mc_processes = signals + backgrounds
# 3. Add systematics
# Luminosity
if '2016' in year and 'APV' not in year:
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi_2016', 'lnN', ch.SystMap()(1.012))
if '2016APV' in year:
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi_2016APV', 'lnN', ch.SystMap()(1.012))
elif year == '2017':
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi_2017', 'lnN', ch.SystMap()(1.023))
elif year == '2018':
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi_2018', 'lnN', ch.SystMap()(1.025))

# Lepton systematics
#cb.cp().process(mc_processes).AddSyst(cb, "CMS_eff_e", "lnN", ch.SystMap()(1.03))
#cb.cp().process(mc_processes).AddSyst(cb, "CMS_eff_m", "lnN", ch.SystMap()(1.03))

# CMS electron trigger
# 1.5 uncertainty correlated across years
syst_map = ch.SystMap("bin_id")([0,1], 1.015)#([4, 5, 6], 1.0)

#cb.cp().signals().AddSyst(cb, "CMS_eff_e", "lnN", syst_map)
#cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_e", "lnN", syst_map)
#eletrig

# NAME HERE HAS TO CHANGE!!!! next round!
cb.cp().signals().AddSyst(cb, "CMS_eff_e_trigger", "shape", ch.SystMap()(1.0))
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_e_trigger", "shape", ch.SystMap()(1.0))

cb.cp().signals().AddSyst(cb, "CMS_eff_e_id", "shape", syst_map)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_e_id", "shape", syst_map)

cb.cp().signals().AddSyst(cb, "CMS_eff_e_reco", "shape", syst_map)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_e_reco", "shape", syst_map)


# CMS muon trigger
# 1.5% correlated across years
syst_map=None
syst_map = ch.SystMap("bin_id")([2,3], 1.015)#([1, 2, 3], 1.0)
#cb.cp().signals().AddSyst(cb, "CMS_eff_m", "lnN", syst_map)
#cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_m", "lnN", syst_map)

cb.cp().signals().AddSyst(cb, "CMS_eff_m_id", "lnN", syst_map)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_m_id", "lnN", syst_map)

cb.cp().signals().AddSyst(cb, "CMS_eff_m_reco", "lnN", syst_map)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_m_reco", "lnN", syst_map)

cb.cp().signals().AddSyst(cb, "CMS_eff_trigger_m", "lnN", syst_map)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_trigger_m", "lnN", syst_map)

cb.cp().process(signals ).AddSyst(cb, "pdf_signal", "shape", ch.SystMap()(1.0))
cb.cp().process(backgrounds).AddSyst(cb, "pdf", "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_l1_ecal_prefiring", "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_pileup", "shape", ch.SystMap()(1.0))

cb.cp().process(qcd).AddSyst(cb, "QCDscale_QCD", "shape", ch.SystMap()(1.))
cb.cp().process(top).AddSyst(cb, "QCDscale_TT", "shape", ch.SystMap()(1.))
cb.cp().process(stop).AddSyst(cb, "QCDscale_ST", "shape", ch.SystMap()(1.))
cb.cp().process(dy).AddSyst(cb, "QCDscale_DY", "shape", ch.SystMap()(1.))
cb.cp().process(wjets).AddSyst(cb, "QCDscale_WJets", "shape", ch.SystMap()(1.))
cb.cp().process(vv).AddSyst(cb, "QCDscale_VV", "shape", ch.SystMap()(1.))
cb.cp().process(top).AddSyst(cb, "top_pt_reweighting", "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_eff_b", "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_btag_light", "shape", ch.SystMap()(1.0))

if year == 'Run2' : 

    #Jet/MET systematics
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi', 'lnN', ch.SystMap()(1.016))
    #cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_scale_j", "shape", ch.SystMap()(1.0))
    #cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_res_j", "shape", ch.SystMap()(1.0))


if year != 'Run2' : 

    #Jet/MET systematics
    cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_scale_j_"+year, "shape", ch.SystMap()(1.0))
    cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_res_j_"+year, "shape", ch.SystMap()(1.0))

    cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_eff_b_"+year, "shape", ch.SystMap()(1.0))
    cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_btag_light_"+year, "shape", ch.SystMap()(1.0))

#cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_btag_lf", "shape", ch.SystMap()(1.0)) ## NEED TO FIX
#cb.cp().process(signals + backgrounds).AddSyst(cb, "QCDscale", "shape", ch.SystMap()(1.0))
#cb.cp().process(top).AddSyst(cb, "top_pt_reweighting_SR", "shape", ch.SystMap()(1.0))


'''
        'pu': 'CMS_pileup',
        'q2': 'QCDscale',
        'topPtWeight': 'top_pt_reweighting',
        'eleid': 'CMS_eff_e_id',
        'elereco': 'CMS_eff_e_reco',
        'eletrigHigh': 'CMS_eff_e_trigger_high',
        'eletrigLow': 'CMS_eff_e_trigger_low',
        'eletrigMed': 'CMS_eff_e_trigger_med',
        'muid': 'CMS_eff_m_id',
        'mureco': 'CMS_eff_m_reco',
        'mutrig': 'CMS_eff_m_trigger',
        'jer': 'CMS_res_j',
        'jes': 'CMS_scale_j',
        'puId': 'CMS_eff_j_PUJET_id',

        'btag_corr': 'CMS_eff_b',
        'btag_uncorr': 'CMS_eff_b_'+IOV,
        'mistag_corr': 'CMS_btag_light',
        'mistag_uncorr': 'CMS_btag_light_'+IOV

'''


#cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_scale_met_unclustered", "shape", ch.SystMap()(1.0))


rootext ="_rebinned_smooth.root"
# 4. Extract shapes using the correct naming scheme
input_file = "UL"+year+"/step1_"+year+"_"+var+"_JetpTgt"+cut+rootext

# Extract shapes for regular data observations
# For SR data
cb.cp().bin([""]).process(["data_obs"]).ExtractShapes(input_file, "$BIN/data_obs", "")

# Signals
cb.cp().signals().ExtractShapes(
    input_file,
    "$BIN/$PROCESS$MASS",
    "$BIN/$PROCESS$MASS_$SYSTEMATIC"
)
# Backgrounds
cb.cp().backgrounds().ExtractShapes(
    input_file,
    "$BIN/$PROCESS$MASS",
    "$BIN/$PROCESS$MASS_$SYSTEMATIC"
)

# 5. Add autoMCStats if enabled
if auto_mc:
    cb.AddDatacardLineAtEnd("* autoMCStats 10")

# 6. Create output directory and write cards
output_dir = os.path.join(folder, year, str(mass))
os.makedirs(output_dir, exist_ok=True)

#writer = ch.CardWriter(
#    "$TAG/$MASS.txt",
#    "$TAG/$MASS.root"
#)
#writer.SetVerbosity(1)
#writer.WriteCards(output_dir, cb)

writer = ch.CardWriter(
    "$TAG/$ANALYSIS_$ERA_$BIN.txt",
    #"$TAG/$ANALYSIS_$ERA_$CHANNEL_$BIN_$MASS.root",
    "$TAG/$ANALYSIS_$ERA_$BIN.root",
)

writer.WriteCards('%s/%s/%s/'%(folder,year,mass), cb)
writer.WriteCards('%s/Run2/%s/'%(folder,mass), cb)

print(f"Datacards successfully created in: {output_dir}")


