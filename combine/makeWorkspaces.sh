var="jet0_pT"

var="recoSuu_mass0"

samples=("2016" "2016APV" "2017" "2018")
#samples=("2018")
masses=(3000 4000 5000 6000 7000 8000 9000)
#masses=(3000)

for sample in "${samples[@]}"; do
  for mass in "${masses[@]}"; do
    python3 CreateWorkspaces.py \
      --mass ${mass} \
      --var ${var} 
  done
done

