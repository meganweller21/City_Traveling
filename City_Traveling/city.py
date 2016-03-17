# Megan Weller
# Ashley Bertrand
# CSCI 305 Lab 2
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
		print ("\n1. Enter 1 to see how many cities are connected to a query city.")
		print ("2. Enter 2 to see if two cities have a direct connection.")
		print ("3. Enter 3 to see if two cities have a k-hop connection.")
		print ("4. Enter 4 to get a connection path between two cities and the total distance.")
		print ("5. Enter 5 to quit.\n")

		userIn = input("Enter your choice: ")

		if (userIn == '1'):
			cityIn = input("Enter the city: ")
			task1(results, cityIn)
		elif (userIn == '2'):
			city1In = input("Start city: ")
			city2In = input("Destination city: ")
			task2(results, city1In, city2In)
		elif (userIn == '3'):
			city1In = input("Start city: ")
			city2In = input("Destination city: ")
			hopsIn = input("Hop value: ")
			task3(results, valid_cities, city1In, city2In, hopsIn)
		elif (userIn == '4'):
			city1In = input("Start city: ")
			city2In = input("Destination city: ")
			task4(results, valid_cities, city1In, city2In)
		else:
			print("\nGoodbye!")
			break

#Task 1. Number of cities directly connected to a query city.
def task1(results, city):
	count = 0
	for result in results:
		if result[0] == city or result[1] == city:
			count+=1
	print()
	print(count)

#Task 2. Given two query cities, return YES/NO for whether there is a direct
#connection (edge) between them.
def task2(results, city1, city2):
	miles = 0

	for result in results:
		if (result[0] == city1 and result[1] == city2):
			miles = result[2]
		elif (result[0] == city2 and result[1] == city1):
			miles = result[2]
	
	#distance between two cities is greater than 0, so a direct edge exists
	if(miles != 0):
		print("\nYES")
		return True
	else:
		print("\nNO")
		return False

#Task 3. Given two query cities and an integer d, return YES/NO for whether there is a k-hop connection,
#k ≤ d, between them; if YES, print one solution out, together with the total distance of the d hops.
def task3(results, valid_cities, city1, city2, d):
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

	#implies there must be a direct connection
	if d == 1:
		if(find_edge(results, city1, city2)):
			print("\nYES")
			print(city1, ",", city2)
			print(get_distance(results, city1, city2), "miles")
			return
		else:
			print("\nNO")
			return

	#a direct connection exists
	if(find_edge(results, city1, city2)):
		print("\nYES")
		print(city1, ",", city2)
		print(get_distance(results, city1, city2), "miles")
		return
	#no connection exists in the given number of hops
	elif(d < get_min_hops(results, valid_cities, city1, city2)):
		print("\nNO")
		return
	#at least one connection exists in the given number of hops
	else:
		dijkstra(results, valid_cities, city1, city2, visited=[], distances={}, predecessors={})
		return

#Task 4. Given two query cities, return YES/NO for whether there is a connection (not necessarily direct)
#between them; if YES, print one solution out, together with the actual total distance of the connection.
def task4(results, valid_cities, city1, city2):
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

	#distances must be non-zero for a connection to exist
	if city1 == city2:
		print(city1, "is 0 miles from itself. No connection exists.")
		return

	#a direct connection exists
	if(find_edge(results, city1, city2)):
		print("\nYES")
		print(city1, ",", city2)
		print(get_distance(results, city1, city2), "miles")
		return
	#looking for a connection
	elif(is_connection(results, valid_cities, get_index_from_city(valid_cities, city1), get_index_from_city(valid_cities, city2))):
		dijkstra(results, valid_cities, city1, city2, visited=[], distances={}, predecessors={})
		return
	else:
		print("\nNO")
		return

#same function as task2 except nothing gets printed
def find_edge(results, city1, city2):
	miles = 0

	for result in results:
		if (result[0] == city1 and result[1] == city2):
			miles = result[2]
		elif (result[0] == city2 and result[1] == city1):
			miles = result[2]
	
	#distance between two cities is greater than 0, so a direct edge exists
	if(miles != 0):
		return True
	else:
		return False

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

#uses depth first search and returns true if there is a connection between two cities
def is_connection(results, valid_cities, i, j):
	start_city = get_city_from_index(valid_cities, i)
	end_city = get_city_from_index(valid_cities, j)

	stack = []
	visited = []

	#push start_city onto stack
	stack.append(start_city)

	#while stack is not empty
	while(stack):
		#current is top of stack
		current = stack[-1]

		#pop from stack
		del stack[-1]
		
		if (current in visited):
			continue
		
		#mark current as visited
		visited.append(current)
		adj_cities = get_connections(results, current)

		#push adjacent cities onto stack
		for adj_city in adj_cities:
			stack.insert(0, adj_city)

	#found a path
	if end_city in visited:
		return True
	else:
		return False

#returns a city's corresponding index
def get_index_from_city(valid_cities, city):
	i = 0
	for valid_city in valid_cities:
		if(valid_city == city):
			return i
		i = i + 1
	return -1

#returns an index's corresponding city
def get_city_from_index(valid_cities, index):
	for i in range(len(valid_cities)):
		if(i == index):
			return valid_cities[i]
	return "Error"

#returns true if there is a direct connection between cities
def is_direct(results, valid_cities, i, j):
	city1 = get_city_from_index(valid_cities, i)
	city2 = get_city_from_index(valid_cities, j)
	if find_edge(results, city1, city2):
		return True
	else:
		return False

#weight of connection is returned
def get_weight_of_connection(results, valid_cities, i, j):
	if is_direct(results, valid_cities, i, j):
		return 1
	#dummy value that represents the number of hops between city i and city j
	if is_connection(results, valid_cities, i, j):
		return 99
	return 0

#Dijkstra's Algorithm to find the shortest path
def dijkstra(results, valid_cities, start_city, end_city, visited=[], distances={}, predecessors={}):
	#end condition
	if start_city == end_city:
		path = []
		previous = end_city
		
		#build shortest path
		while previous != None:
			path.append(previous)
			previous = predecessors.get(previous, None)

		path.reverse()
		print("\nYES")
		print(*path, sep=', ')
		print(get_total_distance(results, path), "miles")
	else:     
		#initializes start distance to 0
		if not visited: 
			distances[start_city] = 0

		#visit the adjacent cities
		adj_cities = get_connections(results, start_city)
		for adj_city in adj_cities:
			if adj_city not in visited:
				new_distance = distances[start_city] + 1
				if new_distance < distances.get(adj_city, float('inf')):
					distances[adj_city] = new_distance
					predecessors[adj_city] = start_city
		
		#mark start_city as visited
		visited.append(start_city)
		
		#select the non visited node with lowest distance
		unvisited={}
		for valid in valid_cities:
			if valid not in visited:
				unvisited[valid] = distances.get(valid, float('inf')) 
		new_start = min(unvisited, key = unvisited.get)

		#recursive call on new_start
		dijkstra(results, valid_cities, new_start, end_city, visited, distances, predecessors)

#used where there is not a direct path between two vertices
infinity = 1000000

#returns the minimum number of hops required between two cities
def get_min_hops(results, valid_cities, start_city, end_city):
	print("\nPlease be patient while I find your results. It may take a minute...")

	distances = []		#list of ints
	shortest = []		#list of bools (true if vertex is in shortest path or if shortest distance is finalized)
	num_verticies = len(valid_cities)

	#initializing lists
	for index in range(num_verticies):
		distances.append(infinity)
		shortest.append(False)

	#distances at start_city is 0
	distances[get_index_from_city(valid_cities, start_city)] = 0

	#updating distance is path to j through shortest_vertex is smaller
	for i in range(num_verticies - 1):
		shortest_vertex = shortest_distance(valid_cities, distances, shortest)
		shortest[shortest_vertex] = True
		for j in range(num_verticies):
			if((not shortest[j]) and 
				(is_connection(results, valid_cities, shortest_vertex, j)) and 
				(distances[shortest_vertex] != infinity) and 
				((distances[shortest_vertex] + (get_weight_of_connection(results, valid_cities, shortest_vertex, j)) < distances[j]))):
				distances[j] = (distances[shortest_vertex] + (get_weight_of_connection(results, valid_cities, shortest_vertex, j)))
			j = j + 1
		i = i + 1

	#minimum number of hops required between start_city and end_city
	min_hops = distances[get_index_from_city(valid_cities, end_city)]

	return min_hops

#finding the minimum distance vertex
def shortest_distance(valid_cities, distances, shortest):
	shortest_path = infinity
	shortest_vertex = -1

	#finding the smallest path and updating shortest_vertex accordingly
	for valid in valid_cities:
		if(not shortest[get_index_from_city(valid_cities, valid)] and distances[get_index_from_city(valid_cities, valid)] <= shortest_path):
			shortest_path = distances[get_index_from_city(valid_cities, valid)]
			shortest_vertex = get_index_from_city(valid_cities, valid)

	return shortest_vertex

open_map("citymap.txt")