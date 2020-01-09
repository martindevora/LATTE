import os
import ast
import csv
import sys
import warnings
import matplotlib
import numpy as np
import pandas as pd
import tkinter as tk
from glob import glob

from os.path import exists
from tkinter import simpledialog
from argparse import ArgumentParser

#custom modules to import
from LATTE import LATTEbrew as brew 
from LATTE import LATTEutils as utils
#sys.tracebacklimit = 0
warnings.filterwarnings('ignore')

'''
NOTE: a warning message currently appears when the code is exited (i.e. at the end of the code). 
This is due to an error in the current verion of matplolib with the interactive widgets but has been adressed
in future releases of matplolib (see https://github.com/matplotlib/matplotlib/issues/13660)
The above link shows how to change the matplolib cbook __init__ file in order to make it disapear.

# REQUIRES MATPLOLIB 3.2 (there is a bug in 3.1 the current stable version - as of January 2020)). 
 --- pip install matplotlib==3.2.0rc1 (still in testing?)
'''

# -------------------- START ---------------------
# ------------------------------------------------

if __name__ == '__main__':
	ap = ArgumentParser(description='Lightcurve Analysis Tool for Transiting Exoplanets')
	ap.add_argument('--new-data', action='store_true')
	ap.add_argument('--tic', type=str, help='the target TIC id, if blank will be prompted to enter', default = 'no')
	ap.add_argument('--sector', type=str, help='the sector(s) to look at', default = 'no')
	ap.add_argument('--targetlist', type=str, help='the link to the target file list', default='no')
	ap.add_argument('--noshow', action='store_true', help='if you want to NOT show the plots write --noshow in the command line')
	ap.add_argument('--o', action='store_true', help='if you call this old files will be overwriten in the non-interactive version')
	ap.add_argument('--auto', action='store_false', help='automatic aperture selection')
	ap.add_argument('--nickname', type=str, help='give the target a memorable name', default='noname')
	ap.add_argument('--FFI', action='store_true', help='is this an FIIs?')
	ap.add_argument('--save', help='is this an FIIs?', default = True)
	ap.add_argument('--north', action='store_true', help='write "north" if you want all the images to be aligned North')
	ap.add_argument('--new-path', action = 'store_true', help ='enter to change the output path')

	args = ap.parse_args()

	# ------------------------------------------------
	# Check what the current path is - when the program is first downloaded the path is set to 'no/path/set/yet' and the user is automatically prompted to change'no/path/set/yet'
	


	def yes_or_no():
		'''
		Yes/No command line option to verify that the user really wants to change the output/input path
		'''
		print ('\n \n WARNING: if you have already downloded the input files (with --new-data) then these will remain in the location set by your previous path, so you will have to redowload the data (not recommended) or move the data to the new location set by this path. \n \n ')
	
		reply = str(input('Are you sure that you want to change the path?' + '(yes/no): '))
	
		if (reply == 'y') or (reply == 'yes') or (reply == 'yep') or (reply == 'yeah'):
			return True
	
		else: # if anything else is entered assume that this is a 'no' and continue with the old path
			return False	 
	
	if not os.path.exists("_config.txt"):
		indir = input("\n \n No output path has been set yet. \n \n Please enter a path to save the files (e.g. ./LATTE_output or /Users/yourname/Desktop/LATTE_output) : " )
	
		# SAVE the new output path
		with open("_config.txt",'w') as f:
			f.write(str(indir))
	
		print("\n New path: " + indir)
	
		# this is also the first time that the program is being run, so download all the data that is required.
		print ("\n Download the data files required ... " )
		print ("\n This will take a while but luckily it only has to run once..." )

		# ------------------------------------------------
		#check whether the chosen (output) directory already exists, and if it doesn't create the directory.
		if not os.path.exists("{}".format(indir)):
			os.makedirs(indir)
	
		if not os.path.exists("{}/data".format(indir)):
			os.makedirs("{}/data".format(indir))
	
		# ------------------------------------------------

		# ----- REFERENCE FILES DOWNLOAD -----
		utils.data_files(indir)
		utils.tp_files(indir)
		utils.TOI_TCE_files(indir)
		utils.momentum_dumps_info(indir)
		# -----

	# if the user chooses to redefine the path
	
	elif args.new_path == True: 
	
		reply = yes_or_no()
	
		if reply == True:
			indir = input("\n \n Please enter a path to save the files (e.g. ./LATTE_output or /Users/yourname/Desktop/LATTE_output) : " )
	
			# SAVE the new output path
			with open("_config.txt",'w') as f:
				f.write(str(indir))	
			
			print("\n New path: " + indir)
	
		else:
	
			print ("LATTE will continue to run with the old path: {}".format(path))
			indir = path
	else:
		with open("_config.txt", 'r') as f:
			indir = str(f.readlines()[-1])
	

	# ------------------------------------------------
	#check whether the chosen (output) directory already exists, and if it doesn't create the directory.
	if not os.path.exists("{}".format(indir)):
		os.makedirs(indir)

	if not os.path.exists("{}/data".format(indir)):
		os.makedirs("{}/data".format(indir))

	# ------------------------------------------------

	'''
	Check whether to download the data reference files
	This will only run if you tell the program to run this (with the args)- needs to be run the first time that one wants to download data
	This should also be called if new TESS data is released 
	The program will check what data has already been downloaded and only download new data files.
	'''

	if (args.new_data != False) and (os.path.exists("_config.txt")): 

		# ----- REFERENCE FILES DOWNLOAD -----
		utils.data_files(indir)
		utils.tp_files(indir)
		utils.TOI_TCE_files(indir)
		utils.momentum_dumps_info(indir)
		# -----
	
	# -----------  INTERACTIVE VERSION  ------------
	# ---------------------------------------------
	
	'''
	
	NOTE: this requires you to have Tkinter installed. Tkinter currently does not work with certain new Mac operating systems.
	In order to run LATTE with an input list and not interatcively, state the path to the csv file when running the program.
	csv file must have format: "TICID, sectors, transits, BLS, model" - see example.
	The TIC ID and Sectors to look at can also be stated in the command line as an argument to save time
	The interactive tool is for ease of use and to avoid having to understand how to use the command line.
	'''
	
	# Check whether the a target list has been defined.
	if args.targetlist == 'no': 

		# Check whether the tic ID and the sector have already been entered
		# If both the sectors and the tic ID are already entered then TKinter does not need to be loaded
		if args.tic != 'no' and args.sector != 'no':
			tic = str(args.tic)
			sectors = str(args.sector)

			# Check whether we are looking at an FFI
			# The FFI information needs to be stored straight away so a folder needs to be created to store them. 
			# The folder for the non-FFIs is created later after the user choses whether to 'save' data or not.
			if args.FFI == True:
				newpath = '{}/{}'.format(indir,tic)

				# if this folder doesn't exist then create it...
				if not exists(newpath):
					os.makedirs(newpath)

			# --------
			# Run a function called TESS-point. This returns wthe sectors in which the target has 
			# been observed as well as the RA and DEC of the target. 
			sectors_all, ra, dec = utils.tess_point(indir, tic) 
			# --------

		# if either the tic or the sectors or both have not already been identified, run Tkinter (interactive tools)
		

		else:

			# make a GUI interface with TKinter
			ROOT = tk.Tk()
			ROOT.withdraw()
			# if this hasn't already been identified as an FFI through the command line, give the option to chose this when entering the TIC ID
			if args.FFI == False:

				# -----------
				class TICprompt(simpledialog.Dialog):
				
				    def body(self, master):
					
						# make a text box for the TIC ID
				        tk.Label(master, text="Enter TIC ID:").grid(row=0)
				        self.e1 = tk.Entry(master)
				        self.e1.grid(row=0, column=1)
				        
				        # make a check button with the option to run this in FFI mode
				        self.FFIbox = tk.IntVar()
				        self.answer = tk.Checkbutton(master,text="Check for FFI mode", variable=self.FFIbox)
				        self.answer.grid(row=1, column=1,  columnspan=2)
				
				    def apply(self):
				    	# make these global variables so that they can be used outside of this class and applied to the rest of the program
				        global tkTIC
				        global tkFFI
				
				        ROOT.form=(self.FFIbox.get())
				        tkTIC = (self.e1.get())
				        tkFFI =  (self.FFIbox.get())
        		# -----------

				TICprompt(ROOT)
				# make the TIC a string
				tic = str(tkTIC)

				# If the FFI button was checked, change the FFI argument 

				if tkFFI == 1:
					args.FFI = True

			else: # if this is a FFI, don't give the FFI option again
				# has the tic already been defined?
				if args.tic == 'no':
	
					# load first prompt window which asks for TIC ID	
					tic = simpledialog.askstring(title="TIC",
													  prompt="Enter TIC ID:")
				else:
					tic = str(args.tic)

			# -----------

			# Is this an FFI? - if it is, need to create a folder to store the FFI data in (one for each TIC ID)
			if args.FFI == True:
				newpath = '{}/{}'.format(indir,tic)
				# if this folder doesn't exist then create it...
				if not exists(newpath):
					os.makedirs(newpath)

			# has the sector already been defined? 
			if args.sector == 'no':
				# returns all of the sectors in which TESS observed the given TIC id - this uses TESS-point

				sectors_all, ra, dec = utils.tess_point(indir, tic) 
		
				# The user is shown a list of the sectors im which the target is observed 
				# and asked to state whichones they want to assess

				sectors = simpledialog.askstring(title="Sectors",
												  prompt="TIC {} was observed in sector(s):\n {}. \n Enter the ones you wish to look at (e.g. 1,4) or 'all' for all of them.".format(tic, sectors_all))
			else:
				# still need to run tess point even if the targets are already defined as we need to check whether target appears in the stated sector - sanity check
				sectors_all, ra, dec = utils.tess_point(indir, tic) 
				sectors = str(args.sector)

			# close the TKinter windows.
			ROOT.quit()
			ROOT.destroy()
		
		# if no sector is defined or the word 'all' is written in the box, analyse all of the given sectors.
		if len(sectors) == 0:
			sectors = 'all'

		
		# if not all of them are chose, convert the input list (given as a string) into a python readable list
		if sectors != 'all':
			sectors = sectors.split(",")
			sectors = [int(i) for i in sectors]
		
		print ("\n")
		
		# print out the information that has been chosen to the command line.
		if sectors == 'all':
			print ("Will look at sector(s): {} \n".format(str(sectors_all)[1:-1]))
			sectors = sectors_all
		else:
			print ("Will look at sector(s):  {} \n".format(str(sectors)[1:-1]))
	
		# start up LATTE interactive where the transit times can be chosen manually 
		# this works differently for FFI data and target files as the data has a different format

		if args.FFI == False:
			utils.interact_LATTE(tic, indir, sectors_all, sectors, ra, dec, args)  # the argument of whether to shos the images or not 
		else:
			utils.interact_LATTE_FFI(tic, indir, sectors_all, sectors, ra, dec, args)
		
		# Done

	# ---------------------------------------
	# ---------------------------------------
	#			RUN WITH INPUT FILE
	# ---------------------------------------
	
	else:

		try:
			targetlist = pd.read_csv("{}".format(args.targetlist)) # If a path is defined, open the input file
		except:
			print ("This target list can't be found. Check the path you have given and the name and format of the file.")

		# process each target individually. 
		for index, row in targetlist.iterrows():
			
			# ---- INPUT PARAMETERS ------

			tic = str(int(row['TICID']))

			existing_files = glob("{}/*{}*".format(indir, tic))
			
			# Check whether this file already exist
			# if it already exists it will only be overwritten if --o function has been enabled to avoid file loss.
			if (len(existing_files) > 0)  and (args.o != True): 
				print ("This file already exists therefore SKIP. To overwrite files run this code with --o in the command line.")
				continue


			# --- WHAT SECTORS WAS IT OBSERVED IN? ---

			sectors_all, ra, dec = utils.tess_point(indir, tic) 
			sectors_in = row['sectors']
			
			try:
				sectors_in = ast.literal_eval(sectors_in)
				if (type(sectors_in) == int) or (type(sectors_in) == float):
					sectors_in = [sectors_in]
				else:
					sectors_in = list(sectors_in)
				
				# Sucessfully entered sectors
				# check that the target was actually observed in the stated sector
				sectors = list(set(sectors_in) & set(sectors_all))
				if len(sectors) == 0:
					print ("The target was not observed in the sector(s) you stated ({}). \
							Therefore take all sectors that it was observed in: {}".format(sectors, sectors_all))
					sectors =sectors_all
			except:
				sectors = sectors_all
	

			# ---- IF NO TRANSIT MARKED RUN WITH INTERFACE ----
			if type(row['transits']) == float:
				utils.interact_LATTE(tic, indir, sectors_all, sectors, args.noshow)

			else:
				transit_list_in = (row['transits'])
				transit_list = ast.literal_eval(transit_list_in)
				
				# convert the input transit times and sectors into transit_list in the form of a list
	
				if (type(transit_list) == float) or (type(transit_list) == int):
					transit_list = [transit_list]
				else:
					transit_list = list(transit_list)
				
				BLS_in = row['BLS']
				model_in = row['model']
	
				# ---- do you want to run a BLS? ----
				if (BLS_in == 'yes') or (BLS_in == 'True') or (BLS_in == 'true') or (BLS_in == '1'):
					BLS = True
				else:
					BLS = False
				
				# ---- do you want to model this transit? ----
				if (model_in == 'yes') or (model_in == 'True') or (model_in == 'true') or (model_in == '1'):
					model = True
				else:
					model = False
				
				simple = False  # we don't want to run the simple version - that's option is simply to do quick test
				save = True  # always save the files - no point running this if you're not going to save them
				DV = True   # we'll make a DV report for all of them
				args.noshow == True  # don't show these, just save them
				# ----------------------------------------
				#			 DOWNLOAD DATA 
				# ----------------------------------------
				
				alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2, ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad = utils.download_data(indir, sectors, tic)
				
				# ----------------------------------------
				#			   START BREWING ....
				# ----------------------------------------
				
				brew.brew_LATTE(tic, indir, transit_list, simple, BLS, model, save, DV, sectors, sectors_all, alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2, ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad, ra, dec, args)


	# end by changing the name of the folder to include the nicknane if defined
	# this allows users to keep track of their targets more easily e.g. Planet Hunters TESS candidates are named after pastries.
		
	if not args.nickname == 'noname':
		os.system("mv {}/{} {}/{}_{}".format(indir, tic, indir, tic, args.nickname))
	
	print ("\n  Complete! \n ")
# End.
