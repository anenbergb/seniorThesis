In this project we will try to perform the first tubelet experiments.

First, we need to filter the videos by length. We decide to discard all
videos of length longer than 4 minutes. (240 seconds)

The video lists are in the current directory:

ucf_list.txt
valid_list.txt
test_list.txt

Also the dictionary of class names to index and visa vera

class_index.pkl


Next, for each video split it into frames of .jpg and .ppm format.
- Extract frames and save then in a directory 'Frames' (here 'ppm' in .ppm format required by libsvx.v3.0).

1. For each dataSet, create a directory and populate it with sub-directoryies of the video_name
	ppm - (contains .ppm frames)
	Frames (contains .png frames)
	ppm_c200_sz500
	AC_IMEmap: initial GB segmentation
	svox (empty)
	tubelet.mat (destination of where to save the tubelet)

Tubelet extraction, for details refer to findTubelets.py

To construct the tubelets I had to specify a merging scheme:
I used options 5 and 13
5: C+T+S+F
13: M+C+T+S+F (I think)





Some calculations of size of video frame folders.
43M	./video_validation_0001001/Frames
197M	./video_validation_0001001/ppm
240M	./video_validation_0001001

Lower bound of 10 seconds would equate to 60.3Mb
So, upper bound of 240 second video would equate to 1.4 Gb of space.

For ucf_list.txt : 13,320 videos at approximately 10 seconds each. >> 784 Gb
For valid_list.txt : 779 videos >> 1090 Gb (upper bound)
For test_list.txt : 1345 >> 1883 Gb

First will experiment with 10 videos from ucf and 10 from valid_list

w-Flow
http://www.irisa.fr/texmex/people/jain/w-Flow/


COMMANDS executed in this directory:

1. Compute map from class name to index.
python $SRC"compute_UCF101_class_index.py" $CLASS_INDEX $CLASS_INDEX_OUT -p -z

2. Computes maps .pkl files which contain dictionaries from the 
video name to the class index.
python makeNameIndexMap.py

3. Builds ucf_list.txt, valid_list.txt, test_list.txt 

filterByLength.py

4. Split video into frames.
python extractFrames.py

5. Extract tubelets from videos.
python findTubelets.py





