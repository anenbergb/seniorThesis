SRC="/afs/cs.stanford.edu/u/anenberg/scr/snrThesis/code/"






UCF_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/train_set.txt"
VALID_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Validation/validation_primaryclass.txt"
BACK_FULL=""
TEST_FULL="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Test/test_primaryclass.txt"



CLASS_INDEX="/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/ucfTrainTestlist/classInd.txt"
CLASS_INDEX_OUT="./class_index"

#python $SRC"compute_UCF101_class_index.py" $CLASS_INDEX $CLASS_INDEX_OUT -p -z

#python makeClassIndex.py

python filterByLength.py