import numpy as np
import sys, os, pickle
sys.path.append("../../code/")
import avconv
import csv

#The video data can come from a number of different directories.
UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/videos/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/videos/"
BACK_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Background/videos/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/videos/"


"""

For each video set directory, determine the length of each video. If the video
duration is less than the threshold (240 seconds), then
include the video in the output list.

The output list is constructed by relying on the map from video_name to output class.

"""
THRESHOLD = 240 #seconds


#UCF 101 videos are all very short. There is no need to measure their lengths.



def write_filtered(directory,out_file,vid_to_class, threshold=240):
	"""
	outfile: e.g., valid_list.txt

	"""
	vidClassOutput = []
	for vid in os.listdir(directory):
		duration = avconv.getDuration(os.path.join(directory,vid))
		vid_name = vid.split('.')[0]
		class_id = vid_to_class[vid_name]
		if duration <= threshold:
			vidClassOutput.append((vid,class_id))

	with open(out_file, 'wb') as f:
	    writer = csv.writer(f, delimiter=' ')
	    for vid, class_id in vidClassOutput:
	   		writer.writerow([vid, class_id])


directories = [VALID_DIR, TEST_DIR]
mapNames = ["VALID_vidmap.pkl", "TEST_vidmap.pkl"]
outLists = ["valid_list.txt", "test_list.txt"]
for directory, mapName, outList, in zip(directories,mapNames,outLists):
	with open(mapName) as f:
	    _, vid_to_id = pickle.load(f)
	write_filtered(directory,outList,vid_to_id)













