import pandas as pd
import numpy as np
from extractPriceLists import *
from helpers import clean_weird_values, special_match, num, cleanPricePipeline, cleanFramePipeline

supplier_list = list(supplier_dict.keys())

def createMaster(supplier_list):
    df = []
    for i in supplier_list:
        print(str('processing' + ' ' + i))
        if supplier_dict[i]['method'] == 'excel':
            df.append(ExcelToDf(i))
        elif supplier_dict[i]['method'] == 'pdf':
            df.append(PdfToDf(i))
        elif supplier_dict[i]['method'] == 'omega':
            df.append(omegaSpecific(i))
        elif supplier_dict[i]['method'] == 'global':
            df.append(globalSpecific(i))
        elif supplier_dict[i]['method'] == 'universal':
            df.append(universalSpecific(i))
        elif supplier_dict[i]['method'] == 'ampf':
            df.append(ampfSpecific(i))
        elif supplier_dict[i]['method'] == 'foster':
            df.append(fosterSpecific(i))
        elif supplier_dict[i]['method'] == 'bella':
            df.append(bellaSpecific(i))
    df = pd.concat(df)
    return df


def finalDataset(supplier_list):
    df = createMaster(supplier_list)
    df = df.dropna()
    df['price'] = df['price'].apply(lambda x: cleanPricePipeline(x))
    df = df.dropna()
    df['frame'] = df['frame'].apply(lambda x: cleanFramePipeline(x))

    df = df.drop_duplicates(subset=['frame', 'supplier'])
    # return df.to_excel('master_list.xlsx', index=False)
    return df.to_csv('master_list.csv', index=False)

finalDataset(supplier_list)

# df = pd.read_csv('master_list.csv')
# df['price'] = df['price'].apply(lambda x: num(x))

