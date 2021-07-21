cd %userprofile%
cd Anaconda3\Scripts
conda init cmd.exe
CALL conda activate ellimaps
cd %~dp0%
conda env create --file ellimaps_env.yml
cd nanofilm_package_installer
pip install nanofilm-ep4-0.7.10.tar.gz
cd ..
set /p DUMMY=Hit ENTER