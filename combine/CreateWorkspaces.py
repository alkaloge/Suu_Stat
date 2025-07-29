#!/usr/bin/env python3

import Suu_Stat.combine.utils as utils
import os

def MakeCommandWorkspace(**kwargs):
    sample = kwargs.get('sample','Run2')
    mass = kwargs.get('mass','3000')
    batch = kwargs.get('batch',False)
    var = kwargs.get('var','recoSuu_mass0')
    folder = kwargs.get('folder','datacards_'+var+'JpTGt300')

    # 2D workspace
    command = 'cd %s ; '%(utils.JobFolder)
    #command += 'combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO \'"map=^.*/bbA$:r_bbA[0,-40,40]"\' --PO \'"map=^.*/ggA$:r_ggA[0,-40,40]"\' -i %s/%s/%s/%s/ -m %s '%(utils.BaseFolder,folder,sample,mass,mass)
    command += 'combineTool.py -M T2W -o "ws.root" --PO \'"map=^.*/signal$:r_signal[0,-40,40]"\'  -i %s/%s/%s/%s/ -m %s --channel-masks'%(utils.BaseFolder,folder,sample,mass,mass)
    if batch:
        taskname='workspace_%s_%s'%(sample,mass)
        command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s '%(taskname)
    command += ' ; cd -'

    return command

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-mass','--mass',dest='mass',required=True) 
    parser.add_argument('-var','--var',dest='var',required=False, default = 'recoSuu_mass0') 
    parser.add_argument('-folder','--folder',dest='folder',default='datacards_JpTGt300')
    parser.add_argument('-batch','--batch',dest='batch',action='store_true')
    args = parser.parse_args()

    folder = args.folder
    var = args.var
    folder = folder.replace('cards_', 'cards_'+var+"_")
    masses = [] 
    if args.mass=='all':
        masses = utils.azh_masses
    else:
        masses.append(args.mass)

    samples = ['2016','2017','2018','Run2','et','mt','tt','btag','0btag']
    samples = ['2016','2017','2018','Run2','ele', 'muo']
    samples = ['2018','2017', 'Run2','ele', 'muo']
    samples = ['preVFP_2016','2016', '2018','2017', 'Run2']
    samples = ['2016', '2016APV', '2017','2018', 'Run2']
    #samples = ['2016', '2016APV', '2017','2018' ]
    #samples = ['2018']


    batch=False
    if args.batch:
        batch=True

    if not os.path.isdir(folder):
        print ('Folder %s does not exist'%(folder))
        print ('Run first datacard production with script make_datacards.py or CreateCards.py')
        exit(1)

    if not os.path.isdir(utils.JobFolder):
        command_mkdir='mkdir %s'%(utils.JobFolder)
        os.system(command_mkdir)

    for sample in samples:
        for mSuu in masses:
            print('')
            folder_mass = folder+'/'+sample+'/'+mSuu
            if not os.path.isdir(folder_mass):
                print('Warning : Folder %s does not exist'%(folder_mass))
                print ('Run first datacard production with script make_datacards.py or CreateCards.py')
                print('Skipping mSuu=%s for %s'%(mSuu,sample))
                print('')
                continue

            ws_file=folder_mass+'/ws.root'
            if os.path.isfile(ws_file):
                rm_command = 'rm '+ws_file
                #            print('removing old file %s'%(ws_file))
                #            print(rm_command)
                os.system(rm_command)

            datacard_file=folder_mass+'/combined.txt.cmb'
            if os.path.isfile(datacard_file):
                rm_command = 'rm '+datacard_file
                #            print('removing old file %s '%(datacard_file))
                #            print(rm_command)
                os.system(rm_command)

            #        print("Creating workspace in folder %s/%s/%s"%(utils.DatacardsFolder,sample,mSuu))
            
            command=MakeCommandWorkspace(sample=sample,folder=folder,mass=mSuu,batch=batch)
            if batch: 
                print('submitting job with command ')
            else:
                print('executing command ')
            print(command)
            os.system(command)
