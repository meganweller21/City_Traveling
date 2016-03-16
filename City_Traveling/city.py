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

	dijkstra(results, valid_cities, "Billings")

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

			#hop_connection(results, valid_cities, city1In, city2In, hopsIn)
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
	
	#distance between two cities is greater than 0, so a direct edge exists
	if(miles != 0):
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

#returns list of tuples
#a tuple contains two cities and the weight between them
def get_weighted_matrix(results):
	matrix = []
	for city1, city2, weight in results:
		#same cities get 0's (violates k-hop rules)
		if(city1 == city2):
			matrix.append((city1, city2, 0))
		#direct cities get 1's (1-hop)
		else:
			matrix.append((city1, city2, 1))

	return matrix

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

#returns true if two indices represent the same city
def same_cities(valid_cities, i, j):
	if get_city_from_index(valid_cities, i) == get_city_from_index(valid_cities, j):
		return True
	else:
		return False

#if connection exists, weight is 1
def is_direct(results, valid_cities, i, j):
	city1 = get_city_from_index(valid_cities, i)
	city2 = get_city_from_index(valid_cities, j)
	if find_edge(results, city1, city2):
		return 1
	else:
		return 0

#used where there is not a direct path between two vertices
infinity = 1000000

#takes a start city and shows the distance to every other city
def dijkstra(results, valid_cities, start_city):
	results = [('A', 'B', 1), 
 			   ('B', 'C', 2),
 			   ('C', 'D', 3),
 			   ('A', 'C', 4),
 			   ('A', 'A', 0)]

	valid_cities = ['A', 'B', 'C', 'D']

	start_city = 'B'

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
				(not same_cities(valid_cities, shortest_vertex, j)) and 
				(distances[shortest_vertex] != infinity) and 
				((distances[shortest_vertex] + (is_direct(results, valid_cities, shortest_vertex, j)) < distances[j]))):
				distances[j] = (distances[shortest_vertex] + (is_direct(results, valid_cities, shortest_vertex, j)))
			j = j + 1
		i = i + 1

	#printing results for testing purposes
	for index in range(num_verticies):
		print(start_city, get_city_from_index(valid_cities, index), distances[index])

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