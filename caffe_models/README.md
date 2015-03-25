Summarize the performance of each test.

#sample_5: 
    * Uses the 20+1 background detection labeling.
    * Frames are labeled individually, so a video could contain frames from multiple classes (and always some background).
    * UCF portion of the training data set is temporally trimmed, so all the frames have the same label as the video.
    * only small portions of the validation videos contain frames labeled as one of the 20 classes, so large portions
    of the validation videos are labeled as background, 0.
    * randomly sampling 5 frames, means sampling 5 frames from each video. Thus, the 5 frames sampled from the validation and testing videos are very likely to be labeled as background, 0.
    *
    * After training, we test the CNN by averaging the scores for the 5 frames per video.
    * To test accuracy, we how well the averaged activation vector predicts the single video level label. 
    (note, for regonition the videos only have a single label)
    * compute AP for the videos for each class (and then mAP).
    
#sample_100

    * same as sample_5, but now sample 100 frames per video.
    
    
# recognition_20_sample_5
    * uses 20 classes, (same classes as in the detection challenge)
    * frames are given the single label of the video. 
    * sample 5 frames per video, average the activation vectors to a single vector per video.
    
# recognition_20_sample_100
    * same as recogition_20_sample_5, but now sample 100 frames per video.
    

# ucf_recognition_20_pretrained
    * Uses 20 classes, same classes as in the detection challenge.
    * forward propagate frames sampled from the UCF videos through a pre-trained ImageNet.
    * No fine-tuning, only forward propagation.

# ucf_recognition_20_svm
    * Try to train a 1-vs-all SVM using a CNN.
