# SUU Analysis Instructions

## First step  - create root files from coffea (use your usual jyputer setup, nothing fancy here)

The main script is this one 

`ExtractHists_forDataCards.ipynb`


The `def hnameRecommended` handles the systematics names according to the official CAT recommendations

The `def createDatacard` is the main function that writes the coffea to root TH1 objects. It has been observed, that in some cases, uproot does not handle properly coffea files and that results into empty or missing TH1 histograms for specific systematics for example. This is been taken care of and we now have all TH1 present in the output.

To produce the corresponding year root file, load the first two blocks (common) and then the desired 2018/2017/year 


## 2nd step - Rebin and fix negative bins 

From bash line execute
 
`  . step1.sh`

This will process the created root  templates and will produce the rebinned TH1 histograms organized in a separate directory per channel. At this point, you can also decide the binning -look at L16 for example 

This now will create a new root file like 
`
UL2018//step1_2018_recoSuu_mass0_JetpTgt300_rebinned.root
`

The next step is to smooth the systematics 


## 3nd step  - Smooth templates (this can be skipped, but for consistency we use it)

The next script `MakeRootTemplates.ipynb` takes as input the output of the 2nd step and smooths out the systematic templates. Plots of before/after are also presented on the fly. If everything works as expected, you should have now in the ULX directory three files like 
`
ls UL2018
step1_2018_recoSuu_mass0_JetpTgt300.root  step1_2018_recoSuu_mass0_JetpTgt300_rebinned.root  step1_2018_recoSuu_mass0_JetpTgt300_rebinned_smooth.root
`

Now we are ready to make the datacards


## Combine/Statistical treatment part
From the bash command line just execute 

`. makeCards.sh`

This will open each _rebinned_smooth root file and will create a datacards for each mass point. You should see messages like 
```
Datacards successfully created in: datacards_recoSuu_mass0_JpTGt300/2018/3000
Datacards successfully created in: datacards_recoSuu_mass0_JpTGt300/2018/4000
Datacards successfully created in: datacards_recoSuu_mass0_JpTGt300/2018/5000
Datacards successfully created in: datacards_recoSuu_mass0_JpTGt300/2018/6000
Datacards successfully created in: datacards_recoSuu_mass0_JpTGt300/2018/7000
Datacards successfully created in: datacards_recoSuu_mass0_JpTGt300/2018/8000
Datacards successfully created in: datacards_recoSuu_mass0_JpTGt300/2018/9000
...
```
Several options can be defined (like the output dir) from the main script `Suu_datacards.py`. Default output dir is `datacards_recoSuu_mass0_JpTGt300`

Next, create the workspaces - the wrapper to be executed is this one 

`. makeWorkspaces.sh`

Once executed, it will create the workspace from combine, but also the combined Run2 one. This may take a while as it is executed locally.

Typical output
```
. makeWorkspaces.sh

executing command
cd /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_13_0_10/src/Suu_Stat/combine//jobs ; combineTool.py -M T2W -o "ws.root" --PO '"map=^.*/signal$:r_signal[0,-40,40]"'  -i /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_13_0_10/src/Suu_Stat/combine//datacards_recoSuu_mass0_JpTGt300/2016/3000/ -m 3000 --channel-masks ; cd -
>> Directory /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_13_0_10/src/Suu_Stat/combine//datacards_recoSuu_mass0_JpTGt300/2016/3000/, looking for datacards
>> pushd /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_13_0_10/src/Suu_Stat/combine//datacards_recoSuu_mass0_JpTGt300/2016/3000/; combineCards.py suu_2016_ele_CR=suu_2016_ele_CR.txt suu_2016_ele_SR=suu_2016_ele_SR.txt suu_2016_muo_CR=suu_2016_muo_CR.txt suu_2016_muo_SR=suu_2016_muo_SR.txt &> combined.txt.cmb; text2workspace.py -o ws.root --PO "map=^.*/signal$:r_signal[0,-40,40]" --channel-masks -m 3000 combined.txt.cmb; popd
/uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_13_0_10/src/Suu_Stat/combine/datacards_recoSuu_mass0_JpTGt300/2016/3000 /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_13_0_10/src/Suu_Stat/combine/jobs
Channel suu_2016_ele_CR will use autoMCStats with settings: event-threshold=10, include-signal=0, hist-mode=1
```

Next  we are ready to run combine to get GoF, limits, impacts - It is better to run the next steps from lxplus, as lpc condor does not have the local disks mounted/visible from condor machines

## Asimov data, CR, --expectSignal=0 (B-only)

```
cd Impacts_Asimov_CR_Bonly
. runImpacts.sh
# script collect.sh to collect once jobs are done, make the json and copy the pdf to your output dir
```

## Real data, CR, --expectSignal=0 (B-only)

```
cd Impacts_Real_CR_Bonly
. runImpacts.sh
# script collect.sh to collect once jobs are done, make the json and copy the pdf to your output dir
```
## GoF test
```
cd GoF_Asimov_CR_Bonly
. GoF_Asimov_CR_Bonly.sh
# collect.sh to collect the root and make the output
```


