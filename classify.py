import numpy as np
import nltk
import os
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
from collections import Counter
import sys

extensions = [".pdf", ".epub", ".mp3", ".flac", ".avi", ".mp4", ".mkv"]
media_type = {0 : "books", 1 : "music", 2 : "Films", 3 : "Audiobooks", 4 : "Series", 5: "Files"}

def prepare_data(filenames, Y, bag, from_files=True):
    path = os.path.expanduser('~/.cls.joblib')
    bag_path = os.path.expanduser('~/.bag')
    if from_files:
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        counter = 1
        for k, v in bag.items():
            bag[k] = counter
            counter+=1
        X = np.zeros((len(filenames), len(bag)))
        for i in range(len(filenames)):
            words = tokenizer.tokenize(filenames[i])
            X[i,:] = np.array([int(b in words) for b in bag])
        
        cls = DecisionTreeClassifier()
        cls.fit(X,Y)
        dump(cls, path)
        with open(bag_path, "wb") as f:
            pickle.dump(bag, f)
        return cls, bag
    else:
        with open(bag_path, "rb") as f:
            bag = pickle.load(f)

        return load(path), bag

def read_dir(dir_name):
    filenames = []
    Y = []
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    bag_of_words = set([])
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


def predict_dir(dir_name, cls, bag):
    filenames = []
    for root, subdirs, files in os.walk(dir_name):
        for f in files:
                filenames.append(f)
    new_filenames = list(filter(lambda x: any([x.endswith(y) for y in extensions]), filenames))
    if not new_filenames:
        return {dir_name : "Files"}
    return {dir_name : Counter(predict(new_filenames, cls, bag)).most_common()[0][1]}

def predict(filenames, cls, bag):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    X = np.zeros((len(filenames), len(bag)))
    for i in range(len(filenames)):
        words = tokenizer.tokenize(filenames[i])
        X[i,:] = np.array([int(b in words) for b in bag])

    d = dict(zip(filenames, cls.predict(X)))
    return dict((k,media_type[v]) for (k,v) in d.items())

def classify(dir_name, cls, bag):
    def condition(f):
        fn, ext = os.path.splitext(f)
        return ext in extensions 
    files = [f for f in os.listdir(dir_name) if not f.startswith(".") and not f.startswith("$") and os.path.isfile(dir_name + "/" + f) and condition(dir_name + "/" + f)]
    dirs = [f for f in os.listdir(dir_name) if not f.startswith(".") and not f.startswith("$") and not os.path.isfile(dir_name + "/" + f) and not f in media_type.values()]

    d1 = predict(files, cls, bag)
    d2 = dict([(d,predict_dir(dir_name + "/" + d, cls, bag)[dir_name + "/" + d]) for d in dirs])
    return {**d1, **d2}
        

if __name__ == '__main__':
    if len(sys.argv) > 1:
        dir_name = sys.argv[1]; ##"/home/sergey/Downloads"
        filenames, Y,  bag = read_dir(dir_name)
        cls, bag = prepare_data(filenames, Y, bag, from_files=False)

        prediction = classify(dir_name, cls, bag)
        for k, v in prediction.items():
            print(k,v)




