

year="Run2"
text2workspace.py ../datacards_recoSuu_mass0_JpTGt300/${year}/3000/combined.txt.cmb  -m 3000 -o CR_${year}_3000.root --channel-masks


maskedChannelsSR=",mask_suu_2016APV_muo_SR=1,mask_suu_2016_muo_SR=1,mask_suu_2017_muo_SR=1,mask_suu_2018_muo_SR=1,mask_suu_2016APV_ele_SR=1,mask_suu_2016_ele_SR=1,mask_suu_2017_ele_SR=1,mask_suu_2018_ele_SR=1"
maskedChannelsCR=",mask_suu_2016APV_muo_CR=1,mask_suu_2016_muo_CR=1,mask_suu_2017_muo_CR=1,mask_suu_2018_muo_CR=1,mask_suu_2016APV_ele_CR=1,mask_suu_2016_ele_CR=1,mask_suu_2017_ele_CR=1,mask_suu_2018_ele_CR=1"

maskedChannels=${maskedChannelsSR}

# Asimov data, CR, --expectSignal=0 (B-only)


combineTool.py -M Impacts -d CR_${year}_3000.root -m 3000 --doInitialFit -n CR_${year}_data_nosignal --rMin -20.0 --rMax 20.0 --setParameters r=0 --freezeParameters r --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminPreScan --cminPreFit 1  --cminDefaultMinimizerTolerance 0.1  --setParameters mask_suu_2016APV_muo_SR=1,mask_suu_2016_muo_SR=1,mask_suu_2017_muo_SR=1,mask_suu_2018_muo_SR=1,mask_suu_2016APV_ele_SR=1,mask_suu_2016_ele_SR=1,mask_suu_2017_ele_SR=1,mask_suu_2018_ele_SR=1


combineTool.py -M Impacts -d CR_${year}_3000.root -m 3000 --doFit -n CR_${year}_data_nosignal --rMin -20.0 --rMax 20.0 --setParameters r=0 --freezeParameters r --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminPreScan --cminPreFit 1 --setParameters mask_suu_2016APV_muo_SR=1,mask_suu_2016_muo_SR=1,mask_suu_2017_muo_SR=1,mask_suu_2018_muo_SR=1,mask_suu_2016APV_ele_SR=1,mask_suu_2016_ele_SR=1,mask_suu_2017_ele_SR=1,mask_suu_2018_ele_SR=1 -w w --snapshotName "MultiDimFit" -t -1 --job-mode condor --sub-opts='+JobFlavour="microcentury"' --task-name Impact_CR_data_nosignal


