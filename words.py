# -*- coding: utf-8 -*-

# Words Generator with sequence of letters

# Version for Linux and Windows
# Author: Serhii Buniak
# 22/03/2013

import os
import sys
import ConfigParser

import chardet

import transform_dict

#############
# CONSTANTS #
#############

CONFIG_FILENAME = 'config.cfg'

STANDART_WINDOWS_ENCODING = 'CP1251'

ERROR_FILE = 'Error read input file. Is file exist?'

ERROR_INPUT_DATA = """Error in input data. Check file, input must be like:
                      \na,q,f,e,o,p,o,d
                      4"""

ERROR_DICT_FILE = 'Error read dictionary file. Is file exist?'

ERROR_DICT_UNKNOWN = 'Unexpected error in dictionary file. File may be corrupted.'

ERROR_CONFIG_FILE = 'Error read config file (config.cfg). Is file exist?'

ERROR_GET_CONFIG = 'Error in get config, please check names of section and options in config file'

INPUT_FILENAME = 'input_filename'

DICT_FILENAME = 'dictionary_filename'

DICT_PICKLED_FILENAME = 'dictionary_pickled_filename'

OUTPUT_FILENAME = 'output_filename'

########
# CODE #
########

def get_filenames_from_config_file(configFilename):
    """ gets input filenames from config file """
    try:
        config = ConfigParser.ConfigParser()
        config.read(configFilename)
        filenames = {}
        filenames[INPUT_FILENAME] = config.get('filenames', INPUT_FILENAME)
        filenames[DICT_FILENAME] = config.get('filenames', DICT_FILENAME)
        dict_fname = filenames[DICT_FILENAME]
        filenames[DICT_PICKLED_FILENAME] = (dict_fname[:dict_fname.rfind('.')] +
                            '.' + config.get('filenames','dictionary_pickled_filename_extension'))
        filenames[OUTPUT_FILENAME]= config.get('filenames',OUTPUT_FILENAME)
        return filenames
    except IOError:
        print ERROR_CONFIG_FILE
    except:
        print ERROR_GET_CONFIG

def get_dictionary(filename, encoding):
    """ gets dictionary from file """
    try:
        words = open(filename).readlines()
        dictionary = map(lambda word: word.strip().decode(encoding).lower(), words)
        return dictionary
    except IOError:
        print ERROR_DICT_FILE
    except:
        print ERROR_DICT_UNKNOWN

def get_input_data(filename):
    """ gets input data from file """
    try:
        lines = open(filename).readlines()
        sequence = lines[0].replace(' ', '').replace(',', '')
        len_sequence = int(lines[1])
        return sequence, len_sequence
    except IOError:
        print ERROR_FILE
    except:
        print ERROR_INPUT_DATA

def write_progress(percentage):
    """ shows progress in percents """
    sys.stdout.flush()
    sys.stdout.write(percentage)

def is_word_can_be_constructed_from_sequence(word, sequence):
    """ returns True if word can be constructed with letters in sequence """
    count_found_letters = 0
    for index_w in range(len(word)):
        index_s = 0
        found = False
        while index_s < len(sequence) and not found:
            if word[index_w] == sequence[index_s]:
                sequence = sequence[:index_s] + sequence[index_s + 1:]
                count_found_letters += 1
                found = True
            index_s += 1
    if count_found_letters == len(word):
        return True


def main():
    """ gets input data and writes output data to file output.txt """
    filenames = get_filenames_from_config_file(CONFIG_FILENAME)
    if not filenames:
        return
    if os.path.exists(filenames[DICT_PICKLED_FILENAME]):
        dictionary_dict = transform_dict.load_obj_from_file(filenames[DICT_PICKLED_FILENAME])
    else:
        dictionary = get_dictionary(filenames[DICT_FILENAME], STANDART_WINDOWS_ENCODING)
        dictionary_dict = transform_dict.transform_dictionary(dictionary)
        transform_dict.save_obj_to_file(dictionary_dict, filenames[DICT_PICKLED_FILENAME])

    sequence, len_sequence = get_input_data(filenames[INPUT_FILENAME])
    sequence_encoding = chardet.detect(sequence)['encoding']
    sequence = sequence.decode(sequence_encoding)
    f = open(filenames[OUTPUT_FILENAME], 'w')
    counter = 0
    words_count = len(dictionary_dict[len_sequence])

    for item in dictionary_dict[len_sequence]:
        counter += 1
        word = item.decode(transform_dict.TRANSFORM_ENCODING)
        percent = round(counter * 100.0 / words_count)
        write_progress('\r%s %%' % percent)
        if is_word_can_be_constructed_from_sequence(word, sequence):
            f.write(item + '\n')

    f.close()
    print '\nProcess succesfully finished\n'

if __name__ == '__main__':
    print '\nStarting process. Please wait...\n'
    main()
