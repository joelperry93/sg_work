import numpy as np 
import regex as re

def clean_weird_values(input_string):
    bad_values = ['length price', '$/ea.', 'Bundle', 'Box']
    if input_string in bad_values: 
        return 'delete'
    else: 
        return str(input_string)

def remove_0(input_string):
    # for bella frames. they all came with an extra 0 on the end
    return input_string[:-1]

def special_match(input_string):
    search = re.compile('[^0-9.]').search
    if not bool(search(input_string)):
        return input_string
    else:
        return np.nan

def num(input_string):
    try:
        return int(input_string)
    except ValueError:
        return float(input_string)

def cleanPricePipeline(input_string):
    input_string = str(input_string)
    input_string = clean_weird_values(input_string)
    input_string = input_string.replace('$', '')
    input_string = input_string.replace('. ', '')
    input_string = input_string.replace(' ', '')
    input_string = input_string.replace(',', '')
    input_string = special_match(input_string)
    return input_string

def cleanFramePipeline(input_string):
    input_string = str(input_string)
    input_string = input_string.replace('*', '')
    input_string = input_string.replace('"', '')
    input_string = input_string.replace('...', '')
    input_string = input_string.replace('..', '')
    input_string = input_string.replace('.', '')
    input_string = input_string.replace('......', '')
    input_string = input_string.replace('::J', '')
    input_string = input_string.replace('"<""', '')
    input_string = input_string.replace('~ ', '')
    input_string = input_string.replace('"<""', '')
    input_string = input_string.replace('"<""', '')
    input_string = input_string.replace('-,', '')
    input_string = input_string.replace('Q)', '')
    input_string = input_string.replace('<', '')
    input_string = input_string.replace('ti)', '')
    input_string = input_string.replace('w ', '')
    input_string = input_string.replace('en ', '')
    input_string = input_string.replace('ti)', '')
    input_string = input_string.strip()
    return input_string