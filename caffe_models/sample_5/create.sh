#!/usr/bin/env sh
rm -r train_lmdb/
rm -r test_lmdb/
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs
CAFFE=/afs/cs.stanford.edu/u/anenberg/scr/caffe
PROJECT=/afs/cs.stanford.edu/u/anenberg/scr/snrThesis

EXAMPLE=$PROJECT/caffe/sample_5
DATA=$PROJECT/data/frames_detection/lists
TOOLS=$CAFFE/build/tools

TRAIN_DATA_ROOT=/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/train/
TEST_DATA_ROOT=/afs/cs.stanford.edu/u/anenberg/scr/CS231N/data/allFrames/test/





# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=false
if $RESIZE; then
  RESIZE_HEIGHT=224
  RESIZE_WIDTH=224
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet training data is stored."
  exit 1
fi

if [ ! -d "$TEST_DATA_ROOT" ]; then
  echo "Error: TEST_DATA_ROOT is not a path to a directory: $TEST_DATA_ROOT"
  echo "Set the TEST_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi


echo "Creating train lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $TRAIN_DATA_ROOT \
    $DATA/shuffle_sampled_t1_5_train_list.txt \
    $EXAMPLE/train_lmdb

echo "Creating test lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    $TEST_DATA_ROOT \
    $DATA/shuffle_sampled_t1_5_test_list.txt \
    $EXAMPLE/test_lmdb

echo "Done."
#    --shuffle \