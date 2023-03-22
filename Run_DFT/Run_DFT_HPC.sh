####################SET VARIABLES PRIOR TO RUNNING CODE####################
MIPNET_PATH="/groups/GaoGroup/dmukasa/Functional_Test/TYR-VAL-ACA"
functional="B3LYP_D3BJ"
basis="6-31++G**"
###########################################################################

#Start the Complex calculations
#Loop through all folders in MIPNET_PATH
cd $MIPNET_PATH
for folder in *
do
    #Go into the complex folder
    cd $MIPNET_PATH/${folder}/Complex
 
    #Loop through all the complex folder and start the jobs
    for file in *
    do
        cd $MIPNET_PATH/${folder}/Complex/${file}
        for xyz in *
        do 
            FILENAME=${xyz%.xyz}
            WD=$(pwd)
            python /groups/GaoGroup/dmukasa/Functional_Test/Run_DFT/Make_inp.py ${FILENAME} ${functional} ${basis} ${WD}
            python /groups/GaoGroup/dmukasa/Functional_Test/Run_DFT/Make_sh.py ${FILENAME} ${functional} ${WD}
            sbatch ${FILENAME}.sh
        done  
    done
done
##########################################################################
#Now start the Monomer

cd ${MIPNET_PATH}
for folder in *
do
    cd ${MIPNET_PATH}/${folder}/Monomer

    for file in *
    do
      	cd ${MIPNET_PATH}/${folder}/Monomer/${file}
        for xyz in *
        do
            FILENAME=${xyz%.xyz}
            WD=$(pwd)
            python /groups/GaoGroup/dmukasa/Functional_Test/Run_DFT/Make_inp.py ${FILENAME} ${functional} ${basis} ${WD}
            python /groups/GaoGroup/dmukasa/Functional_Test/Run_DFT/Make_sh.py ${FILENAME} ${functional} ${WD}
            sbatch ${FILENAME}.sh
        done
    done
done
##########################################################################
#Now start the Target

cd ${MIPNET_PATH}
for folder in *
do
    cd ${MIPNET_PATH}/${folder}/Target

    for file in *
    do
      	cd ${MIPNET_PATH}/${folder}/Target/${file}
        for xyz in *
        do
            FILENAME=${xyz%.xyz}
            WD=$(pwd)
            python /groups/GaoGroup/dmukasa/Functional_Test/Run_DFT/Make_inp.py ${FILENAME} ${functional} ${basis} ${WD}
            python /groups/GaoGroup/dmukasa/Functional_Test/Run_DFT/Make_sh.py ${FILENAME} ${functional} ${WD}
            sbatch ${FILENAME}.sh
        done
    done
done

