# QuantumDock
Code for the QuantumDock publication, compatible with a zsh shell. This python wrapper can be utilized to generate stable dimers between two molecules of ones choice. Use of this package requires Orca is installed. For quick use it should be installed in the QuantumDock directory with the path QuantumDock/ORCA/Orca421/. The only reuired files in this directory are "orca_ndoint" "orca_scf" "orca_util" and "orca" from the orca software package. ORCA downloads can be found here https://orcaforum.kofo.mpg.de/app.php/dlext/?cat=10. The VMD software package should also be downloaded to the QuantumDock directory under the name "VMD_1.9.4a55-x86_64-Rev11". The specific version of VMD needed for various machines can be found here https://www.ks.uiuc.edu/Research/vmd/alpha. Renaiming the file may be nessecary after download to avoid errors.

The exact versions used for this publication can be found under this publicly availible dropbox https://www.dropbox.com/scl/fo/kq35tlwc9qdjorpsm1z82/h?dl=0&rlkey=6in0iddgeb0o4ljyur5otkux6

New conformations can be made by following editing the Pose_Gen.sh file and modifying the variables "Molecule_1_name" and "Molecule_2_name" to and of the Targets or Monomers in the Molecular_Database path.

NOTE: The following packages must be installed (you can use pip, homebrew, or your package manager of choice)
1. obabel
2. matplotlib
3. os
4. sys
5. re
6. numpy
7. subprocess
8. scipy
9. operator
