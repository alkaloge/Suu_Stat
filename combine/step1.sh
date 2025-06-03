# create root files with proper dir

var=${1}

cut="300"
#python3 SetupSuu.py --year 2017 --cut 500
#python3 SetupSuu.py --year 2018 --cut 500
python3 SetupSuu.py --year 2018 --cut ${cut} --var ${var}
python3 SetupSuu.py --year 2017 --cut ${cut} --var ${var}
python3 SetupSuu.py --year postVFP_2016 --cut ${cut} --var ${var}
python3 SetupSuu.py --year preVFP_2016 --cut ${cut} --var ${var}


mkdir UL2016
hadd  -f UL2016/step1_2016_${var}_JetpTgt${cut}.root ULpostVFP_2016/step1_postVFP_2016_${var}_JetpTgt${cut}.root ULpreVFP_2016/step1_preVFP_2016_${var}_JetpTgt${cut}.root

