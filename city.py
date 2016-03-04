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
	#print(map)
	return map

def open_map(file_name):
	cityMap = read_file(file_name)
	clone = cityMap[:]

	solve_map(clone)




#--------------------------------------------



def solve_map(map):
	print ("Welcome to the new Montana Road Network")
	print ("1. Enter 1 to see how many cities are connected to a specific city")
	print ("2. Enter 2 to see if two cities have a direct connection")
	print ("3. Enter 3 to see if two cities have a connection")
	print ("4. Enter 4 to see if two cities have any connection")
	print ("5. Quit")


	userIn = input("Enter your choice: ")

	if (userIn == '1'):
		cityIn = input("Enter the city: ")
		print(find_city_num(map, cityIn))
	elif (userIn == '2'):
		city1In = input("First City: ")
		city2In = input("Second City:")
		find_edge(map, city1In, city2In)
	elif (userIn == '3'):
		city1In = input("First City: ")
		city2In = input("Second City: ")
		hopsIn = input("Hop connection: ")
		hop_connection(map, city1In, city2In, hopsIn)
	elif (userIn == '4'):
		city1In = input("First City: ")
		city2In = input("Second City: ")
		city_connection(map, city1In, city2In)
	else:
		print("quitting")


#Task 1. Number of cities directly connected to a query city.
#Complete!
def find_city_num(maps, city):
	count = 0;
	for map in maps:
		if map[0] == city or map[1] == city:
			count+=1

	return count

#Task 2. Given two query cities, return YES/NO for whether there is a direct
#connection (edge) between them.
def find_edge(maps, city1, city2):
	print("hi")

#Task 3. Given two query cities and an integer d, return YES/NO for whether there is a k-hop connection,
#k ≤ d, between them; if YES, print one solution out, to gether with the total distance of the d hops.
def hop_connection(maps, city1, city2, d):
	print("hi")

#Task 4. Given two query cities, return YES/NO for whether there is a connection (not necessarily direct)
#between them; if YES, print one solution out, together with the actual total distance of the connection.
def city_connection(maps, city1, city2):
	print("hi")





open_map("citymap.txt")