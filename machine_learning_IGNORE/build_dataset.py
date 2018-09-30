"""
Split the dataset into test/train/validation sets 
there are two folders initially containing data : raw_gates and raw random_articles
raw_gates/
        article1
        article2
        article3
        ...

random_articles/
        article1
        article2
        article3
        
        ...


the data get splitted into subfolders which name should signal the label. e.g.:

test/
    gates/
        article1
        article2
        ....
    other/
        article1
        article2
        ...

"""
def write_file(filename, output_dir) : 
    print(filename,output_dir)
    write_file = filename.split('/')
    src_gates = str(path_gates_data+write_file[1])
    src_other= str (path_others_data+write_file[1])
    dst = str(output_dir+'/'+filename)
    if not os.path.exists(output_dir+'/'+write_file[0]):
        os.mkdir(output_dir+'/'+write_file[0])
    if write_file[0] == 'gates' : 
        copyfile(src_gates,dst)
    elif write_file[0] == 'other' : 
        copyfile(src_other,dst)



def preprocess_files(filenames):
    # Make sure to always shuffle with a fixed seed so that the split is reproducible
    random.seed(230)
    filenames.sort()
    random.shuffle(filenames)
    split_train = int(ratio_train * len(filenames))
    split_test =split_train + int (ratio_test * len(filenames))
    #the valid slice will just be astimated as the substraction of the sum of train and test from 1 
    train_filenames = filenames[:split_train]
    test_filenames = filenames[split_train:split_test]
    valid_filenames = filenames[split_test:]
    filenames = {'train': train_filenames,
                     'valid': valid_filenames,
                     'test': test_filenames}

    return filenames



import os
import random
from shutil import copyfile
from tqdm import tqdm
#initil params
path_gates_data ="raw_gates/"
path_others_data="raw_random_articles/"
#the ratio between test / train and validation have to sum up to one!
ratio_train = 0.8
ratio_test  = 0.15
ratio_valid = 0.05
# Define the data directories
train_data_dir = "train/"
test_data_dir =  "test/"
valid_data_dir = "valid/"
# Get the filenames in each directory (raw_gates and raw_random_articles)
filenamesGates = os.listdir(path_gates_data)
filenamesGates = [os.path.join('gates', f) for f in filenamesGates ]
filenamesOther =  os.listdir(path_others_data)
filenamesOther = [os.path.join('other', f) for f in filenamesOther ]
# Gates Files preprocessing
filenames_gates = preprocess_files(filenamesGates)
#Other Files preprocessing
filenames_other = preprocess_files(filenamesOther)
# Preprocess train, dev and test
for split in ['train', 'valid', 'test']:
    output_dir_split = os.path.join( format(split))
    if not os.path.exists(output_dir_split):
        os.mkdir(output_dir_split)
    else:
        print("Warning: dir {} already exists".format(output_dir_split))
    print("Processing {} data, saving preprocessed data to {}".format(split, output_dir_split))
    for filename in tqdm(filenames_gates[split]):
        write_file(filename,output_dir_split)
    for filename in tqdm(filenames_other[split]):
        write_file(filename,output_dir_split)
print("Done building dataset")

