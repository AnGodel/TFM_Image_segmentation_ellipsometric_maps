
cd %userprofile%
cd Anaconda3\Scripts
conda init cmd.exe
CALL conda activate ellimaps
cd %~dp0%


streamlit run streamlit_ElliMaps_segmentation.py