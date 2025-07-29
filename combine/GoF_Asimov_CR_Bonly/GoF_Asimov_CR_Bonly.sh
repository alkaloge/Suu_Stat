year="Run2"
#if Run2 --> card = combined.txt.cmb
text2workspace.py ../datacards_recoSuu_mass0_JpTGt300/${year}/3000/combined.txt.cmb  -m 3000 -o input_${year}_3000.root --channel-masks

maskedChannelsSR=",mask_suu_2016APV_muo_SR=1,mask_suu_2016_muo_SR=1,mask_suu_2017_muo_SR=1,mask_suu_2018_muo_SR=1,mask_suu_2016APV_ele_SR=1,mask_suu_2016_ele_SR=1,mask_suu_2017_ele_SR=1,mask_suu_2018_ele_SR=1"

maskedChannelsCR=",mask_suu_2016APV_muo_CR=1,mask_suu_2016_muo_CR=1,mask_suu_2017_muo_CR=1,mask_suu_2018_muo_CR=1,mask_suu_2016APV_ele_CR=1,mask_suu_2016_ele_CR=1,mask_suu_2017_ele_CR=1,mask_suu_2018_ele_CR=1"

maskedChannels=${maskedChannelsSR}


combine -M FitDiagnostics -d input_${year}_3000.root -n _fit_CRonly_result --saveShapes  --saveWithUncertainties --rMin -150.0 --rMax 150.0 -m 3000 --robustFit 1 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 0  --freezeParameters r --setParameters r=0${maskedChannelsSR} --cminPreScan --cminPreFit 1


combine -M GoodnessOfFit -d input_${year}_3000.root --algo saturated -m 3000 -n .goodnessOfFit_data_saturated --freezeParameters r --setParameters r=0${maskedChannelsSR} --cminPreScan --cminPreFit 1


#wget https://raw.githubusercontent.com/lcorcodilos/2DAlphabet/bstar/importPars.py

python3 importPars.py ../datacards_recoSuu_mass0_JpTGt300/${year}/3000/combined.txt.cmb fitDiagnostics_fit_CRonly_result.root

combine -M GenerateOnly -d morphedWorkspace.root --toysFrequentist --bypassFrequentistFit --expectSignal 0 -t 1000 --saveToys -m 3000



for i in {1..50}
do
    random=$RANDOM
    echo random seed $random


combineTool.py -M GoodnessOfFit -d input_${year}_3000.root \
        --algo=saturated \
        --toysFrequentist \
        --bypassFrequentistFit \
        --freezeParameters r \
        -m 3000 \
        -t 20 \
        -n .goodnessOfFit_toys_saturated_${random} \
        --setParameters r=0${maskedChannelsSR} \
        --cminPreScan \
        --cminPreFit 1 \
        --job-mode condor \
        --sub-opts='+JobFlavour="testmatch"' \
        --task-name GoodnessOfFit_CRonly_${random} \
        --cminDefaultMinimizerTolerance 0.1 \
        -s ${random}  # This sets the random seed


done


