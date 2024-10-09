import chardet

# check file encoding
with open('online_retail_II_2009_2010.csv', 'rb') as f:
    result = chardet.detect(f.read())
    print(result)