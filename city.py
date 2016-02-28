# Megan Weller
# Ashley Bertrand
# CSCI 338 Concepts

def read_file(file_name):
    file = open(file_name, "r")
    next_line = file.readline()
    map = []
    
    while next_line:
        travels = next_line.split()  # splits line into list of tokens
        fromCity = (travels[0])  
        toCity = (travels[1])     
        miles = (travels[2]) 
        map.insert(0, (fromCity, toCity, miles))
        next_line = file.readline()
        
    map.reverse()                # original order
    return map

def open_map(file_name):
	cityMap = read_file(file_name)
	clone = cityMap[:]

	solve_map(clone)


open_map("citymap.txt")

#--------------------------------------------



def solve_map(map):
	print ("I'm here")