#Check the permissions on ORCA, and VMD
cwd=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

VMD_PATH=$cwd/VMD_1.9.4a55-x86_64-Rev11.app
ORCA_PATH=$cwd/ORCA/Orca421/orca
ORCA_NDOINT=$cwd/ORCA/Orca421/orca_ndoint
ORCA_SCF=$cwd/ORCA/Orca421/orca_scf
ORCA_UTIL=$cwd/ORCA/Orca421/orca_util

#grant access
chmod +x $VMD_PATH
chmod +x $ORCA_PATH
chmod +x $ORCA_NDOINT
chmod +x $ORCA_SCF
chmod +x $ORCA_UTIL

xattr -dr com.apple.quarantine $ORCA_PATH
xattr -dr com.apple.quarantine $ORCA_NDOINT
xattr -dr com.apple.quarantine $ORCA_SCF
xattr -dr com.apple.quarantine $ORCA_UTIL
