# -*- coding: utf-8 -*-

# Transforms list of words into dict obj, pickles to file and unpickles

# Author: Serhii Buniak
# 22/03/2013

import pickle

TRANSFORM_ENCODING = 'UTF-8'

def transform_dictionary(dictionary):
    """ gets dictionary, returns dict of list of words where keys - length of words """
    output_dict = {}
    for word in dictionary:
        word_encoded = word.encode(TRANSFORM_ENCODING)
        if len(word) in output_dict:
            output_dict[len(word)].append(word_encoded)
        else:
            output_dict[len(word)] = [word_encoded,]
    return output_dict

def save_obj_to_file(obj, filename):
    """ serializes object and saves to file """
    f = open(filename, 'w')
    pickle.dump(obj, f)

def load_obj_from_file(filename):
    """ loads serialized obj from file """
    f = open(filename)
    return pickle.load(f)

def main():
    """ transforms dictionary, saves it to file """
    dictionary_dict = transform_dictionary(open('pldf-win.txt'))
    save_obj_to_file(dictionary_dict, 'pldf-win.pkl')
    dictionary_dict = load_obj_from_file('pldf-win.pkl')
    for key in dictionary_dict:
        print len(dictionary_dict[key])

if __name__ == '__main__':
    main()
