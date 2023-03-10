# -*- coding: utf-8 -*-
"""HandWriting_Detection_Capital_Letters

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1thTYiQOw1Ka8E27z7m0BsFCmh-ec0hgx

First of all giving permission to google colab so that it can access the files
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/drive')
# %cd /content/drive/MyDrive

import csv

"""Reading the data

"""

#Dividing the data in test and training data but first getting total number of rows, then only adding 90% of it to training data.
data=[]
number_of_rows=0
with open('A_Z Handwritten Data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      number_of_rows+=1
      data.append(list(row))

"""Segregating the data"""

# segregating the read data
# train_data=[]
# test_data=[]
# counter=0
# for i in data:
#   counter+=1
#   if counter<=(0.9*number_of_rows):
#     train_data.append(i)
#   else: 
#     test_data.append(i)

#THIS IS COMMENTED OUT FOR THE REASON EXPLAINED IN BELOW COMMENTS

# #Now the next step is to calculate p(y=k) where k belongs to [0,25]
# dict1={}
# counter_list=[]  
# #will store the first column of each row and then we will use counter to count number of times a particular one appears and then divide by total number to get probability by favourable/total

# for i in train_data:
#   counter_list.append(i[0])

# #Now our next step is to assign the number and the probability of each as key value pair in dictionary, we are using dictionary because it uses hash mapping ang take less time to fetch data
# counter_set=set(counter_list)   #just to remove the duplicates and see all the labels that have been covered in the training data
# print(counter_set)
# #OUTPUT=['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '3', '4', '5', '6', '7', '8', '9']
# #so we can see if we use training data then not all the labels between 0 to 25 are covered. So for calculating P(Y=k) we need to first shuffle the data and then segregate it and that's why above part was commented out

import random
random.shuffle(data)

#segregating the read data
train_data=[]
test_data=[]
counter=0
for i in data:
  counter+=1
  if counter<=(0.9*number_of_rows):
    train_data.append(i)
  else: 
    test_data.append(i)

"""Calculation P(Y=k)"""

#Now the next step is to calculate p(y=k) where k belongs to [0,25]
dict1={}
counter_list=[]  
dict1_counter={}
#will store the first column of each row and then we will use counter to count number of times a particular one appears and then divide by total number to get probability by favourable/total

for i in train_data:
  counter_list.append(i[0])

#Now our next step is to assign the number and the probability of each as key value pair in dictionary, we are using dictionary because it uses hash mapping ang take less time to fetch data
counter_set=set(counter_list)   #just to remove the duplicates and see all the labels that have been covered in the training data. These will help in adding keys to the dictionary

#Calculating P(y=k) and adding to dictionary
for i in counter_set:
  probability_count=counter_list.count(i)
  dict1[i]=probability_count/len(train_data)
  dict1_counter[i]=probability_count

print(dict1)

"""Addressing the problems of creation of bins, initially taking it be bin size of 8. """

bin_dict={}  #again using dictionary for associating

bin_size=8

key=0
for i in range(0,256):
  if 32*key<=i and i<32*(key+1):
    bin_dict[i]=key
  else:
    bin_dict[i]=key+1 #because otherwise numbers such as 32,64 where if statements are not satisfied would never be added to dictionary.
    key+=1
#so we are creating a bin size of 8 i.e. all the pixels which were taking values between 0 to 255 will now be scaled down to take values between 0 to 7
#so that means the scaling will take 32 numbers at a time to divide 256 over 8 parts, so numbers in range 0 to 31 will come to 0 then between 32 to 63 to 1 and so on...

print(bin_dict)

"""Now once we have done this we need to change all the data in our training set according to our bin size."""

#so in the train_data list each element is a list which has 785 entries where the first entry is the label and remaining 784 as pixels and we can verify that
print(len(train_data[1]))

#so to convert all 784 pixels according to our bin size, we will take all data by iterating through them and replace them with their corresponding value in the bin dictionary

for i in train_data:
  for j in range(1,785): #starting from index 1 as index 0 is label and we only need to change the pixel data
    i[j]=bin_dict[int(i[j])]

"""Now we need to find P(Xi=Xit|Y=k) for all data points i.e. for all 784 pixels over all the data."""

Xi_dict={}  
#this dictionary would store the above values and the keys would be a tuple containing the values of Xi and k and i which is the label of pixel i.e. out of 0 to 784, so in this dictionary probability would be associated as key=(i,Xit,k) and value=P(Xi=Xit|Y=k)

"""In this procedure for calculating the probability for each and every data point so it is 784 pixel points for almost 25000 rows, and each of this data point will be counted multiple times just to check how many times a particular value of a particular pixel point occurs to calculate probability, and infact searching for the value itself in the given list. So to reduce the iteration time we are converting the training data into a dictionary rather than a list. 

So how is this dictionary made, so dictionary has 26 keys which is from 0 to 25, which are labels that are given to each row. Now each label appears multiple times in the given data, and dictionary doesn't allow duplicates. So how will we store multiple data for the same label?

Well for dealing with that we have a clever trick, we will make use of nested lists. Which value of each key is a list and this list contains elements which are also list. Now what is the data stored in this list so actually every time a label repeats in the training data it has 784 pixels associated with it. So the list inside the list contains the data of this 784 pixels and there are many lists inside this main lists as many times the label is repeated to store the data every time the label is repeated.

So dictionary reduces this time because dictionary makes use of hash mapping so searching for a particular element in dictionary takes constant time which is much less than that of list.
"""

train_data_dict={}
for i in range(0,26):
  list2=[]
  for j in train_data:
    if int(j[0])==i:
      list1=[]
      for k in range(1,785):
        list1.append(j[k])
      list2.append(list1)
    else:
      continue
  train_data_dict[i]=list2

print(len(train_data_dict[0][0]))

#we also need to create a special counter function
def counter(i,xi,k):    #i=>Which pixel I am talking about, Xi=>what is the value of the pixel, and for which Y=k
  count=0
  for j in train_data_dict[k]:
    if int(j[i])==xi:
      count+=1
    else:
      continue

  return count

print(counter(0,0,0))

#And also a probability function to calculate to calculate P(xi=Xit|Y=k)

def probability(i,xi,k):     #i=>Which pixel I am talking about, Xi=>what is the value of the pixel, and for which Y=k

  if xi>7 or xi<0: 
      print("Enter a valid pixel value")
      return 
  if k>25 or k<0:
      print("Enter a valid label")
      return
    
  else:   #Calculating using the formula P(Xit=Xi|Y=k)=P(Xit=Xi and Y=k)/P(Y=k)
    prob1=(counter(i,xi,k)+1)/((dict1_counter[str(k)])) #calculating P(Y=k and Xit=Xi)
    # prob=prob1/float(dict1[str(k)])
    return prob1

print(probability(0,7,0))

"""Now our first instinct is to calculate the probability of all possible value of each data point such as 

for k in range(0,26):
  for j in train_data_dict[k]:
    for i in range(0,784):
      Xi_dict[(j[i],k)]=probability(i,j[i],k)

So what is our idea here is that we go to each value of each pixel and calculate how many times the same value for the same pixel corresponding to the same label. And we do it for each of the 26 label for each of the 784 pixels and for each row in the data (which are about 25000), so overall 26 x 784 x 25000, one might think this manageable but we are missing out on a point, the probability function calls couter functions which again iterates through entire data. 
So it is actually 26x784x25000x25000 iterations which can't be completed in given possible time constraints.

So how to reduce this?
"""

for k in range(0,26):
    for i in range(0,784):
      for j in range(0,bin_size):
        Xi_dict[(i,j,k)]=probability(i,j,k)

print(Xi_dict)

"""Above is the solution we came up with, so we know that in the probability function the entire data will be scanned given the label, value of pixel and pixel number. SO we don't need to iterate through the entire data again in our loops, instead what we do is something much more clever.

We know each pixel can take values between 0 to bin_size-1. So instead of iterating through the whole data manually, going to each pixel point then seeing which value it takes then calculating the probability for that value. What we do is that we calculate the porbability of each possible value of each pixel point. 

So instead of getting the value by iterating for whole data, we are giving it all possible values to each and every data point. 
Which reduce number of iterations to 26 x 784 x 8 x 25000.

And we are sure that all pixel points will be covered in the data by the first two loops. Because fofr given label and pixel number our counter function will iterate through all rows for counting the corresponding. 

So just manually giving the value decreases number of iterations significantly.
"""

print(Xi_dict[(200,6,22)])

s=0
for i in range(0,784):
  for k in range(0,bin_size):
    s=s=Xi_dict[(i,k,2)]
print(s)

"""Predicting the data"""

import math

"""So smoothing process, involves dealing with mathematical domain error which is that the probability for some labels probability of pixel attaining some values is 0 and therefore while taking log (which turns amll number into large number to make comparisons easier ) or by dividing we are getting division by 0. 

So what we do is that we add 1 in the numerator and proportionaly the bin_size in the denominator. Why is bin_size proportional to 1? Well in numerator we are finding data wrt single label, and we are adding 1 to make it non zero, but then in denominator we are taking total probability of same data over all label, so each label will have a corresponding 1 added to it, to make the assumpltion hold, and since it is total probability in the denominator therefore all labels will be added, there for 1 will be added as many times as the total number of labels which is nothing but bin_size.

Now what is the need of log in the numerator, well our number would be too small in both numerator and denominator to lead any significant result there it is important. 

Also why are we adding math.log term, whereas we can mutiply whole probability and do log in end, and by properties of log it will lead the same thing at the end, well that is where the complication arise. In multiplication even when 0 is encountered a single time it will make the whole term 0 and so we won't get any significant result, but in addition this problem this should have been resolved, as even when even a single one is 0 then also whole term won't be affected. Well, yeah but that leads to another issue, i.e. now log will get input as 0. So a jugaad logic to deal with this is that we add 1 to each probability value, which is not mathematically valid, but it gives us answers with very low accuracy. So we need to find something to avoid this on it's whole.
"""

def probability_func(x,k):
  prob=math.log(float(dict1[str(k)]))
  for i in range(0,784):
    prob=prob+math.log(float(Xi_dict[((i),int(x[i]),k)]))

  # prob3=0
  # for j in range(0,26):
  #   prob2=math.log(float(dict1[str(j)]))
  #   for i in range(0,784):
  #     prob2=prob2+math.log(float(Xi_dict[((i),int(x[i]),j)])+1)
  #   prob3=prob3+prob2

  return prob

"""The denominator for all the terms is fixed and therefore there is no need to include it in the final answer.

So the earlier issue with smoothing was that, when we were mutliplying the terms in the numerator directly, then even if one of the pixel had probability as zero for corresponding label and pixel value (which obviously be true for some pixel in each rwo of data for a particular value and particular label) then the whole product goes to 0.

Then we tried taking the log and converting multiplication to addition, but then the log was getting 0 as input and that was wrong too. So we addded one in each probability value at this statement 

prob=prob+math.log(float(Xi_dict[((i),int(x[i]),k)] +1))

But that didn't help with the accuracy either because its mathematically incorrect, because adding 1 to a smaller than 1 number increases the error significantly. 

So what we tried to do is that instead of adding 1 here, we added one to the value given by the counter(i,j,k) function before calculating its probability in the probability function used for Xi_dict. So adding 1 here was useful because here even if counter is 0 adding 1 will make the probability non-zero. 

And since denominator, after division the error would be negligible. 

So this is the solution to the error. 
"""

def index(y,sample_list):
  for i in range(0,len(sample_list)):
    if sample_list[i]==y:
      return i

def predict(data):
  list1=[]
  for i in range(0,26):
    list1.append(probability_func(data,i))
  return index(max(list1),list1)

#so to convert all 784 pixels according to our bin size, we will take all data by iterating through them and replace them with their corresponding value in the bin dictionary

for i in test_data:
  for j in range(1,785): #starting from index 1 as index 0 is label and we only need to change the pixel data
    i[j]=bin_dict[int(i[j])]

test_data_dict={}
for i in range(0,26):
  list2=[]
  for j in test_data:
    if int(j[0])==i:
      list1=[]
      for k in range(1,785):
        list1.append(j[k])
      list2.append(list1)
    else:
      continue
  test_data_dict[i]=list2

"""So now we can see that if we don't do smoothing then we are getting division by 0."""

# count=0
# for k in range(0,26):
#   for i in test_data_dict[k]:
#     if(predict(i))==k:
#       count+=1
#     else:
#       continue
# print(count/len(test_data))

# accuracy=(count/len(test_data))*100
# print("Accuracy=%s percent"%accuracy)

"""Now once we have trained our machine also tested the data, let's begin to take input and detect the handwriting. But first we need to take a data which will be used to resize it to the size with which our algorithm can function. We can later optimize it, but for a really large value it won't work unless we drastically increase the running time.

Started reading the image converting it to black and white and storing pixel value for reading data but for some reason all values are turning out be around 255 which is an issue. Will look into it soon.
"""

from PIL import Image
import os

def resize(img_path):
  image=Image.open('%s'%img_path)
  new_image=image.resize((28,28))
  new_image.save('resized_img.png')
  return os.path.abspath('resized_img.png')

print(resize(r'Screenshot_1.png'))

import cv2

def image_processing(pth):
  data=[]
  final_pth=resize(pth)
  img_rgb = cv2.imread('%s'%final_pth)
  img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
  for i in range(0,28):
    for j in range(0,28):
      data.append(img_gray[i][j])

  for i in range(0,len(data)):
     data[i]=bin_dict[data[i]]

  x=predict(data)
  return x

alphabet_dict={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

print(alphabet_dict[image_processing('Screenshot_7.png')])