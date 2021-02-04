import pandas as pd
import numpy as np
import json
import tabula

root = './2021-price-lists/'

with open('suppliers.JSON', 'r') as f:
    supplier_dict = json.load(f)

def ExcelToDf(supplier):
    key = supplier_dict[supplier]
    file_path = root + str(key['file_path'])
    df = pd.read_excel(file_path, header = key['header'])
    df = df[[df.columns[key['frame']], df.columns[key['price']]]]
    df.columns = ['frame', 'price']
    df['supplier'] = supplier
    return df

def PdfToDf(supplier):
    key = supplier_dict[supplier]
    file_path = root + str(key['file_path'])
    df = tabula.read_pdf(file_path, 
                        pages=list(np.arange(key['first_page'],key['last_page'],1)),
                        guess=True,
                        stream=True,
                        pandas_options={'header': key['header']}
                        )
    df = pd.concat(df)
    df = df[[key['frame'], key['price']]]
    df.columns = ['frame', 'price']
    df['supplier'] = supplier
    return df

def omegaSpecific(supplier):
    key = supplier_dict[supplier]
    file_path = root + str(key['file_path'])
    df = tabula.read_pdf(file_path, 
                    pages=list(np.arange(key['first_page'],key['last_page'],1)),
                    guess=True,
                    stream=True,
                    pandas_options={'header': key['header']},
                    multiple_tables=False)
    df = pd.concat(df)

    # 2 tables on some pages, one on left, one on right
    df_left = df[[key['frame'],key['price']]]
    df_left.columns = ['frame', 'price']
    df_right = df[[key['frame1'], key['price1']]].dropna()
    df_right.columns = ['frame', 'price']
    df = pd.concat([df_left, df_right])
    df['supplier'] = supplier
    return df

def ampfSpecific(supplier):
    key = supplier_dict[supplier]
    file_path = root + str(key['file_path'])
    df = tabula.read_pdf(file_path, 
                    pages=list(np.arange(key['first_page'],key['last_page'],1)),
                    guess=True,
                    stream=True,
                    pandas_options={'header': key['header']},
                    multiple_tables=False)
    df = pd.concat(df)

    # 2 tables on some pages, one on left, one on right
    df_left = df[[key['frame'],key['price']]]
    df_left.columns = ['frame', 'price']
    df_right = df[[key['frame1'], key['price1']]].dropna()
    df_right.columns = ['frame', 'price']
    df = pd.concat([df_left, df_right])
    df['supplier'] = supplier
    return df


def globalSpecific(supplier):
    # for 'global metal' and 'global wood'
    key = supplier_dict[supplier]
    file_path = root + str(key['file_path'])
    df = tabula.read_pdf(file_path, 
                    pages=list(np.arange(key['first_page'],key['last_page'],1)),
                    guess=True,
                    stream=True,
                    pandas_options={'header':0},
                    multiple_tables=False)
    df = pd.concat(df)
    df.loc[len(df)] = df.columns
    df.columns = [0, 1, 2, 3 ,4]
    df = df[[key['frame'], key['price']]]
    df.columns = ['frame', 'price']
    df['supplier'] = supplier
    return df

def universalSpecific(supplier):
    key = supplier_dict[supplier]
    file_path = root + str(key['file_path'])
    df = tabula.read_pdf(file_path, 
                        pages=list(np.arange(key['first_page'],key['last_page'],1)),
                        guess=False,
                        stream=True,
                        pandas_options={'header': key['header']}
                        )
    df = pd.concat(df)
    df = df[[key['frame'], key['price']]]
    df.columns = ['frame', 'price']
    df['supplier'] = supplier
    return df

def fosterSpecific(supplier):
    key = supplier_dict[supplier]
    file_path = root + str(key['file_path'])
    df = tabula.read_pdf(file_path, 
                        pages=list(np.arange(key['first_page'],key['last_page'],1)),
                        guess=True,
                        stream=True,
                        multiple_tables=True,
                        pandas_options={'header': key['header']}
                        )
    df = pd.concat(df)

    # 3 tables on some pages, one on left, middle, right
    df_left = df[[key['frame'],key['price']]]
    df_left.columns = ['frame', 'price']
    df_mid = df[[key['frame1'], key['price1']]].dropna()
    df_mid.columns = ['frame', 'price']
    df_right = df[[key['frame2'], key['price2']]].dropna()
    df_right.columns = ['frame', 'price']
    df = pd.concat([df_left, df_mid, df_right])
    df['supplier'] = supplier
    return df

# Enter in the Json file and test
# print(fosterSpecific('foster').head(20))


# The suppliers
# print(supplier_excel_dict.keys())
