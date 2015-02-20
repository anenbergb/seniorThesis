
"""
Script to train a basic action classification system.

Trains a One vs. Rest SVM classifier on the fisher vector video outputs.
This script is used to experimentally test different parameter settings for the SVMs.

"""

import os, sys, collections, random, string, argparse, itertools
import numpy as np
from tempfile import TemporaryFile
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
import sklearn.metrics as metrics
import classify_library
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import consolidateFiles




"""
OLD:

SRC="/afs/cs.stanford.edu/u/anenberg/code/snrThesis/src/"
#Lists for this project
UCF_list=os.path.join(PROJ_DIR,"ucf_small.txt")
VALID_list=os.path.join(PROJ_DIR,"valid_small.txt")
TEST_list=os.path.join(PROJ_DIR,"test_small.txt")
#Load class index
class_index_file = os.path.join(SRC,"class_index.npz")
class_index_file_loaded = np.load(class_index_file)
class_index = class_index_file_loaded['class_index'][()]
index_class = class_index_file_loaded['index_class'][()]

def train_test_lists(train_list, test_list, Proj_dir,):

#    Returns two tuples. ( (X_train, y_train), (X_test, y_test))

    X_train_basenames, y_train  = as_list(train_list)
    X_test_basenames, y_test = as_list(test_list)

    ##THIS IS THE SAFE WAY, ALTERNATIVELY we could just assume that all the videos from our predefined list
    ##of basenames are actually in the FISHER directory.
    # Define training and testing splits.
    X_train_files = []
    X_test_files = []
    for filename in os.listdir(os.path.join(Proj_dir,"FISHER")):
        #each of the files here is a fisher vector.
        if filename.endswith('.npz'):
            #e.g. split v_ApplyEyeMakeup_g01_c01.fisher.npz
            file_base = os.path.basename(filename).split('.')[0]
            if file_base in X_train_basenames:
                X_train_files.append(filename)
            elif file_base in X_test_basenames:
                X_test_files.append(filename)

"""



def list_to_files(XY_list, Proj_dir):
    """
    Given a list of files (e.g. training, testing splits)
    returns the corresponding list of .fisher.npz files in the FISHER
    sub directory of Proj_dir.
    Returns a tuple (X_files, y)
    """
    #X_basenames, y_list  = as_list(X_list)
    ##THIS IS THE SAFE WAY, ALTERNATIVELY we could just assume that all the videos from our predefined list
    ##of basenames are actually in the FISHER directory.
    

    #XY = zip(X_basenames,y_list) #Tuples of [(X_1, y_1), (X_2,y_2), ..]
    print 
    X_files = []
    Y_list = []
    Fisher_Dir = os.path.join(Proj_dir,"FISHER")
    for filename in os.listdir(Fisher_Dir):
        #each of the files here is a fisher vector.
        if filename.endswith('.npz'):
            #e.g. split v_ApplyEyeMakeup_g01_c01.fisher.npz
            file_base = os.path.basename(filename).split('.')[0]
            for x_base,y in XY_list:
                if x_base==file_base:
                    full_file_path = os.path.join(Fisher_Dir,filename)
                    X_files.append(full_file_path)
                    Y_list.append(y)
    toReturn = (X_files, Y_list)
    return toReturn


#Returns:
# 1. np.ndarray where of verticallys stacked fisher vectors.
# 2. np.array of class labels
# Inputs:
# videos:  is a list of fisher.npz files
# fisher_path: path to the fisher vector directory
# class_index: dictionary from video name to the class.
def simple_FV_matrix(X_list, y_list):
    matrix = []
    for x_npz in X_list:
        matrix.append(np.load(x_npz)['fish'])
    X = np.vstack(matrix)
    Y = np.array(y_list)
    return (X,Y)



def sample_from_matrix(X, y, percentage):
    """
    X is a np.array (matrix)
    Y_list corresponding list of labels

    Assume percentage is 0 <= p <= 1
    """

    sample_indices = random.sample(xrange(X.shape[0]),int(X.shape[0]*percentage))
    sample_indices.sort()
    X_out = X[sample_indices]
    Y_out = y[sample_indices]
    toReturn = (X_out,Y_out)
    return toReturn

def funn():

     #completed_vids = [filename.split('.')[0] for filename in os.listdir(FISHER_DIR) if filename.endswith('.npz')]
      #  overlap = [vid for vid in input_vids if os.path.basename(vid.split()[0]).split('.')[0] in completed_vids]
        



    training = [filename for filename in os.listdir(training_output) if filename.endswith('.fisher.npz')]
    testing = [filename for filename in os.listdir(testing_output) if filename.endswith('.fisher.npz')]


    training_dict = classify_library.toDict(training)
    testing_dict = classify_library.toDict(testing)


    #GET THE TRAINING AND TESTING DATA.


    X_train_vids, X_test_vids = classify_library.limited_input(training_dict, testing_dict, 101, 24)
    X_train, Y_train = classify_library.make_FV_matrix(X_train_vids,training_output, class_index)
    X_test, Y_test = classify_library.make_FV_matrix(X_test_vids,testing_output, class_index)

    training_PCA = classify_library.limited_input1(training_dict,1)



    #Experiments with PCA
    pca_dim = 1000
    pca = PCA(n_components=pca_dim)
    pca.fit(X_train)
    X_train_PCA = pca.transform(X_train)
    X_test_PCA = pca.transform(X_test)
    estimator = OneVsRestClassifier(LinearSVC(random_state=0, C=100, loss='l1', penalty='l2'))
    classifier = estimator.fit(X_train_PCA, Y_train)
    metrics = classify_library.metric_scores(classifier, X_test_PCA, Y_test, verbose=True)
    print metrics


    do_learning_curve = False
    if do_learning_curve:
        X_full = np.vstack([X_train_PCA, X_test_PCA])
        Y_full = np.hstack([Y_train, Y_test])
        title= "Learning Curves (Linear SVM, C: %d, loss: %s, penalty: %s, PCA dim: %d)" % (100,'l1','l2',pca_dim)
        cv = cross_validation.ShuffleSplit(X_full.shape[0], n_iter=4,test_size=0.2, random_state=0)
        estimator = OneVsRestClassifier(LinearSVC(random_state=0, C=100, loss='l1', penalty='l2'))
        plot_learning_curve(estimator, title, X_full, Y_full, (0.7, 1.01), cv=cv, n_jobs=1)
        plt.show()


"""
Example usage:
python $SRC"classify_experiment.py" $PROJ_DIR $UCF_train1 $UCF_test1 $CLASS_INDEX_OUT
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("Proj_dir", help="Project Directory", type=str)
    parser.add_argument("train_list", help="Training list cut", type=str)
    parser.add_argument("test_list", help="Testing List cut", type=str)
    parser.add_argument("class_index_file", help="Class index file. .npz file which contains mappings from UCF101 class \
        class index", type=str)



    args = parser.parse_args()

    #Load the class_index file
    class_index_file_loaded = np.load(args.class_index_file)
    class_index = class_index_file_loaded['class_index'][()]
    index_class = class_index_file_loaded['index_class'][()]


    XY_train = zip(*consolidateFiles.as_list(args.train_list))
    XY_test = zip(*consolidateFiles.UCF_missing_y_as_list(args.test_list, class_index))

    X_train_list, y_train = list_to_files(XY_train, args.Proj_dir)
    X_test_list, y_test = list_to_files(XY_test, args.Proj_dir)

    X_train, Y_train = simple_FV_matrix(X_train_list, y_train)
    X_test, Y_test = simple_FV_matrix(X_test_list, y_test)

    #Percent of the training data that we want to sample to use to create the pca matrix
    PCA_sample_percentage = 0.25 
    X_train_sampled, _ = sample_from_matrix(X_train,Y_train,PCA_sample_percentage)


    #Experiments with PCA
    pca_dim = 1000
    pca = PCA(n_components=pca_dim)
    pca.fit(X_train_sampled)
    X_train_PCA = pca.transform(X_train)
    X_test_PCA = pca.transform(X_test)

    estimator = OneVsRestClassifier(LinearSVC(random_state=0, C=1, loss='l2', penalty='l2'))
    classifier = estimator.fit(X_train_PCA, Y_train)
    metrics = classify_library.metric_scores(classifier, X_test_PCA, Y_test, verbose=True)
    print metrics










