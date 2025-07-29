var="jet0_pT"
var=${1}
var="recoSuu_mass0"


var="recoSuu_mass0"

masses=(3000 4000 5000 6000 7000 8000 9000)
#masses=(3000)
years=("2018" "2017" "2016" "2016APV")

for year in "${years[@]}"; do
  for mass in "${masses[@]}"; do
     python3 Suu_datacards.py \
      --year ${year} \
      --mass ${mass} 
  done
done


