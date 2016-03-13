# Megan Weller
# Ashley Bertrand
# CSCI 338 Concepts
import re

def read_file(file_name):
	file = open(file_name, "r")
	line = file.readline().replace("-----------------------", "").replace("\t", "")    
	results = []
	
	while line:
		if (line == '\n'):  #we don't want to read in a blank line
			line = file.readline().replace("\t", " ").replace("-----------------------", "")
		else:
			line = line.strip() #strip unnessesary white space
			line = re.sub('\s\s+', ',', line)   #replace lone tabs with a comma
			fromCity, toCity, miles = line.split(',')  # splits line into list of tokens
		
			results.insert(0, (fromCity, toCity, miles))   # insert into the map
			
			line = file.readline().replace("\t", " ").replace("-----------------------", "")
	   
		
	results.reverse()                # original order
	#print(map)
	return results

def open_map(file_name):
	cityMap = read_file(file_name)
	clone = cityMap[:]

	solve_map(clone)




#--------------------------------------------



def solve_map(results):
	print ("Welcome to the new Montana Road Network")
	print ("1. Enter 1 to see how many cities are connected to a specific city")
	print ("2. Enter 2 to see if two cities have a direct connection")
	print ("3. Enter 3 to see if two cities have a connection")
	print ("4. Enter 4 to see if two cities have any connection")
	print ("5. Quit")


	userIn = input("Enter your choice: ")

	if (userIn == '1'):
		cityIn = input("Enter the city: ")
		print(find_city_num(results, cityIn))
	elif (userIn == '2'):
		city1In = input("First City: ")
		city2In = input("Second City:")
		print(find_edge(results, city1In, city2In))
	elif (userIn == '3'):
		city1In = input("First City: ")
		city2In = input("Second City: ")
		hopsIn = input("Hop connection: ")
		print(hop_connection(results, city1In, city2In, hopsIn))
	elif (userIn == '4'):
		city1In = input("First City: ")
		city2In = input("Second City: ")
		print(city_connection(results, city1In, city2In))
	else:
		print("quitting")


#Task 1. Number of cities directly connected to a query city.
#Complete!
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
	
	if(miles != 0):
		return miles
	else:
		return "No connection"

#Task 3. Given two query cities and an integer d, return YES/NO for whether there is a k-hop connection,
#k ≤ d, between them; if YES, print one solution out, to gether with the total distance of the d hops.

def hop_connection(results, city1, city2, d):
	mapCity = city1
	i = 0
	netMiles = 0
	
	mapConnections = []

	for result in results:
		if(result[0] == mapCity):
			for i in range(0, int(d)):
				mapConnections.insert(0, (mapCity, result[2]))
				mapCity = result[1]
				netMiles = result[2]
					
		print( "before if: ", str(mapCity), ' ', result[0], ' ', result[1])
		if (result[0] == mapCity and result[1] == city2):
			mapConnections.insert(0, (city2, result[2]))
			mapConnections.reverse()
			for mapConnection in mapConnections:
				print (mapConnection[0], ' ', mapConnection[1])
			return netMiles	
	
	#mapConnections.reverse()
	return netMiles
	
#Task 4. Given two query cities, return YES/NO for whether there is a connection (not necessarily direct)
#between them; if YES, print one solution out, together with the actual total distance of the connection.
def city_connection(results, city1, city2):
	mapConnections = []
	mapCity = city1
	for result in results:
		if(result[0] == mapCity):
			print("Hi I'm here: ", mapCity, ' ', result[1])
			mapConnections.insert(0, (mapCity, results[2]))

			if(result[1] == city2):

				mapConnections.insert(0, (result[1], result[2]))
				mapConnections.reverse()
				for mapConnection in mapConnections:
					print(str(mapConnection[0]), " ", str(mapConnection[1]))
				return "There is a connection"
				break;
			else:
				mapCity = result[1]
				#print (str(mapCity))
			
	



open_map("citymap.txt")