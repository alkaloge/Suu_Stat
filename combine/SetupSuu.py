#!/usr/bin/env python
import ROOT
import os
from array import array
import argparse
ROOT.gROOT.SetBatch(True)

# Dynamic rebinning configuration
bins = []
for ib in range(0, 5001, 200):
    bins.append(ib)
bins.append(6000)  # Add the final edge
rebin = array('d', bins)


parser = argparse.ArgumentParser(description="Root files producer")
parser.add_argument("-year", "--year", required=True, choices=["2016", "2017", "2018", "preVFP_2016", "postVFP_2016"])
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
    input_filename = folder+"/"+"test_"+year+"_"+Var+"_JetpTgt"+cut+".root"
    output_filename = folder+"/"+"step1_"+year+"_"+Var+"_JetpTgt"+cut+".root"
    
    input_file = ROOT.TFile.Open(input_filename, "READ")
    output_file = ROOT.TFile(output_filename, "RECREATE")
    print ('will handle ', input_filename, ' saving to ', output_filename)
    # Create channel directories
    for channel in ["ele", "muo"]:
        output_file.mkdir(channel)
    
    for key in input_file.GetListOfKeys():
        original_name = key.GetName().split(';')[0]
        parts = original_name.split('_')
        
        if 'data' in original_name : print ('found it', original_name)
        if len(parts) < 3:
            print ('less ', parts)
            continue

        channel = parts[0]
        if channel not in ["ele", "muo"]:
            continue
            
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
            continue
            
        processed_hist = process_histogram(hist, rebin)
        if not processed_hist:
            continue
        
        # Write to appropriate channel directory
        output_file.cd(channel)
        #print ('new name', new_name)
        new_name = new_name.replace("muo_","")
        new_name = new_name.replace("ele_","")
        #new_name = new_name.replace("data_obs","data")
        new_name = new_name.replace("SR_","")
        processed_hist.Write(new_name)
    
    output_file.Close()
    input_file.Close()

if __name__ == "__main__":
    main()


