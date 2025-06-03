import numpy as np
import matplotlib.pyplot as plt

def plot_limits(Era="2018",    # dataset : 2016, 2017, 2018, Run2
                Sample="2018", # options : 2016, 2017, 2018, Run2, et, mt, tt, btag, 0btag
                Process="signal", # process : ggA, bbA
                basefolder="limits", # input folder (output of macro RunLimits.py)
                postfix="asymptotic",       # postfix in the name of output png file
                YMin=0.0,   # lower boundary of Y axis 
                YMax=0.015,   # upper boundary of Y axis
                XMin=2900.,  # lower boundary of X axis
                XMax=9100., # upper boundary of X axis
                logy=False,  # log scale of Y axis
                logx=False,   # log scale of X axis
                xLeg=0.65,  # x coordinate of the legend box
                yLeg=0.6,   # y coordinate of the legend box
                BR_AZh=False, # produce results in terms of sigma x BR(A->Zh)
                pb=True,     # limits are shown in picobarn (otherwise in fb)
                blindData=True): # blinding observed limit

    folder = basefolder
    limitLabel = "Frequentist CLs"
    if "limits_asymptotic" in folder:
        limitLabel = "Asymptotic"
    
    scaleBR = 1.0
    if BR_AZh:
        scaleBR = 1.0 / (0.1 * 0.062)
    
    unit = "fb"
    if pb:
        unit = "pb"

    massesD = [3000, 4000, 5000, 6000, 7000, 8000, 9000] 
    masses = ["3000", "4000", "5000", "6000", "7000", "8000", "9000"]

    massTheory = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    xsecTheory = [150.1, 32.02, 6.798, 1.311, 0.2148, 0.02774, 0.002491, 0.0001249]

    lumiLabel = {
        "Run2": "Run2, 138 fb^{-1}",
        "2018": "2018, 59.8 fb^{-1}",
        "2017": "2017, 41.5 fb^{-1}",
        "2016": "2016, 36.3 fb^{-1}"
    }

    lumi_13TeV = lumiLabel[Era]

    # Initialize arrays
    nPoints = 20
    mA = np.zeros(nPoints)      
    minus2R = np.zeros(nPoints) 
    minus1R = np.zeros(nPoints) 
    medianR = np.zeros(nPoints) 
    plus1R = np.zeros(nPoints)  
    plus2R = np.zeros(nPoints)  
    obsR = np.zeros(nPoints)    

    obs = np.zeros(nPoints)
    minus2 = np.zeros(nPoints)
    minus1 = np.zeros(nPoints)
    median = np.zeros(nPoints)
    plus1 = np.zeros(nPoints)
    plus2 = np.zeros(nPoints)

    LIMIT = 0.0
    counter = 0

    for mass in masses:
        fileName = f"{folder}/higgsCombine.signal_{Sample}_{Process}.AsymptoticLimits.mH{mass}.root"
        print(fileName)

        # Assuming a function to read the ROOT file and extract the limit values
        # This part needs to be implemented based on the specific library used for ROOT file handling in Python
        # For example, using uproot or similar library

        # Example of reading the file (pseudo-code):
        # with uproot.open(fileName) as file:
        #     tree = file["limit"]
        #     LIMIT = tree["limit"].array()[0]  # Replace with actual extraction logic

        MH = float(mass)
        
        # Simulating the extraction of limits for demonstration purposes
        # Replace these with actual values from the ROOT file
        LIMIT_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]  # Placeholder for actual limit values
        for i in range(6):
            LIMIT = LIMIT_values[i] * scaleBR
            if i == 0:
                minus2R[counter] = LIMIT
            elif i == 1:
                minus1R[counter] = LIMIT
            elif i == 2:
                medianR[counter] = LIMIT
            elif i == 3:
                plus1R[counter] = LIMIT
            elif i == 4:
                plus2R[counter] = LIMIT
            elif i == 5:
                obsR[counter] = LIMIT
                if blindData:
                    obsR[counter] = medianR[counter]

        mA[counter] = MH
        counter += 1

    print("\n          ", limitLabel, " (", Process)

