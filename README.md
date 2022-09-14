# CLOWN
Cloud detection software to be applied in observatories with an all-sky camera.


This software can be used with any type of all-sky camera even without knowing its parameters. 
To run, first create a config file, with the parameters according to the location and the camera used. You can see two examples of these config files for PASO (ConfigPASO.txt) and OPD (Config.txt).

To obtain the phase difference and the zenith position, choose an image and simulate it with Stellarium. Then save the (x,y) coordinates from the iamge and the (Alt,Az) from Stellarium and run "ZenithPhaseCalculator.py" to calibrate the pictures, using a selected image.

With Configuration ready, create a folder both in Images and Cloud Masks with the chosen name. Place your images in Image folder and then run CLOWN.py. It can be run from the terminal with:

python3 CLOWN.py Config.txt



If you use this code in your work, please cite our paper in IAF.
