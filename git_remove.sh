git filter-branch --force --index-filter "git rm --cached --ignore-unmatch data/frames_detection/lists/train_list.txt"
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch data/frames_detection/lists/fullpath_test_list.txt"
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch data/frames_detection/lists/fullpath_train_list.txt"