"""
Next, for each video split it into frames of .jpg and .ppm format.
- Extract frames and save then in a directory 'Frames' (here 'ppm' in .ppm format required by libsvx.v3.0).

1. video_name
    ppm - (contains .ppm frames)
    Frames (contains .png frames)
"""
import os, csv, sys
sys.path.append("../../code/")
import avconv

UCF_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/videos/"
VALID_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/videos/"
BACK_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Background/videos/"
TEST_DIR="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/videos/"


DestinationDir = "./"

UCF_list = "./ucf_list.txt"
Valid_list = "./valid_list.txt"
Test_list = "./test_list.txt"

NUM_VIDS_TO_PROCESS = 10


def frames_from_vids(listname, dataDir, framesDir, num=10):
    """
    listname: list of the input videos.
    dataDir: directory where the actual video exits.
    framesDir: directory that we are populating for this data set.
    num: number of input videos to extract frames from.
    """

    vid_to_extract = []
    length = 0
    #with open(listname, 'r+') as f:
    f = open(listname, 'r+')
    data = csv.reader(f, delimiter=' ')
    for row in data:
        print row
        #e.g, filename.avi we want filename
        videoName = row[0]
        vid_to_extract.append(videoName)
        length +=1
    f.close()
    for vid in vid_to_extract[:num]:
        full_vid_path = os.path.join(dataDir,vid)
        avconv.extract_frames(full_vid_path,framesDir)
    


dataLists = [UCF_list, Valid_list, Test_list]
dataSets = ["UCF", "Validation", "Test"]
dataDirs = [UCF_DIR, VALID_DIR, TEST_DIR]



for dataList, dataSet, dataDir in zip(dataLists, dataSets, dataDirs)[:2]:
    framesDir = os.path.join(DestinationDir, dataSet)
    if not os.path.isdir(framesDir):
        os.makedirs(framesDir)
    frames_from_vids(dataList,dataDir,framesDir,num=NUM_VIDS_TO_PROCESS)



