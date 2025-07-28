rm -fr UL2018
rm -fr UL2017
rm -fr UL2016
rm -fr UL2016APV
rm -fr ULRun2

cp -r /uscms_data/d3/alkaloge/MetStudies/nAOD/Suu/new/SuuToTU_TToBLNu_SUNY/datacards/hirak/UL2018 .
cp -r /uscms_data/d3/alkaloge/MetStudies/nAOD/Suu/new/SuuToTU_TToBLNu_SUNY/datacards/hirak/UL2017 .

echo copying UL2016
mkdir UL2016
cp -r /uscms_data/d3/alkaloge/MetStudies/nAOD/Suu/new/SuuToTU_TToBLNu_SUNY/datacards/hirak/ULpostVFP_2016/* UL2016/.

echo copying UL2016APV
mkdir UL2016APV
cp -r /uscms_data/d3/alkaloge/MetStudies/nAOD/Suu/new/SuuToTU_TToBLNu_SUNY/datacards/hirak/ULpreVFP_2016/* UL2016APV/.

mv UL2016/test_postVFP_2016_recoSuu_mass0_JetpTgt300.root UL2016/test_2016_recoSuu_mass0_JetpTgt300.root
mv UL2016APV/test_preVFP_2016_recoSuu_mass0_JetpTgt300.root UL2016APV/test_2016APV_recoSuu_mass0_JetpTgt300.root


mkdir ULRun2
echo merging 2016 pre+post -- not really used anywhere --

hadd -f ULRun2/test_2016APV_recoSuu_mass0_JetpTgt300.root UL2018/test*root UL2017/test*root UL2016/test*root UL2016APV/test*root
