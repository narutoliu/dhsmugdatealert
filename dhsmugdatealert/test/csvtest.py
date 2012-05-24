import csv
import sys

read=csv.reader(open("haha.csv", "r"), delimiter = ",", skipinitialspace=True)
read2=csv.reader(open("testdate.csv", "r"), delimiter = ",", skipinitialspace=True)
def subcheck(name):
    
    checker=False
    for row in read:
        if row[0]==name:
            user=row
            checker=True
    
    time=[]
    if checker:
        for test in read2:
            if test:
               for i in user[5:-2]:
                   if test[0]==i:
                       paper=test[1]
                       date=test[2]
                       time=test[3]
                       gg=True
    if checker==False:
        print ('gg')

    print (paper,date,time)

subcheck('liu.fengyuan')
                      
           


    

