import numpy as np
import nltk
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

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
    
    cls = DecisionTreeClassifier()
    cls.fit(X,Y)
    return cls

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

def predict(filenames, cls, bag):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    X = np.zeros((len(filenames), len(bag)))
    for i in range(len(filenames)):
        words = tokenizer.tokenize(filenames[i])
        X[i,:] = np.array([int(b in words) for b in bag])

    return cls.predict(X)

if __name__ == '__main__':
    dir_name = "/home/sergey/Downloads"
    filenames, Y,  bag = read_dir(dir_name)
    cls = prepare_data(filenames, Y, bag, dir_name)

    file_name1 = "Java Programming Data.epub".lower()
    file_name2 = "02. Amadeus Liszt - Win The Race (12'' Version).mp3".lower()
    file_name3 = "Coding Tricks and Tips March 2020.pdf".lower()
    file_name4 = "01. Alan Brando - The Same Old Story (Extended Vocal Disco Mix).mp3"
    file_name5 = "Happily.2021.1080p.WEBRip.x264-RARBG.mp4"
    file_name6 = "Thundercloud.2015.1080p.AMZN.WEBRip.DDP5.1.x264-ISA.mkv"
    prediction = predict([file_name1, file_name2, file_name3,
        file_name4, file_name5, file_name6], cls, bag)
    print(prediction)



