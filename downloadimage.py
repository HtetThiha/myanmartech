# import pandas as pd
# data = pd.read_csv("images.csv")
# data
# data[['id','images']]
# type(data)
# type(data[['id','images']])


from csv import reader
import wget
import os

# open file in read mode
with open('collections2_images.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
#         print("id is "+row[0])
#         print("link is "+row[1])
#         id 
#         x = row[1].split(;)
        
        id = row[0]
        links = row[1].split(";")
        del links[0]
        index = 1
        
        try:
            os.makedirs('/home/hlthiha/Desktop/mmnewsextracts/collectionimages/'+ str(id))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        for l in links:
            wget.download(l, '/home/hlthiha/Desktop/mmnewsextracts/collectionimages/'+ str(id) + '/'+ str(index)+'.jpg')
            index += 1

# from csv import reader
# # iterate over each line as a ordered dictionary and print only few column by column Number
# with open('students.csv', 'r') as read_obj:
#     csv_reader = reader(read_obj)
#     for row in csv_reader:
#         print(row[1], row[2])