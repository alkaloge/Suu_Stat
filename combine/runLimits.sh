pt=${1}
pt="300"
var="recoSuu_mass0"
var="jet0_pT"
var=${1}

python3 RunLimits.py --sample 2016 --mass 3000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2016 --mass 4000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2016 --mass 5000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2016 --mass 6000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2016 --mass 7000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2016 --mass 8000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2016 --mass 9000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}

python3 RunLimits.py --sample 2018 --mass 3000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2018 --mass 4000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2018 --mass 5000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2018 --mass 6000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2018 --mass 7000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2018 --mass 8000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2018 --mass 9000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}

python3 RunLimits.py --sample 2017 --mass 3000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2017 --mass 4000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2017 --mass 5000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2017 --mass 6000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2017 --mass 7000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2017 --mass 8000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample 2017 --mass 9000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}

python3 RunLimits.py --sample Run2 --mass 3000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample Run2 --mass 4000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample Run2 --mass 5000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample Run2 --mass 6000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample Run2 --mass 7000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample Run2 --mass 8000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
python3 RunLimits.py --sample Run2 --mass 9000 --outdir limits_${var}_JpTGt${pt} --folder datacards_${var}_JpTGt${pt}
