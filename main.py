import numpy as np
import nltk
import os
from sklearn.linear_model import LogisticRegression


def prepare_data(filenames, Y, bag, dir_name):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    counter = 1
    for k, v in bag.items():
        bag[k] = counter
        counter+=1
    X = np.zeros((len(filenames), len(bag)))
    for i in range(len(filenames)):
        words = tokenizer.tokenize(filenames[i])
        X[i,:] = np.array([int(b in words) for b in bag])
    return X,Y

def read_dir(dir_name):
    filenames = []
    Y = []
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    bag_of_words = set([])
    extensions = [".pdf", ".epub", ".mp3", ".flac", ".avi", ".mp4", ".mkv"]
    for root, subdirs, files in os.walk(dir_name):
        for f in files:
            if any([f.endswith(x) for x in extensions]):
                full_path = os.path.join(root, f)
                to_classify = False
                if full_path.startswith(dir_name + "/books"):
                    Y.append(0)
                    to_classify = True
                elif full_path.startswith(dir_name + "/music"):
                    Y.append(1)
                    to_classify = True
                elif full_path.startswith(dir_name + "/Films"):
                    Y.append(2)
                    to_classify = True
                elif full_path.startswith(dir_name + "/Audiobooks"):
                    Y.append(3)
                    to_classify = True
                elif full_path.startswith(dir_name + "/Series"):
                    Y.append(4)
                    to_classify = True

                if to_classify:
                    filenames.append(f.lower())
                    words = tokenizer.tokenize(f)
                    bag_of_words.update(words)

    return filenames, Y, dict.fromkeys(bag_of_words,1)
if __name__ == '__main__':
    dir_name = "/Users/sergey/Downloads/test"
    filenames, Y,  bag = read_dir(dir_name)
    X,Y = prepare_data(filenames, Y, bag, dir_name)
    cls = LogisticRegression(multi_class="multinomial")
    cls.fit(X,Y)
    

    file_name = "Java Programming Data.epub".lower()
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(file_name)
    print(words)
    x = np.array([int(b in words) for b in bag])

    print(cls.predict(x.reshape(1,-1)))



