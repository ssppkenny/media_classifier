import numpy as np
import nltk
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
from collections import Counter

extensions = [".pdf", ".epub", ".mp3", ".flac", ".avi", ".mp4", ".mkv"]
media_type = {0 : "books", 1 : "music", 2 : "Films", 3 : "Audiobooks", 4 : "Series"}

def prepare_data(filenames, Y, bag, from_files=True):
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
        dump(cls, '~/.cls.joblib') 
        return cls
    else:
        load('~/.cls.joblib')

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
    for root, subdirs, files in os.walk(dir_name):
        filenames = []
        for f in files:
            if any([f.endswith(x) for x in extensions]):
                filenames.append(f)

    return {dir_name : media_type[Counter(predict(filenames, cls, bag)).most_common()[0][0]]}

def predict(filenames, cls, bag):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    X = np.zeros((len(filenames), len(bag)))
    for i in range(len(filenames)):
        words = tokenizer.tokenize(filenames[i])
        X[i,:] = np.array([int(b in words) for b in bag])

    d = dict(zip(filenames, cls.predict(X)))
    return dict((k,media_type[v]) for (k,v) in d.items())

def classify(dir_name, cls, bag):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    dirs = [f for f in os.listdir('.') if not os.path.isfile(f)]

    d1 = predict(files, cls, bag)
    d2 = dict([(d,predict_dir(d, cls, bag)[d]) for d in dirs])
    return {**d1, **d2}
        

if __name__ == '__main__':
    dir_name = "/home/sergey/Downloads"
    filenames, Y,  bag = read_dir(dir_name)
    cls = prepare_data(filenames, Y, bag)

    prediction = classify(dir_name, cls, bag)
    print(prediction)




