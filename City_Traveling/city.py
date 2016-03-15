# Megan Weller
# Ashley Bertrand
# CSCI 305 Concepts
# Python 3.5.1

import re

def read_file(file_name):
	file = open(file_name, "r")
	line = file.readline().replace("-----------------------", "").replace("\t", "")    
	results = []
	
	while line:
		if (line == '\n'):  								#we don't want to read in a blank line
			line = file.readline().replace("\t", " ").replace("-----------------------", "")
		else:
			line = line.strip() 							#strip unnessesary white space
			line = re.sub('\s\s+', ',', line)   			#replace lone tabs with a comma
			fromCity, toCity, miles = line.split(',')  		#splits line into list of tokens
		
			if(miles != 'Miles'):							
				miles = int(miles)							#converting miles from strings to ints

			results.insert(0, (fromCity, toCity, miles))   	#insert into the map
			line = file.readline().replace("\t", " ").replace("-----------------------", "")
	   
		
	results.reverse()       #original order
	del results[0]			#removing "From, To, Miles"
	return results

def open_map(file_name):
	cityMap = read_file(file_name)
	clone = cityMap[:]
	print ("\nWelcome to the new Montana Road Network!")
	solve_map(clone)

#--------------------------------------------

def solve_map(results):
	#make a list of cities in database
	valid_cities = [toCity[0] for toCity in results]
	valid_cities = sorted(set(valid_cities))

	#continue prompt until '5' or invalid input
	while True:
		print ("\n1. Enter 1 to see how many cities are connected to a query city")
		print ("2. Enter 2 to see if two cities have a direct connection")
		print ("3. Enter 3 to see if two cities have a k-hop connection")
		print ("4. Enter 4 to get a connection path between two cities and the total distance")
		print ("5. Enter 5 to quit\n")

		userIn = input("Enter your choice: ")

		if (userIn == '1'):
			cityIn = input("Enter the city: ")
			print(find_city_num(results, cityIn))
		elif (userIn == '2'):
			city1In = input("First city: ")
			city2In = input("Second city: ")
			find_edge(results, city1In, city2In)
		elif (userIn == '3'):
			city1In = input("First city: ")
			city2In = input("Second city: ")
			hopsIn = input("Hop value: ")
			hop_connection(results, valid_cities, city1In, city2In, hopsIn)
		elif (userIn == '4'):
			city1In = input("First city: ")
			city2In = input("Second city: ")
			depth_first_helper(results, valid_cities, city1In, city2In)
		else:
			print("Goodbye!")
			break

#returns a given city's direct connections as a list
def get_connections(results, city):
	connections = []

	for result in results:
		if (result[0] == city):
			connections.insert(0, result[1])
		elif (result[1] == city and result[0] != city):
			connections.insert(0, result[0])

	connections.reverse()
	return connections

#returns the total distance across a path
def get_total_distance(results, path):
	total_distance = 0
	for index in range(len(path)):
		if(index+1 < len(path)):
			#summing distances between pairs of cities in path
			total_distance += get_distance(results, path[index], path[index+1])
			index+1
	return total_distance

#returns the distance between two cities
def get_distance(results, city1, city2):
	miles = 0
	for result in results:
		if (result[0] == city1 and result[1] == city2):
			miles = result[2]
		elif (result[0] == city2 and result[1] == city1):
			miles = result[2]
	return miles

#Task 1. Number of cities directly connected to a query city.
def find_city_num(results, city):
	count = 0
	for result in results:
		if result[0] == city or result[1] == city:
			count+=1

	return count

#Task 2. Given two query cities, return YES/NO for whether there is a direct
#connection (edge) between them.
def find_edge(results, city1, city2):
	miles = 0

	for result in results:
		if (result[0] == city1 and result[1] == city2):
			miles = result[2]
		elif (result[0] == city2 and result[1] == city1):
			miles = result[2]
	
	#distance between the same cities will be 0, but an edge exists, so YES is printed
	#distance between two cities is greater than 0, so a direct edge exists
	if(city1 == city2 or miles != 0):
		print("YES")
		return True
	else:
		print("NO")
		return False

#Task 3. Given two query cities and an integer d, return YES/NO for whether there is a k-hop connection,
#k ≤ d, between them; if YES, print one solution out, together with the total distance of the d hops.
def hop_connection(results, valid_cities, city1, city2, d):
	#converting d from string to int
	d = int(d)

	#ensuring that a valid value for d was entered
	if d < 1:
		print("The number of hops must be greater than 0.")
		return

	#invalid inputs
	if(city1 not in valid_cities and city2 not in valid_cities):
		print(city1, "and", city2, "are not in the database.")
		return
	if(city1 not in valid_cities):
		print(city1, "is not in the database.")
		return
	if(city2 not in valid_cities):
		print(city2, "is not in the database.")
		return

	#distances must be non-zero to be included in k-hop definition
	if city1 == city2:
		print(city1, "is 0 miles from itself. In order to fit the k-hop definition, distance must be greater than 0 miles.")
		return

	#a direct connection exists
	if (find_edge(results, city1, city2)):
		print(city1, ",", city2)
		print(get_distance(results, city1, city2), "miles")
		return

	#contine with Task 3 here...

#Task 4. Given two query cities, return YES/NO for whether there is a connection (not necessarily direct)
#between them; if YES, print one solution out, together with the actual total distance of the connection.
def depth_first_helper(results, valid_cities, start_city, end_city):
	stack = []
	visited = []
	first = start_city

	#invalid inputs
	if(start_city not in valid_cities and end_city not in valid_cities):
		print(start_city, "and", end_city, "are not in the database.")
		return
	if(start_city not in valid_cities):
		print(start_city, "is not in the database.")
		return
	if(end_city not in valid_cities):
		print(end_city, "is not in the database.")
		return

	adj_cities = get_connections(results, start_city)
	depth_first_search(results, start_city, end_city, adj_cities, stack, visited, first)

def depth_first_search(results, start_city, end_city, adj_cities, stack, visited, first):
	#start_city is visited
	visited.append(start_city)

	#end_city is discovered
	if(end_city in visited): 
		#if last city in stack is end_city
		if (stack[-1] == end_city):
			#full valid path
			stack.insert(0, first)
			print("YES")
			print(*stack, sep=', ')
			print(get_total_distance(results, stack), "miles")
		return stack

	#add adj_city to stack to keep track of that path to the end_city
	for adj_city in adj_cities:
		if adj_city not in visited:
			stack.append(adj_city)
			adj_cities = get_connections(results, adj_city)
			depth_first_search(results, adj_city, end_city, adj_cities, stack, visited, first)

open_map("citymap.txt")