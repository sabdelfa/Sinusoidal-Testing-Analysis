import matplotlib
import scipy
import numpy as np
import csv
# this is my edit
def read_csv(csvName):
    #this function will process the force displacement data in the named CSV file into an array

    #--------------INPUTS----------------
    #csvName: the name of the CSV file that you want to read (**IMPORTANT: MUST BE IN THE SAME FOLDER AS MAIN**)
    #------------------------------------
    line_count = 0
    with open(csvName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        sinusoid_count = 1 
        e_array = []
        print("check one")
        for row in csv_reader:            
            if line_count == 0:
                print("check two")
                print(row)
            else:
                definer = list(row[1]) #at index 1 we expect to see a string of the form int_word (e.g. 1_Stretch), but we only care if it is int_"stretch"
                #that is going to give us a character array "1","_","S","t","r","e","t","c","h"
                #definer[0] will tell us which cycle we're in (1-20)
                #definer[2] will be either S (we want this data) or P or R (we dont want this data)
                if definer[2] == "P" or definer[2] == "R":
                    print("check three")
                else:
                    #now we've determined we are in a stretch phase 
                    print("check four")
                    temp_displacement = []
                    temp_force = []
                    if definer[0]==sinusoid_count:
                        temp_displacement.append(row[4])
                        temp_force.append(row[5])
                        #add the force and displacement to the temp arrays
                    else:
                        #we're on a new sinusoid
                        #find_e(temp_displacement, temp_force)
                        e_array.append(line_count)
                        sinusoid_count = sinusoid_count+1
                        #so append the two arrays to our bigger array, empty them, and start brand new
                        #and then increment sinusoid_count
            line_count += 1
        print(f'Processed {line_count} lines.')
        print(e_array)

def find_e(force, displacement):
    #this function will process the force displacement data in the two arrays and return youngs modulus

    #--------------INPUTS----------------
    #force: an array of doubles represeting force in newtons
    #displacement: an array of doubles representing displacement in mm
    #------------------------------------
    return 7

def main():
    read_csv("20minuteCure_Sinuoid013Data.csv")

main()

#end goal:
#1: read the file and get an array of arrays [[displacement@]]
