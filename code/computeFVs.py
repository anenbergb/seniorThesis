import argparse
import computeIDTF, os, sys, subprocess, ThreadPool
import classify_library
import time

"""
Uses multi-threading to extract IDTFs and compute the Fisher Vectors (FVs) for
each of the videos in the input list (vid_in). The Fisher Vectors are output
in the output_dir

Creates the FISHER directory to store the fisher files.
"""


#This is is the function that each worker will compute.
def processVideo(vid,FISHER_DIR,gmm_list):
    """
    gmm_list is the file of the saved list of GMMs

    vid is a line in the vid_list of the format: ['vid_name'] [class#]
    """
    videoLocation = vid.split()[0]
    fisherOutput = os.path.join(FISHER_DIR,os.path.basename(videoLocation).split('.')[0]+".fisher")
    print videoLocation
    print fisherOutput
    computeIDTF.extractFV(videoLocation, fisherOutput,gmm_list)


#python computeFVs.py videos vid_in vid_out
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("project_dir", help="Output directory to store .fisher files", type=str)
    parser.add_argument('-g',"--gmm_list", help="File of saved list of GMMs", type=str)
    #This should be full path to the gmm_list file.
    parser.add_argument('-f', "--input_list", help="List of input videos from which to sample", type=str)
    parser.add_argument('-t', "--num_threads", help="Number of threads", type=int)

    args = parser.parse_args()
    print args.project_dir
    #Check if the FISHER directory has already been created. If it hasn't, then create it
    FISHER_DIR = os.path.join(args.project_dir,"FISHER")
    if not os.path.exists(FISHER_DIR):
        os.makedirs(FISHER_DIR)

    #Identify the gmm_list file. If gmm_list isn't given using the -g option, then it
    #is assumed to be located in the project directory.
    if args.gmm_list is None:
        gmm_list = os.path.join(args.project_dir,"gmm_list.npz")
        if not os.path.exists(gmm_list):
            raise ValueError("No gmm_list.npz file specified or in project directory.")
    else:
        gmm_list = args.gmm_list

    #Read in the videos
    input_vids = []
    if args.input_list is None:
        for line in sys.stdin:
            input_vids.append(line)
    else:
        f = open(args.input_list, 'r')
        input_vids = f.readlines()
        f.close()

    ###Just to prevent overwriting already processed vids
    completed_vids = [filename.split('.')[0] for filename in os.listdir(FISHER_DIR) if filename.endswith('.npz')]
    overlap = [vid for vid in input_vids if os.path.basename(vid.split()[0]).split('.')[0] in completed_vids]
    print overlap

    numThreads = 5
    if args.num_threads is not None:
        numThreads = args.num_threads
    #Multi-threaded FV construction.
    pool = ThreadPool.ThreadPool(numThreads)

    t0 = time.time()
    time_list = []
    for line in input_vids:
        if line not in overlap:
            pool.add_task(processVideo,line,FISHER_DIR,gmm_list)
            time_list.append(time.time())
    pool.wait_completion()

    #Timing.
    tf = time.time() - t0
    avg_time = 0
    if len(time_list) > 0:
        avg_time = tf/len(time_list)
    print "Average time to process a video: %f, Total time to process videos: %f" % (avg_time, tf)