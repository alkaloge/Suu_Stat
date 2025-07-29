
year="Run2"
text2workspace.py ../datacards_recoSuu_mass0_JpTGt300/${year}/3000/combined.txt.cmb  -m 3000 -o CR_${year}_3000.root --channel-masks


maskedChannelsSR=",mask_suu_2016APV_muo_SR=1,mask_suu_2016_muo_SR=1,mask_suu_2017_muo_SR=1,mask_suu_2018_muo_SR=1,mask_suu_2016APV_ele_SR=1,mask_suu_2016_ele_SR=1,mask_suu_2017_ele_SR=1,mask_suu_2018_ele_SR=1"

maskedChannelsCR=",mask_suu_2016APV_muo_CR=1,mask_suu_2016_muo_CR=1,mask_suu_2017_muo_CR=1,mask_suu_2018_muo_CR=1,mask_suu_2016APV_ele_CR=1,mask_suu_2016_ele_CR=1,mask_suu_2017_ele_CR=1,mask_suu_2018_ele_CR=1"

maskedChannels=${maskedChannelsSR}

# Asimov data, CR, --expectSignal=0 (B-only)


combineTool.py -M Impacts -d CR_${year}_3000.root -m 3000 --doInitialFit -n CR_${year}_nodata_nosignal --rMin -150.0 --rMax 150.0 --setParameters r=0${maskedChannels} --freezeParameters r --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminPreScan --cminPreFit 1 --robustFit 1 --cminDefaultMinimizerTolerance 0.1

combineTool.py -M Impacts -d CR_${year}_3000.root -m 3000 --doFit -n CR_${year}_nodata_nosignal --rMin -150.0 --rMax 150.0 --freezeParameters r --expectSignal 0 --cminDefaultMinimizerStrategy 1 --cminPreScan --cminPreFit 1 --setParameters r=0${maskedChannels} -t -1 --job-mode condor --sub-opts='+JobFlavour="microcentury"' --task-name Impact_CR_${year}_nodata_nosignal  --robustFit 1 --cminDefaultMinimizerTolerance 0.1


