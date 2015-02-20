"""
Can execute this as a script to populate the GMM or load it as a module

The IDTF features are temporarily saved at a file local to the project directory.
Automatically generates this output directory called ./TMP_FEATURES

The output gmm_list.npz file is saved in the project directory.

Pca reduction on each descriptor is set to false by default.
"""
import computeIDTF, IDT_feature, computeFV
import numpy as np
import sys, os, random
sys.path.append("/usr/local/yael")
#sys.path.append("~/code/yael")
from yael import ynumpy
from tempfile import TemporaryFile
import argparse

def populate_gmms(PROJ_DIR,TMP_FEATURES,k_gmm,GMM_OUT,sample_size=1500000, PCA=False):
    """
    sample_size is the number of IDTFs that we sample from the total_lines number of IDTFs
    that were computed previously.

    Saves the GMMs in the GMM_OUT file as the gmm_list attribute.

    PROJ_DIR is the directory of the project (directory where we save the gmm_list)
    TMP_FEATURES is the directory of the temporary .feature vectors

    Returns the list of gmms.
    """
    feature_list = [filename for filename in os.listdir(TMP_FEATURES) if filename.endswith('.features')]
    #total_lines = 2488317
    total_lines = total_IDTF_lines(TMP_FEATURES)
    print "Total IDTFs constructed", total_lines
    sample_size = min(total_lines,sample_size)
    sample_indices = random.sample(xrange(total_lines),sample_size)
    sample_indices.sort()

    sample_descriptors = IDT_feature.list_descriptors_sampled(TMP_FEATURES, feature_list, sample_indices)
    bm_list = IDT_feature.bm_descriptors(sample_descriptors)
    #Construct gmm models for each of the different descriptor types.
    
    gmm_list = [gmm_model(bm, k_gmm, PCA=PCA) for bm in bm_list]
    np.savez(GMM_OUT, gmm_list=gmm_list)
    return gmm_list


def gmm_model(sample, k_gmm, PCA=False):
    """
    Returns a tuple: (gmm,mean,pca_transform)
    gmm is the ynumpy gmm model fro the sample data. 
    pca_tranform is None if PCA is True.
    Reduces the dimensions of the sample (by 50%) if PCA is true
    """

    print "Building GMM model"
    # until now sample was in uint8. Convert to float32
    sample = sample.astype('float32')
    # compute mean and covariance matrix for the PCA
    mean = sample.mean(axis = 0) #for each row
    sample = sample - mean
    pca_transform = None
    if PCA:
        cov = np.dot(sample.T, sample)

        #decide to keep 1/2 of the original components, so vid_trajs_bm.shape[1]/2
        #compute PCA matrix and keep only 1/2 of the dimensions.
        orig_comps = sample.shape[1]
        pca_dim = orig_comps/2
        #eigvecs are normalized.
        eigvals, eigvecs = np.linalg.eig(cov)
        perm = eigvals.argsort() # sort by increasing eigenvalue 
        pca_transform = eigvecs[:, perm[orig_comps-pca_dim:orig_comps]]   # eigenvectors for the 64 last eigenvalues
        # transform sample with PCA (note that numpy imposes line-vectors,
        # so we right-multiply the vectors)
        sample = np.dot(sample, pca_transform)
    # train GMM
    gmm = ynumpy.gmm_learn(sample, k_gmm)
    toReturn = (gmm,mean,pca_transform)
    return toReturn

def total_IDTF_lines(GMM_dir):
    """
    Returns the total number of IDTFs (features) computed
    for all of the videos. Each line in a .feature file is an IDTF, so this
    is the total number of lines in the GMM_dir
    """ 
    videos = [filename for filename in os.listdir(GMM_dir) if filename.endswith('.features')]
    total_lines = sum([sum(1 for line in open(os.path.join(GMM_dir, vid))) for vid in videos])
    return total_lines


def computeIDTFs(vid_list, TMP_FEATURES):
    """
    Computes the IDTFs specifically used for constructing the GMM
    vid_list list of videos in the format: ['vid_name'] [class#]

    The IDT features are output in TMP_FEATURES directory in Project_DIR

    Precondition: TMP_FEATURES directory does not yet exist.
    """
    os.makedirs(TMP_FEATURES)

    for line in vid_list:
        videoLocation = line.split()[0]
        featureOutput = os.path.join(TMP_FEATURES,os.path.basename(videoLocation).split('.')[0]+".features")
        print "Computing IDTF for %s" % (os.path.basename(videoLocation))
        computeIDTF.extract(videoLocation, featureOutput)
        print "complete."  


def sampleVids(vid_list, percentage):
    """
    vid_list list of videos in the format: ['vid_name'] [class#]

    This function randomly samples the reads the video names and creates a list with one video
    from each class.

    Assume percentage is 0 <= p <= 1
    """

    sample_indices = random.sample(xrange(len(vid_list)),int(len(vid_list)*percentage))
    sample_indices.sort()
    return [vid_list[i] for i in sample_indices]


#python gmm.py 120 UCF101_dir train_list
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("k_gmm", help="number of GMM modes", type=int)
    parser.add_argument("project_dir", help="Output directory to store .feature IDTFs", type=str)
    parser.add_argument('-f', "--input_list", help="List of input videos from which to sample", type=str)
    parser.add_argument('-s', "--sample_percentage", help="Percentage of videos to use to extract .feature vectors", type=float)

   # parser.add_argument("-p", "--pca", type=float, help="percent of original descriptor components to retain after PCA")
    parser.add_argument("-p", "--pca", action="store_true",
        help="Reduce each descriptor dimension by 50 percent using PCA")
    args = parser.parse_args()

    #Check if the TMP_FEATURES directory has already been created.
    TMP_FEATURES = os.path.join(args.project_dir,"TMP_FEATURES")

    if os.path.exists(TMP_FEATURES):
        raise ValueError("Temporary .feature directory already exists.")

    #Read in the videos
    input_vids = []
    if args.input_list is None:
        for line in sys.stdin:
            input_vids.append(line)
    else:
        f = open(args.input_list, 'r')
        input_vids = f.readlines()
        f.close()

    #sample the percentage of videos.
    vid_samples = input_vids
    if args.sample_percentage is not None:
        vid_samples = sampleVids(input_vids,args.sample_percentage)


    computeIDTFs(vid_samples, TMP_FEATURES)

    GMM_OUT=os.path.join(args.project_dir,"gmm_list")
    populate_gmms(args.project_dir,TMP_FEATURES,args.k_gmm,GMM_OUT,PCA=args.pca)

