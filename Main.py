import matplotlib.pyplot as plt
import scipy
import numpy as np
import csv
import os
import pandas as pd 

#----------------------GLOBAL VARIABLES------------------------
cross_sectional_area = 10.176
gauge_length = 9.53

def new_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Folder %s created!" % dir_name)
    else:
        print("Folder %s already exists" % dir_name)

def read_csv(csv_name):
    #this function will process the force displacement data in the named CSV file into an array

    #--------------INPUTS--------------------------------------------------------------------------------------
    #csv_name: the name of the CSV file that you want to read (**IMPORTANT: MUST BE IN THE SAME FOLDER AS MAIN**)
    global active_name
    active_name = csv_name
    #----------------------------------------------------------------------------------------------------------

    fileName = csv_name+".csv"
    new_directory(active_name)

    line_count = 0
    temp_displacement = []
    temp_force = []
    e_array = []

    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        sinusoid_count = 1 
        for row in csv_reader:            
            if line_count == 0:
                pass
            else:
                definer = list(row[1]) 
                if sinusoid_count<10:
                    cycle = definer[2]
                    curr_sin = int(definer[0])
                else:
                    cycle = definer[3]
                    curr_sin = int(definer[0]+definer[1])
                #cycle will define whether we're in Preload ("P"), Stretch ("S"), or Recovery ("R")

                if cycle == "P" or cycle == "R":
                    pass
                else:
                    #now we've determined we are in a stretch phase 
                    if curr_sin==sinusoid_count:
                        temp_displacement.append(float(row[4]))
                        temp_force.append(float(row[5]))
                        #add the force and displacement to the temp arrays
                    else:
                        #we're on a new sinusoid
                        e_array.append(find_e(temp_force, temp_displacement, sinusoid_count))
                        sinusoid_count = sinusoid_count+1
                        temp_displacement = []
                        temp_force = []
                        #so append the two arrays to our bigger array, empty them, and start brand new
                        #and then increment sinusoid_count                
            line_count += 1
        #need this one more time to account for final sinusoid
        e_array.append(find_e(temp_force, temp_displacement, sinusoid_count))

        print(f'Processed {line_count} lines.')
        e_array.insert(0,"Youngs Modulus for Sinuoids")
        pd.DataFrame(e_array).to_csv(active_name+"/"+active_name+'youngs modulus.csv')    

def find_e(force, displacement, sinusoid_count):
    #this function will process the force displacement data in the two arrays and return youngs modulus

    #--------------INPUTS----------------
    #force: an array of doubles represeting force in newtons
    #displacement: an array of doubles representing displacement in mm
    #------------------------------------
    stress_array = []
    strain_array = []

    #find stress: force/cross sectional area
    #find strain: displacement/gauge length

    for i in range (len(displacement)):
        stress = displacement[i]/cross_sectional_area
        stress_array.append(stress)
    for i in range (len(force)):
        strain = force[i]/gauge_length
        strain_array.append(strain)

    stress_strain_plot(stress_array, strain_array, sinusoid_count)
    res = scipy.stats.linregress(stress_array, strain_array)

    print("Youngs modulus for sinusoid cycle", sinusoid_count, "is", float(res[0]))
    return float(res[0])

def stress_strain_plot(stress, strain, sinusoid_count):
    
    plt.plot(strain, stress)
    plt.ylabel("Stress")
    plt.xlabel("Strain")
    plt.title("Stress-Strain Curve for Sinusoid Repetition #"+str(sinusoid_count))
    #save the plot
    plt.savefig(active_name+"/"+str(sinusoid_count)+".png")    
    plt.clf()


def main():  
    read_csv("20minuteCure_Sinuoid013Data")

main()

