#!/usr/bin/env sh
# Compute the mean image from the imagenet training leveldb
# N.B. this is available in data/ilsvrc12

#./build/tools/compute_image_mean examples/imagenet/ilsvrc12_train_leveldb \
#  data/ilsvrc12/imagenet_mean.binaryproto

CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/compute_image_mean ./train_lmdb/ ./mean.binaryproto
NUMPY_OUTFILE="mean.npy";
python /afs/cs.stanford.edu/u/anenberg/scr/snrThesis/caffe_code/convert_protomean.py mean.binaryproto $NUMPY_OUTFILE
