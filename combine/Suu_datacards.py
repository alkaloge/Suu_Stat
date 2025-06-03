#!/usr/bin/env python

import argparse
import os
import ROOT
import CombineHarvester.CombineTools.ch as ch

# Define categories with regions (ele_SR, ele_CR, muo_SR, muo_CR)
cats = [
    (1, "ele"),
    (2, "muo"),
]
cats_ele = [
    (1, "ele"),
]
cats_muo = [
    (2, "muo"),
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
    'JER': 'CMS_res_j'
}

def DecorrelateUncertainties(cb, year):
    for unc in expUnc:
        cb.cp().RenameSystematic(cb,unc,expUnc[unc]+"_"+year)

parser = argparse.ArgumentParser(description="Datacards producer")
parser.add_argument("-year", "--year", required=True, choices=["preVFP_2016","2016", "2017", "2018"])
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
#cb.AddObservations([""], ["suu"], [year], ["muo"], cats)

# 2. Add processes
signals = [f"signal_{mass}"]
btag_label="0btag"
backgrounds = ["WJets", "TT", "ST", "DY", "VV", "QCD"]
top=["TT"]
qcd=["QCD"]
mc_bkgd = backgrounds
#cb.AddProcesses([mass], ["suu"], [year], [cats], signals, cats, True)
#cb.AddProcesses([""], ["suu"], [year], [cats], backgrounds, cats, False)

#    return self.__AddProcesses__(mass, analysis, era, channel, procs, bin, signal)
#cb.AddObservations([""], ["azh"], [year], [btag_label], cats)
cb.AddProcesses([""], ["suu"], [year],  [""], signals, cats, True)
cb.AddProcesses([""], ["suu"], [year],  [""], backgrounds, cats, False)

mc_processes = signals + backgrounds
# 3. Add systematics
# Luminosity
if year == '2016':
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi_2016', 'lnN', ch.SystMap()(1.010))
elif year == '2017':
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi_2017', 'lnN', ch.SystMap()(1.020))
elif year == '2018':
    cb.cp().process(mc_processes).AddSyst(cb, 'CMS_lumi_2018', 'lnN', ch.SystMap()(1.015))

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

#Jet/MET systematics
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_scale_j_"+year, "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_res_j_"+year, "shape", ch.SystMap()(1.0))

cb.cp().process(signals + backgrounds).AddSyst(cb, "pdf", "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_l1_ecal_prefiring", "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_pileup", "shape", ch.SystMap()(1.0))
cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_btag_hf", "shape", ch.SystMap()(1.0))
#cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_btag_lf", "shape", ch.SystMap()(1.0)) ## NEED TO FIX
#cb.cp().process(signals + backgrounds).AddSyst(cb, "QCDscale", "shape", ch.SystMap()(1.0))
#cb.cp().process(top).AddSyst(cb, "top_pt_reweighting_SR", "shape", ch.SystMap()(1.0))
cb.cp().process(qcd).AddSyst(cb, "QCD_scale", "lnN", ch.SystMap()(1.5))
#cb.cp().process(top).AddSyst(cb, "top_pt_reweighting", "shape", ch.SystMap()(1.0))


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
        'btag_corr': 'CMS_btag_hf',
        'btag_uncorr': 'CMS_btag_hf',
        'mistag_corr': 'CMS_btag_lf',
        'mistag_uncorr': 'CMS_btag_lf'

'''


#cb.cp().process(signals + backgrounds).AddSyst(cb, "CMS_scale_met_unclustered", "shape", ch.SystMap()(1.0))

# 4. Extract shapes using the correct naming scheme
input_file = "UL"+year+"/step1_"+year+"_"+var+"_JetpTgt"+cut+".root"
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
    cb.AddDatacardLineAtEnd("* autoMCStats 0")

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


