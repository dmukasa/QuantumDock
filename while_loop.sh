while [ "${h_bonds}" == "0" ]
    do
    #delete all files in the current directory
    rm *

    #Make a new conformer
    python3 ${cwd}/Make_new_confomer.py ${Molecule_1_PATH} ${Molecule_2_PATH} ${OUT_PATH}

    #Make new hbonds.dat
    cd ${OUT_PATH}
    if [[ ${Molecule_2_name} == "2AM" ]]
        then
            export Confomer_name
            ${cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_2AM}
        elif [[ ${Molecule_2_name} == "APB" ]]
        then
            export Confomer_name
            ${cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_APB}
        elif [ ${Molecule_2_name} == "4VP" ] | [ ${Molecule_2_name} == "AVB" ] | [ ${Molecule_2_name} == "PAA" ]
        then
            export Confomer_name
            ${cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_Strict}
        else #use general
            export Confomer_name
            ${cwd}/VMD_1.9.4a55-x86_64-Rev11.app/Contents/MacOS/startup.command -dispdev text -e ${check_h_bond_General}
    fi
    #save the number of hydrogen bonds as h_bonds
    while IFS= read -r line; do
        h_bonds=${line: -1}
    done < ${OUT_PATH}/hbonds.dat
    echo "THIS IS A TEST: " ${file}
    echo "|"
    echo "|"
    echo "|"
    echo "|"
    echo "V"
    echo "THE NEW NUMBER OF H-BONDS IS:" ${h_bonds}
done

#Make .inp file
FILENAME=${Confomer_name}
WD=${OUT_PATH}
functional="PM3"
python3 ${cwd}/Make_Semi_inp.py ${FILENAME} ${functional} ${WD}

#run orca
cd ${OUT_PATH}
#PATH/TO/ORCA ${OUT_PATH}/${FILENAME}.inp > ${OUT_PATH}/${FILENAME}.out
#/Users/danielmukasa/ORCA/Orca421/orca ${OUT_PATH}/${FILENAME}.inp > ${OUT_PATH}/${FILENAME}.out
/Users/danielmukasa/Desktop/Pub_Repo/ORCA/Orca421/orca ${OUT_PATH}/${FILENAME}.inp > ${OUT_PATH}/${FILENAME}.out
