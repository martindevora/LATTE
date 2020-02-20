# LATTE

Written by Nora L. Eisner

email: *nora.eisner@new.ox.ac.uk*


### THE CODE

--------

*The aim of this code is to provide a series of diagnostic tests which are used in order to determine the nature of events found in *TESS* lightcurves.*


--------
--------
### Installation

You can download the code directly from github (https://github.com/noraeisner/LATTE). Alternatively you can install LATTE using pip (https://pypi.org/project/tessLATTE/) via your command line with:

			pip install tessLATTE      

In order for LATTE to work you will need to have the right versions of certain modules installed, so downloading it in a virtual environemt. **Note: ensure that the matplotlib version that you are using is v3.2.0rc1 (pip install matplotlib==3.2.0rc1).**

The first time that the program is run you will be prompted to enter a path to a file on your computer where all the output data will be stored (this path can be changed later using --new-path). The first time that the code is run it will also have to download the text data files from MAST (this only has to run once). This may take a couple of minutes so be patient. 


### How to run it? 

LATTE is simply run through the command line with:

			python3 -m LATTE        

This will open up a box for you that prompts you to enter a TIC ID and indicate whether you would like to extract the information from the 2-minute cadence ('Standard mode') or 30-minute candence Full Frame Image (FFI) data ('FFI mode')

Once a TIC ID has been entered, the program will tell you in what sectors that target has been observed. If you want to look at all of the sectors, either enter them or simply press enter with nothing in the box. Alternatively, enter the sectors that you are interested in and enter them separated by commas. Remember that LATTE will have to download all the data for each sector so you might not always want to look at all of the sectors. 

TESS data is released periodically approximately once a month. When there is a new data release run the program with:

			python3 -m LATTE --new-data

which will automatically download the files that you need to access the new TESS data. 

**Normal Mode**

The '*normal mode*' looks at the short-cadence *TESS* data which has already been detrended and extracted by the SPOC pipeline. Optimal aperture lightcurve extraction aperture sizes have therefore already been identified and do not need to be selected manually.


**FFI Mode**

In *FFI mode* the data is downloaded using TESScut and the data detrended using PCA, a moving average filter and k-sigma clipping. Unlike the *TESS* 2-minute cadence targets, the FFIs do not come with a pre-chosen optimal aperture. By default, the user is given the option to manually select the pixels within each aperture for a 'large' and a 'small' aperture. This GUI opens automatically and the two apertures are selected by clicking on the desired pixels in the interface. The two (large and small aperture) lightcurves are simultaneously displayed. When the FFI mode is run with the command '--auto', the aperture size is chosen manually using a threshold flux value centred at the midpoint of the postage stamp.

### Transit time selection

Once you have identified the TIC ID, the observational sectors and the aperture sizes (*FFI mode* only), you will see a screen that has the full lighcurve as well as a zoom in of the lightcurve. The solid red line across the full lightcurve lets you know where on the lighcurve you are zooming in on. Click on the top (full) or bottom (zoomed in) plots to change the location of the zoom in until the red vertical line is centred on the mid-point of a transit-event. When you are happy with the location press the 'Add Time' button below the plots in order to record this time (in TBJD) . You can delete wrongly entered times with the 'Delete time'. The saved times will be shown on the screen. The position of the red line can also be changed by dragging the teal coloured 'Transit' slider with your mouse. The y-scale of the plots can be changed with the grey coloured slider.

Additional options are displayed to the left of the plots.

Binning Factor: 
- change the binning of the top plot (only available in the normal and not FFI mode)

Settings:

- Simple: only run the most basica diagnostic tests (not suing TPF). This is for a very quick analysis. 
- Hide Plots: Don't display the plots after they are made (will still store them). This speeds up the code.
- North: Align all the images due North (this slows down the code).
- BLS: Run a Box-Least-Squares algorithm that searches for periodic signals in the lightcurve. 
- Save: Save all the images (default this is already checked)
- Report: Generate a pdf file at the end of the code to summaise the findings (default this is already checked).

Finally, there is an optional box to enter a 'Memorable name' for the candidate. This name is used to store the data at the end in order to make identifying certain targets easier.


Once all the options have been chosen and the transit times stored (you have to enter at least one transit time), press the orange 'Done' button to continue.

The code will then generate download and process all of the data. Note that all the data is downloaded but not stored. The more sectors you analyse in one go the longer the code will take to run.


### Output


**Figures:**

- Full lightcurve with the times of the momentum dumps marked. 

- Background flux around the times of the marked transit event(s).

- Centroid positions around the time of the marked transit event(s).

- The lightcurve around the time of the marked event(s) extracted in two different aperture sizes (in 'normal' mode: TESS pipeline aperture and an aperture that is ~ 40 % smaller)

- The outlines of the two used apertues. 

- The average flux in and out of the marked event(s) and the differences between the two.

- The average flux of the target pixel file with the locations of nearby stars (magnitude < 15) indicated (GAIA DR2 queried).

- The lightcurves of the 5 closest stars that were also observed by *TESS* (TP files).

- A lightcurve around the time of the marked event(s) extracted for every pixel in the target pixel file.

- (optional) Two simple BLS plots. The second with the highest detected signal-to-noise transits from the initial run removed.
- (in progress, will be available in next release of LATTE) Modelling of the signal using a Bayesian approach with an MCMC sampling. This makes use of the Pyaneti code (Barragan et al. 2017). 

**FFI Mode**

- The FFI mode currently does not plot the nearby stars lightcurves (will be implemented soon).
- Saves the extracted apertures used
- Saves the corrected and the uncorrected lightcurves to verify that the detrending is workign correctly - there's are nt stored in the DV reports. 


**Tables:**

- Stellar parameters summarized, as well as information to whether the target has been flagged as a TCE or a TOI. The table links to the relevant reports (if applicable) as well as to the exofop page on the star.
- (optional) Summary of the BLS results. 
- (optional) Fitting parameters with uncertainties from the modelling. 


### Arguments

NOTE: all of these arguments (except new-path, auto and targetlist) can be changed as option in the GUI. They are arguments in case the same options wish to be run multiple times and the user therfore wishes to identify them in the command line when the program is executed.


!!!!!!  **--new-data**  The code requires multiple text files to be stored on your computer in order to run - these are downloaded automatically from the MAST server. The first time the proghram is run, and any time that there is new data available, add **--new-data** to the command line when running the program. The code checks what data has already been downloaded and doesn't re-download anything that already exists.

**--tic** You can skip the box to enter the tic ID by entering it in the command line with e.g. --tic=55525572. 

**--sector** You can skip entering the sectors by entering them in the command line with e.g. --sector=2,5. You will need to know in what sectors this target was observed.

**--targetlist***=path/to/the/csv/input/file* instead of entering the information manually everytime, you can provide LATTE with an input file which lists all the TIC IDs and the times of the transit events. Look at the example file to see the required format of the information.

**--noshow** if you do not want the figures to pop up on your screen you can run the program with this command in the command line. The program will run significantly faster with this run. If this option is chosen the files are always saved. 

**--o** If the input target list option is chosen, the program will check whether each target has already been analysed, in which case it will skip this target. If you do not wish to skip targets that have already been assessed use this in order to specify the 'overwrite' option. When the program is run interactively (not with an input file) this option has no effect.

**--auto** When looking at the FFIs, the default option is that you choose both the large and small apertures interactivelty. In order for the system to choose them run the command with '--auto'. 

**--nickname** In order to keep track of all of the candidates, it can be useful to asign them a nickname. This can be entered here which will simply change the name of the folder at the end. 

**--FFI** If you want to look at a FFI write '--FFI' in the command line. 

**--north** If you want all the images to be oriented due north (this is not the default as it takes longer to run)

**--new-path** If you want to define a new path to store the data.










