1. SYSTEM REQUIREMENTS
Python 3.7 with the following libraries: matplotlib, numpy, tkinter, os. The code can be run on any OS that supports Python 3 (e.g., Windows, MAC, LINUX; note: the code has been tested only on macOS Catalina and Windows 10). No non-standard hardware is required.

2. INSTALLATION GUIDE
Install Python 3 with Anaconda following standard procedures. Unzip “digitISA.zip” to a location of choice on your hard disk drive. The unzipped folder "digitISA" contains the main analysis software code called “getBursts_digitISA.py”, and 3 dependency files: “readPTU.py”, “burstLoc.py”, “leeFilter.py”. Note: For the code to work, the main analysis software code and the dependencies need to be saved within the same folder. Furthermore, a raw data demo file is provided called "25pM_MVSA_50pM_DNA_AttoBiotin_10mM_HEPES_150uW_150V_2000_300_70ulh_100_steps_5s_4th_electrolyte_16_760.15um_steps.ptu" which can be found in the "DEMO" folder.

3. DEMO
a. Instructions to run on data
For data analysis of the demo file, run the main software code file called “getBursts_digitISA.py” from the "digitISA" folder. A pop-up window will appear to select a .ptu file. Choose the demo .ptu file in the "DEMO" folder. Note: If the pop-up window does not appear, it might be in the background. Simply reduce the window size or minimize the window to display the directory file.

b. Expected output
Once the code is executed, the console in Python displays the number of molecules detected ("Number of bursts detected:"). The output value for the number of molecules of the demo .ptu file is 200. Additionally, a plot is generated which contains 4 subpanels. Top left panel: intensity versus time plot (detected bursts are highlighted with a red dot above the time trace). Top right corner: inter-photon time plot (photons that correspond to a fluorescence burst are highlighted in red). Bottom left and right panels: histograms of burst time duration and number of photons per burst, respectively.

c. Expected run time for demo on a "normal" desktop computer
The first time the .ptu file is selected it may take up to 10 s for the computer to read the .ptu file and provide the output values and plot the data. If the code is re-run, the run time reduces to less than one second. This is because upon re-running, the .out file, which is generated the first time the code is run, is directly used to analyse the data.

4. INSTRUCTIONS FOR USE
How to run the software on your data.
Adjustable input parameters for data analysis in the main software code file “getBursts_digitISA.py” are the Lee filter parameter (setLeeFilter), interphoton time threshold (threIT), the minimum number of photons per burst threshold (minPhs). Default values for the demo file are: setLeeFilter = 4, threIT = 0.1, minPhs = 7.