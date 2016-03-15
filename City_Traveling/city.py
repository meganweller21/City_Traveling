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
			print(find_edge(results, city1In, city2In))
		elif (userIn == '3'):
			city1In = input("First city: ")
			city2In = input("Second city: ")
			hopsIn = input("Hop value: ")
			hops(results, city1In, city2In)
		elif (userIn == '4'):
			city1In = input("First city: ")
			city2In = input("Second city: ")
			depth_first_helper(results, city1In, city2In, valid_cities)
		else:
			print("Goodbye!")
			break

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
	
	if(miles != 0):
		return "YES"
	else:
		return "NO"

#returns a given city's direct connections
def get_connections(results, city):
	connections = []

	for result in results:
		if (result[0] == city):
			connections.insert(0, result[1])
		elif (result[1] == city and result[0] != city):
			connections.insert(0, result[0])

	connections.reverse()
	return connections

#Task 3. Given two query cities and an integer d, return YES/NO for whether there is a k-hop connection,
#k ≤ d, between them; if YES, print one solution out, together with the total distance of the d hops.
def hop_connection(results, valid_cities, city1, city2, d):
	#invalid inputs
	if(city1 not in valid_cities and city2 not in valid_cities):
		print("Provided cities are not in the database")
		return
	if(city1 not in valid_cities):
		print("First city is not in the database")
		return
	if(city2 not in valid_cities):
		print("Second city is not in the database")
		return

def hops(start, end, hops):
    start = ord(start.upper())
    end = ord(end.upper())
    distance = end - start + 1
    if abs(distance) <= hops:
        if distance > 0:
            path = range(start, end + 1)
        else:
            path = list(range(end, start + 1))[::-1]
        print(", ".join(chr(c) for c in path))
    else:
        print("No connection.")

#Task 4. Given two query cities, return YES/NO for whether there is a connection (not necessarily direct)
#between them; if YES, print one solution out, together with the actual total distance of the connection.
def city_connection(results, valid_cities, city1, city2):
	#invalid inputs
	if(city1 not in valid_cities and city2 not in valid_cities):
		print(city1, "and", city2, "are not in the database")
		return
	if(city1 not in valid_cities):
		print(city1, "is not in the database")
		return
	if(city2 not in valid_cities):
		print(city2, "is not in the database")
		return

	#alphabetize city inputs to make runtime possible
	switched = False
	temp = city1
	cities = [city1, city2]
	cities.sort()
	city1 = cities[0]
	city2 = cities[1]

	#final path must be reversed
	if temp != city1:
		switched = True

	paths = [[0, city1]]
	found = True

	#direct connections
	for result in results:
		if((result[0] == city1 and result[1] == city2) or (result[0] == city2 and result[1] == city1)):
			print("YES")
			print(city1, ",", city2)
			print(result[2], "miles")
			return

	#indirect connections
	while found:
		found = False
		for first, second, weight in results:
			for path in paths:
				candidate = None
				#found a new link in path
				if (first in path) and (second not in path):
					candidate = second
				elif (first not in path) and (second in path):
					candidate = first
				#build a path
				if candidate:
					new_path = list(path)
					new_path.append(candidate)
					new_path[0] += weight
					#unique list of paths
					if new_path not in paths:
						paths.append(new_path)

				#found a valid path
				if city2 in path:
					found = True
					#save distance
					distance = path[0]
					del path[0]
					
					#order of input cities was switched
					if(switched):
						path.reverse()

					print("YES")
					print(*path, sep=', ')
					print(distance, "miles")
					return
	
	#no connections
	print("NO")

def depth_first_helper(results, start_city, end_city, valid_cities):
	stack = []
	visited = []
	first = start_city

	#invalid inputs
	if(start_city not in valid_cities and end_city not in valid_cities):
		print(start_city, " and ", end_city, " are not in the database")
		return
	if(start_city not in valid_cities):
		print(start_city, " is not in the database")
		return
	if(end_city not in valid_cities):
		print(end_city, " is not in the database")
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

def get_total_distance(results, path):
	total_distance = 0
	for index in range(len(path)):
		if(index+1 < len(path)):
			#summing distances between pairs of cities in path
			total_distance += get_distance(results, path[index], path[index+1])
			index+1
	return total_distance

def get_distance(results, city1, city2):
	for result in results:
		if (result[0] == city1 and result[1] == city2):
			miles = result[2]
		elif (result[0] == city2 and result[1] == city1):
			miles = result[2]
	return miles

open_map("citymap.txt")