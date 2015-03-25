import pandas as pd
import sys, numpy as np
sys.path.append("/afs/cs.stanford.edu/u/anenberg/scr/caffe/python/")
import caffe, os
import lmdb

full_list = '../../data/ucf_recognition_20/lists/sampled_t1_p10_fullpath_all_list.txt'


def get_label_from_list(list_filename):
    df = pd.read_csv(list_filename, delimiter= ' ', header = None, names = ['filename', 'class_id'])
    return df

frame_df =  get_label_from_list(full_list)
frame_df['video_name'] = frame_df.filename.apply(lambda x: x.split('/')[-2])

num_frames = len(frame_df)
num_videos = len(frame_df.video_name.unique())

print "num frames: %d, num videos: %d" % (num_frames,num_videos)

def extract_CNN_features(features_dir):
    """
    features_dir is the relative directory in the /extracted folder
    df: data frame of the list associated with these features.
    """
    extract_dir = '/afs/cs.stanford.edu/u/anenberg/scr/snrThesis/caffe_models/ucf_recognition_20_pretrained/extracted/'
    env = lmdb.open(os.path.join(extract_dir, features_dir), readonly=True)

    predicted_labels = [] # for a particular image, this will be the argmax for the scores
    data = np.zeros((num_frames, 4096)) # (N_images, num fc7 features)

    with env.begin() as txn:
        with txn.cursor() as cursor:
            for i in range(num_frames):
                key = str(i)
                val = cursor.get(key)
                datum = caffe.proto.caffe_pb2.Datum()
                datum.ParseFromString(val)
                # datum.ListFields()[3][1] contains the scores
                data[i, :] = np.array(list(datum.ListFields()[3][1]))
    
    data_df = pd.DataFrame(data)
    data_df['video_name'] = frame_df['video_name']
    averaged_df = data_df.groupby('video_name').mean() #take the mean of the frames for the same video.
    return averaged_df

df = extract_CNN_features('pretrain')
np.savez('./cnn_features',data=df.as_matrix(columns=range(4096)))