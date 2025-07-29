


combineTool.py -M Impacts -m 3000 -d CR_${year}_3000.root -o impacts_CR_${year}_data_nosignal_3000.json -n CR_${year}_data_nosignal
plotImpacts.py -i impacts_CR_${year}_data_nosignal_3000.json -o impacts_CR_${year}_data_nosignal;


