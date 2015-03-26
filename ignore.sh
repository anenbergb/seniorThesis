#find ./* -size +50M | cat >> .gitignore
find ./* -size +50M | awk '{print substr($0,3)}' | cat >> .gitignore