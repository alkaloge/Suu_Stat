


combineTool.py -M CollectGoodnessOfFit --input higgsCombine.goodnessOfFit_data_saturated.GoodnessOfFit.mH3000.root higgsCombine.goodnessOfFit_toys_saturated*.root -m 3000.0 -o gof_Suu3000_CR_t0.json

plotGof.py gof_Suu3000_CR_t0.json --statistic saturated --m 3000.0 --cms-sub "Preliminary" -o gof_Suu3000_CR_t0  --title-right="CR fit, B-only"

cp gof_Suu3000_CR_t0.png /eos/user/a/alkaloge/www/Suu/Results/gof_Suu3000_CR_t0.png
