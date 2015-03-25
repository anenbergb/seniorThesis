#!/usr/bin/env sh
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe

$CAFFE/build/tools/extract_features.bin $CAFFE"/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel" ./pretrain_all.prototxt fc7 ./extracted/pretrain/ 35114 lmdb GPU 1
