
var="jet0_pT"

var=${1}

python3 CreateWorkspaces.py --mass 3000 --var ${var}
python3 CreateWorkspaces.py --mass 4000 --var ${var}
python3 CreateWorkspaces.py --mass 5000 --var ${var}
python3 CreateWorkspaces.py --mass 6000 --var ${var}
python3 CreateWorkspaces.py --mass 7000 --var ${var}
python3 CreateWorkspaces.py --mass 8000 --var ${var}
python3 CreateWorkspaces.py --mass 9000 --var ${var}

