#!/usr/bin/env python
import ROOT
import os
from array import array
import argparse
ROOT.gROOT.SetBatch(True)
import numpy as np

# Dynamic rebinning configuration
bins = []
for ib in range(0, 5001, 200):

    bins.append(ib)
bins.append(6000)  # Add the final edge
rebin = array('d', bins)

#v16_oldbin
rebin = np.array([0,400] + list(np.linspace(600, 4000, num=18))
            +[4500, 5500, 6500, 9000])

#current one, merge last three bins
#rebin = np.array([0,400] + list(np.linspace(600, 4000, num=18))
#            +[4500, 9000])

print ('bins....', rebin)

parser = argparse.ArgumentParser(description="Root files producer")
parser.add_argument("-year", "--year", required=True, choices=["2016", "2017", "2018", "2016APV"])
parser.add_argument("-cut", "--cut", default="500", help="JetpT Cut", required = False)
parser.add_argument("-var", "--var", default="recoSuu_mass0", help="Variable to be used to extract signal", required = False)
args = parser.parse_args()

year = args.year
cut = args.cut
Var=args.var
folder="UL"+year+"/"


def process_histogram(hist, rebin_array):
    """Rebin histogram including overflow handling, negative bin cleaning, and sum preservation."""
    try:
        # Rebin while preserving original axis range
        rebinned = hist.Rebin(len(rebin_array)-1, hist.GetName() + "_rebinned", rebin_array)
        
        # Merge overflow to last bin (critical for sum conservation)
        n_bins = rebinned.GetNbinsX()
        overflow = rebinned.GetBinContent(n_bins + 1)
        overflow_err = rebinned.GetBinError(n_bins + 1)
        
        if overflow != 0:
            new_val = rebinned.GetBinContent(n_bins) + overflow
            new_err = (rebinned.GetBinError(n_bins)**2 + overflow_err**2)**0.5
            rebinned.SetBinContent(n_bins, new_val)
            rebinned.SetBinError(n_bins, new_err)
            rebinned.SetBinContent(n_bins + 1, 0)
            rebinned.SetBinError(n_bins + 1, 0)

        # Clean negative bins (after overflow handling)
        for i in range(1, rebinned.GetNbinsX()+1):
            if rebinned.GetBinContent(i) < 0:
                rebinned.SetBinContent(i, 0)
                rebinned.SetBinError(i, 0)
        
        # Preserve the exact sum of weights
        original_sum = hist.GetSumOfWeights()
        new_sum = rebinned.GetSumOfWeights()
        if new_sum != 0:
            scale_factor = original_sum / new_sum
            rebinned.Scale(scale_factor)
                
        return rebinned
    except Exception as e:
        print(f"Error processing {hist.GetName()}: {str(e)}")
        return None
def main():
    input_filename = folder+"/"+"step1_"+year+"_"+Var+"_JetpTgt"+cut+"_smooth.root"
    output_filename =  input_filename.replace(".root", "_smooth.root")
    
    print ("will process, ", input_filename, "and will write", output_filename)
    input_file = ROOT.TFile.Open(input_filename, "READ")
    output_file = ROOT.TFile(output_filename, "RECREATE")
    print ('will handle ', input_filename, ' saving to ', output_filename)
    # Create channel directories
    for channel in ["ele_SR", "muo_SR", "ele_CR", "muo_CR"]:
        output_file.mkdir(channel)
    
    for channel in ["ele_SR", "muo_SR", "ele_CR", "muo_CR"]:
        for key in input_file.GetListOfKeys():
            original_name = key.GetName().split(';')[0]
            parts = original_name.split('_')
            
            if 'data' in original_name : print ('found it', original_name)
            if len(parts) < 3:
                print ('less ', parts)
                #continue

            output_file.cd(channel)
            #channel = parts[0]
            #if channel not in ["ele", "muo"]:
            #    continue
                
            # Process signal name
            modified_parts = list(parts)
            if len(parts) >= 3 and parts[2] == "MSuu-3TeV":
                modified_parts[2] = "signal_3000"
            if len(parts) >= 3 and parts[2] == "MSuu-4TeV":
                modified_parts[2] = "signal_4000"
            if len(parts) >= 3 and parts[2] == "MSuu-5TeV":
                modified_parts[2] = "signal_5000"
            if len(parts) >= 3 and parts[2] == "MSuu-6TeV":
                modified_parts[2] = "signal_6000"
            if len(parts) >= 3 and parts[2] == "MSuu-7TeV":
                modified_parts[2] = "signal_7000"
            if len(parts) >= 3 and parts[2] == "MSuu-8TeV":
                modified_parts[2] = "signal_8000"
            if len(parts) >= 3 and parts[2] == "MSuu-9TeV":
                modified_parts[2] = "signal_9000"
            if len(parts) >= 3 and parts[2] == "MSuu-10TeV":
                modified_parts[2] = "signal_10000"
            new_name = "_".join(modified_parts)
            # Get and process hist
            hist = input_file.Get(original_name)

            if not hist:
                print ('something went wrong with this', original_name)
                replacename=original_name
                if 'Up' not in original_name and 'Down' not in original_name and 'ele_CR_QCD' in original_name:
                    hname='ele_CR_QCD_topPtWeight_CRUp'
                    hist = input_file.Get(hname)
                    hist.SetName(original_name)
                    print('problem with nominal histo...check!')
                else : 
                    if 'Up' in original_name :
                        ('problem with Up variation', original_name)
                        replacename = original_name.replace("Up", "Down")
                    if 'Down' in original_name :
                        ('problem with Down variation', original_name)
                        replacename = original_name.replace("Down", "Up")
                        

                    hist = input_file.Get(replacename)

                print ('trying once more with', original_name, replacename, hist.GetSumOfWeights())
                #continue
                
            processed_hist = process_histogram(hist, rebin)
            processed_hist = process_histogram(hist, rebin)
            if not processed_hist:
                print('failed to process_histogram ie rebining...', hist.GetName())
                continue
            
            # Write to appropriate channel directory
            #print ('new name', new_name)
            if channel not in new_name : continue
            new_name = new_name.replace(channel+"_","")
            #new_name = new_name.replace("ele_","")
            #new_name = new_name.replace("data_obs","data")
            new_name = new_name.replace("topPtWeight_SR","top_pt_reweighting")
            new_name = new_name.replace("topPtWeight_CR","top_pt_reweighting")
            new_name = new_name.replace("topPtWeightDown","top_pt_reweightingDown")
            new_name = new_name.replace("topPtWeightUp","top_pt_reweightingUp")
            #new_name = new_name.replace("SR_","")
            #new_name = new_name.replace("CR_","")
            new_name = new_name.replace("_2018_2018","_2018")
            new_name = new_name.replace("_2017_2017","_2017")
            new_name = new_name.replace("_2016_2016","_2016")
            new_name = new_name.replace("_preVFP_2016_preVFP_2016","_2016APV")
            new_name = new_name.replace("_preVFP_2016_preVFP_2016","_2016APV")
            new_name = new_name.replace("_preVFP_2016","_2016APV")
            if 'QCDscale_' in new_name :
                new_name = new_name.replace("_SRUp", "Up")
                new_name = new_name.replace("_CRUp", "Up")
                new_name = new_name.replace("_SRDown", "Down")
                new_name = new_name.replace("_CRDown", "Down")

            if '2017' in year and 'ele' in channel and 'data' not in new_name: 
                #print( 'we have ele 2017', year, channel, ' will also scale it by', float(36.7/41.5))
                processed_hist.Scale(float(36.7/41.5))
            if 'signal' in new_name and 'pdf' in new_name : new_name = new_name.replace('pdf', 'pdf_signal')
            #print ('we have a looser!!!', processed_hist.GetBinContent(processed_hist.GetNbinsX()))
            #if processed_hist.GetBinContent(processed_hist.GetNbinsX()) == 1e-06 : print ('we have a looser!!!', new_name, processed_hist.GetNbinsX())
            '''
            for i in range (1, processed_hist.GetNbinsX()+1) :
                if processed_hist.GetBinContent(i) < 1e-05 : print ('we have a looser!!!', new_name, i, processed_hist.GetBinContent(i), processed_hist.GetBinError(i))
                processed_hist.SetBinContent(i,0.0) 
                processed_hist.SetBinError(i,0.0) 
            '''
            processed_hist.Write(new_name)
    
    output_file.Close()
    input_file.Close()

if __name__ == "__main__":
    main()


