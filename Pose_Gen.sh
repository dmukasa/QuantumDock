#!/usr/bin/python3

###########################################################VARIABLES################################################################
Molecule_1_name="PHE"
Molecule_2_name="PYR"
############################################################IMPLIED VARIABLES#######################################################
cwd=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
Confomer_name=${Molecule_1_name}_${Molecule_2_name}
Molecule_1_PATH=${cwd}"/Molecular_Database/Targets/"${Molecule_1_name}/${Molecule_1_name}.pdb
if [[ ${Molecule_1_name} == "TRP" && ${Molecule_2_name} == "MAA" ]]
    then
        Molecule_2_PATH=${cwd}"/Molecular_Database/tmp/"${Molecule_2_name}/${Molecule_2_name}.pdb
    else
        Molecule_2_PATH=${cwd}"/Molecular_Database/Monomers/"${Molecule_2_name}/${Molecule_2_name}.pdb
fi
mkdir ${cwd}/${Molecule_1_name}-${Molecule_2_name}
MIPNET_PATH=${cwd}"/${Molecule_1_name}-${Molecule_2_name}"
check_h_bond_2AM=${cwd}"/h_bonds_2AM.vmd"
check_h_bond_APB=${cwd}"/h_bonds_APB.vmd"
check_h_bond_General=${cwd}"/h_bonds_General.vmd"
check_h_bond_Strict=${cwd}"/h_bonds_Strict.vmd"
####################################################################################################################################
#####Timing######
#################
start=`date +%s`
#################

#Make all the directories
cd $MIPNET_PATH
pwd

for i in {1..100}
    do
    mkdir ${Confomer_name}_${i}
done

#Make confomer files and run a PM3 geometric optimization as a first guess 
#Use vmd to confirm the conformations have h bonds in them 
for file in *
    do
    #Make the confomer file
    OUT_PATH=${MIPNET_PATH}/${file}
    python3 ${cwd}/Make_new_confomer.py ${Molecule_1_PATH} ${Molecule_2_PATH} ${OUT_PATH}

    #Make the hbonds.dat counting the number of h bonds
    cd ${OUT_PATH}
    if [[ ${Molecule_2_name} == "2AM" ]]
        then
            export Confomer_name
            ${cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_2AM}
        elif [[ ${Molecule_2_name} == "APB" ]]
        then
            export Confomer_name
            $cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_TRP_MAA}
        elif [ ${Molecule_2_name} == "4VP" ] | [ ${Molecule_2_name} == "AVB" ] | [ ${Molecule_2_name} == "PAA" ]
        then
            export Confomer_name
            ${cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_Strict}
        elif [[ ${Molecule_2_name} == "DVP" ]]
        then
            :
        else #use general
            export Confomer_name
            ${cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_General}
    fi
    
    echo "THIS IS A TEST: " ${file} 
    echo "|"
    echo "|"
    echo "|"
    echo "|"
    echo "|"
    echo "V"
    #save the number of hydrogen bonds as h_bonds
    while IFS= read -r line; do
        h_bonds=${line: -1}
    done < ${OUT_PATH}/hbonds.dat
    echo "THE NUMBER OF H-BONDS IS:" ${h_bonds}
    
    #If h_bonds==0 or 1 or 2 then delete the contents of the current directory and start the loop again
    export h_bonds Molecule_1_PATH Molecule_2_PATH OUT_PATH Molecule_1_name Molecule_2_name Confomer_name check_h_bond_2AM check_h_bond_APB check_h_bond_Strict check_h_bond_General FILENAME cwd
    sh ${cwd}/while_loop.sh &
done    

#Wait for all the conformations to be generated prior to proceeding
wait

#Find the 20 most stable conformations (20 lowest energies) Delete all the rest of the files
cd $MIPNET_PATH

python3 /Volumes/MIP_DESIGN/Pose_Generation/Pose_Gen_Analysis.py ${MIPNET_PATH} ${Molecule_1_name} ${Molecule_2_name}

cd $MIPNET_PATH

#Rename the files in Complex to proper names
cd Complex

for file in *
    do
    mv "$file" "${file%????}"
done



#Delete everything but the resulting XYZ files
for file in *
    do
    cd ${file}
    find . -type f -not -name ${Molecule_1_name}_${Molecule_2_name}.xyz -print0 | xargs -0 rm --
    cd ..
done

cd $MIPNET_PATH

#Make a directory Archive and save the other files here
mkdir Archive

for file in *
    do
    if [ "${file}" != "Complex" ] && [ "${file}" != "Archive" ]
        then
        mv ${file} Archive
    fi
done

cd Archive

#Delete everything but the resulting XYZ files
for file in *
    do
    cd ${file}
    find . -type f -not -name ${Molecule_1_name}_${Molecule_2_name}.xyz -print0 | xargs -0 rm --
    cd ..
done



#Make a trj.xyz from the files in complex: go into Complex first and make a trj.xyz for the top 20 configarations
cd ${MIPNET_PATH}/Complex

#loop through files
for file in *
    do
    cd ${MIPNET_PATH}/Complex/${file}
    cat ${Molecule_1_name}_${Molecule_2_name}".xyz" >> "${MIPNET_PATH}/Complex_trj.xyz"
done


#DELETE ARCHIVE UNLESS MAKING FIGURE 2B,C
cd $MIPNET_PATH
rm -r Archive


#Make a directory for the Monomer
cd $MIPNET_PATH
mkdir Monomer

cd $MIPNET_PATH/Monomer
mkdir ${Molecule_2_name}

cd $MIPNET_PATH/Monomer/${Molecule_2_name}
cp /Volumes/MIP_DESIGN/Pose_Generation/Molecular_Database/Monomers/${Molecule_2_name}/${Molecule_2_name}.pdb .
#convert the pdb to xyz
obabel ${Molecule_2_name}.pdb -O ${Molecule_2_name}.xyz
rm ${Molecule_2_name}.pdb


#And repeat for the Target
cd $MIPNET_PATH
mkdir Target

cd $MIPNET_PATH/Target
mkdir ${Molecule_1_name}

cd $MIPNET_PATH/Target/${Molecule_1_name}
cp /Volumes/MIP_DESIGN/Pose_Generation/Molecular_Database/Targets/${Molecule_1_name}/${Molecule_1_name}.pdb .
#convert the pdb to xyz
obabel ${Molecule_1_name}.pdb -O ${Molecule_1_name}.xyz
rm ${Molecule_1_name}.pdb

#################
end=`date +%s`
runtime=$((end-start))
echo "Elapsed Time: ${runtime} seconds"
#################
