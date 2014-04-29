**************************************************************************************************
* This document outlines the steps used to integrate the Wii Balance Board with Blender 2.70.
* 
* Python wrappers from Lubosz are used:
* 	http://lubosz.wordpress.com/2013/06/26/oculus-rift-support-in-blender-game-engine/
*
* (Unfortunately Cwiid libraries cannot be used because Blender uses Python3.3, and Cwiid is only
*	supported by Python2.*)
**************************************************************************************************
-----------------------------
Step 1 - Install Dependencies
-----------------------------

	Use Synaptic Package Manager to Install:
		1) python3.3
		2) python3.3-dev
		3) libpython3.3-dev
		4) python3-all
		5) cython
		6) cython3
		
-------------------------------------------------------------
Step 2 - Make and Install WiiC (http://wiic.sourceforge.net/)
-------------------------------------------------------------

	Install Dependencies:
		sudo apt-get install gcc g++
		sudo apt-get install cmake
		sudo apt-get install libbluetooth-dev

	Download WiiC Library:
		http://sourceforge.net/projects/wiic/files/
		
		--> Download and extract

	Make:
   		cd <WIIC_HOME>
   		mkdir build
   		cd build
   		cmake ../src
   		make

		## Do this if there are make errors regarding 'cv.h'. For some reason cv.h from OpenCV is called, but it is not needed. ##
		1) In /WiiC/src/ml/CMakeLists.txt
			--> Comment out everything

		2) In /WiiC/src/bin/CMakeLists.txt
			--> Comment out the following section:

				IF(OpenCV_FOUND)
					INCLUDE_DIRECTORIES(${OpenCV_INCLUDE_DIR})
					ADD_EXECUTABLE(wiic-ml ml.cpp)
					TARGET_LINK_LIBRARIES(wiic-ml wiicpp wiicml ${OpenCV_LIBS})
					INSTALL(TARGETS wiic-ml DESTINATION /usr/local/bin)
				ENDIF(OpenCV_FOUND)	

		--> Re-run make instructions.

	Install:
   		sudo make install
   		sudo ldconfig

--------------------------------------------------------------
Step 3 - Clone and edit Lubosz's Wii Balance Board Python Wrapper Code
--------------------------------------------------------------

	Clone Repo:
		git clone https://github.com/lubosz/python-balanceboard.git

	Edit Files:
		--> Lubosz's framework is good, but it has a few errors in it.

		setup.py
			1) Change '/usr/include/wiic' to '/usr/local/include/wiic'
				--> This is after WiiC is made and installed. Location referenced is wrong.

		BalanceBoard.cpp
			1) Change "wii->FindAndConnect(1);"

				to

				"wii->Find(1);
				 wii->LoadRegisteredWiimotes();
				 wii->Connect();" 
	
				--> The WiiC libraries that are available do not support the "FindAndConnect()" function. 
				--> This substitution works equivalently.

		balanceboard.pyx
			1) Add:
				property topRight:
					def __get__(self): return self.thisptr.topRight

				property bottomLeft:
					def __get__(self): return self.thisptr.bottomLeft

				property bottomRight:
					def __get__(self): return self.thisptr.bottomRight
				
				--> Add this to access all variables of Wii Balance Board Object. 

		


----------------------------------------------------------
Step 4 - Run setup.py Script to Generate Desired .so File
----------------------------------------------------------

	Don't forget to run the script with Python3.3, because Blender uses this:
		
		python3.3 setup.py build

------------------------------------------------
Step 5 - Link .so File to Blender Add-on Folder
------------------------------------------------

	--> Link .so file to the blender add-on folder.
		sudo ln -s $SOURCE/filename.so /usr/lib/blender/scripts/addons/

	Example:
		sudo ln -s /home/gregory/Documents/prjFloat/python-balanceboard-master/build/lib.linux-x86_64-3.3/balanceboard.cpython-33m.so /usr/lib/blender/scripts/addons/

--------------------------------------------------
Step 6 - Test the Build and Connection in Blender
--------------------------------------------------

	--> The balance.py script can be used to test the quality of the build, and also the connection in Blender.
			As long as there are no errors, everything should work.

		from balanceboard import PyBalanceBoard

		foo = PyBalanceBoard()

		while foo.hasWiiMotes():
		  foo.poll()
		  #print(foo.topLeft)
		  foo.printSensors()

------------------------------------------------------------
Step 7 - Read Values and Calculate CoP (Centre of Pressure)
------------------------------------------------------------

	#Global Variables
	WIIXMAX = 430 #length in mm
	WIIYMAX = 235 #width in mm

	#Function
	def calcCOP(tr,tl,br,bl):
		netForce = tr + tl + br + bl
		if((netForce < 50) and (netForce > -50)):
		    netForce = 0
		    copX = WIIXMAX / 2
		    copY = WIIYMAX / 2
		if(netForce != 0):
		    copX = ((((tr+br) - (tl+bl)) / (netForce*1.0))+1) * (WIIXMAX/2)
		    copY = ((((tr+tl) - (br+bl)) / (netForce*1.0))+1) * (WIIYMAX/2)
		values = [copX ,copY]
		return values

	#Call this in Code
	pos = calcCOP(foo.topRight, foo.topLeft, foo.bottomRight, foo.bottomLeft)






















