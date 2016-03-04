# Megan Weller
# Ashley Bertrand
# CSCI 338 Concepts
import re

def read_file(file_name):
    file = open(file_name, "r")
    line = file.readline().replace("-----------------------", "").replace("\t", "")    
    map = []
    
    while line:
        if (line == '\n'):  #we don't want to read in a blank line
            line = file.readline().replace("\t", " ").replace("-----------------------", "")
        else:
            line = line.strip() #strip unnessesary white space
            line = re.sub('\s\s+', ',', line)   #replace lone tabs with a comma
            fromCity, toCity, miles = line.split(',')  # splits line into list of tokens
            map.insert(0, (fromCity, toCity, miles))   # insert into the map
            
            line = file.readline().replace("\t", " ").replace("-----------------------", "")
       
        
    map.reverse()                # original order
    print(map)
    return map

def open_map(file_name):
    cityMap = read_file(file_name)
    clone = cityMap[:]

    solve_map(clone)




#--------------------------------------------



def solve_map(map):
    print ("I'm here")



open_map("citymap.txt")