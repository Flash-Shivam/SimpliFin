class RideSharingApp:
    def __init__(self):
        self.users = {}
        self.rides = {}
        self.ride_offered = {}
        self.ride_taken = {}

    def add_user(self, user_detail):
        name, _, _ = user_detail.split(", ")
        if name in self.users:
            print(f"User {name} already exists.")
        else:
            self.users[name] = {"details": user_detail, "vehicles": []}
            self.ride_offered[name] = 0
            self.ride_taken[name] = 0
            print(f"User {name} added successfully.")

    def add_vehicle(self, vehicle_detail):
        user_name, vehicle_info = vehicle_detail.split(", ")[0], ", ".join(vehicle_detail.split(", ")[1:])
        if user_name in self.users:
            self.users[user_name]["vehicles"].append(vehicle_info)
            print(f"Vehicle added successfully for {user_name}.")
        else:
            print(f"User {user_name} does not exist.")

    def offer_ride(self, ride_detail):
        driver_name, details = ride_detail.split(", ")[0], ", ".join(ride_detail.split(", ")[1:])
        source1, seats1, vehicle1, vehicle_number1, destination1 = details.split(", ");
        if driver_name in self.users:
            if driver_name not in self.rides:
                self.rides[driver_name] = [details]
                self.ride_offered[driver_name] = self.ride_offered[driver_name] + 1
                print(f"Ride offered successfully by {driver_name}.")
            else:
                flag1 = True
                for detail in self.rides[driver_name]:
                    source, seats, vehicle, vehicle_number, destination = detail.split(", ")
                    # ride will be identical when vehicle number and vehicle type is same
                    if vehicle1 != vehicle or vehicle_number != vehicle_number1:
                        self.rides[driver_name].append(details)
                        self.ride_offered[driver_name] = self.ride_offered[driver_name] + 1
                        print(f"Ride offered successfully by {driver_name}.")
                        flag1 = False
                        break
                if flag1 == True:
                    print(f"Ride already offered by {driver_name}.")
        else:
            print(f"User {driver_name} does not exist.")


    def dfs(self, graph, start, dest, visited, path, user):
        visited[start] = True
        path.append(start)
        if start == dest:
            print("Path exists:", path)
            for i in range(len(path)-1):
                # for know I have kept it as most vacant
                # but we can customize it depending upon user , by adding another param in the function
                ride_detail = user + ", Origin=" + path[i] + ", Destination=" + path[i+1] + ", Seats=1, Most Vacant"
                self.select_ride(ride_detail)
            return True

        for neighbor in graph.get(start, []):
            if not visited.get(neighbor, False):
                if self.dfs(graph, neighbor, dest, visited, path, user):
                    return True
        path.pop()
        return False



    def decrementSeats(self, ride, ride_details, driver):
        ride_details = [f'Available Seats={int(ride_details.split("=")[1]) - 1}' if ride_details.startswith('Available Seats=') else ride_details for ride_details in ride_details]
        self.rides[driver].remove(ride)
        self.rides[driver].append(", ".join(ride_details))


    def select_ride(self, ride_detail):
        driver_name ,source, destination, seats, selection_strategy = ride_detail.split(", ");
        source = source.split('=')[1]
        destination = destination.split('=')[1]
        seats = int(seats.split('=')[1])
        flag = True
        selected_ride = None
        ride_taken = None
        driver_taken = None
        ride_taken_details = None
        for driver, rides in self.rides.items():
            if flag == False:
                break
            for ride in rides:
                ride_details = ride.split(", ")
                if ride_details[0].split("=")[1] == source and ride_details[4].split("=")[1] == destination:
                    available_seats = int(ride_details[1].split("=")[1])
                    if available_seats >= seats:
                        if selection_strategy == "Most Vacant":
                            if selected_ride is None or available_seats > int(selected_ride.split(", ")[1].split("=")[1]):
                                ride_taken = ride
                                driver_taken = driver
                                ride_taken_details = ride_details
                                selected_ride = ride
                        else :
                            passenger_vehicle = ride_details[2].split("=")[1]
                            if passenger_vehicle == selection_strategy.split("=")[1]:
                                selected_ride = ride
                                ride_taken = ride
                                driver_taken = driver
                                ride_taken_details = ride_details
                                flag = False
                                break
                                

        if selected_ride:
            #update the available seats -> decrement it by one as single user is occupying it 
            self.decrementSeats(ride_taken, ride_taken_details, driver_taken)
            self.ride_taken[driver_name] = self.ride_taken[driver_name] + 1
            print(f"Selected ride: {selected_ride}")
        else:
            print("No rides found.")

    def find_connecting_ride(self, source, destination, user):
        #create a directed graph with exisiting rides
        #node => location
        # a->b  (edge from a to b) => ride is offered from node a to b  
        # run dfs to check if path exist from source to destination
        # here we can also create graph edges on the basis of user preference of selection strategy 
        graph = {}
        for driver, rides in self.rides.items():
            for ride in rides:
                ride_details = ride.split(", ")
                source1 = ride_details[0].split("=")[1] 
                destination1 = ride_details[4].split("=")[1]
                if source1 in graph.keys():
                    if destination1 not in graph[source1]:
                        graph[source1].append(destination1)
                else:
                    graph[source1] = [destination1]

        visited = {node: False for node in graph}
        path = []

        if not app.dfs(graph, source, destination, visited, path, user):
            print("Path does not exist")


    def end_ride(self, ride_details):
        driver_name, details = ride_details.split(", ")[0], ", ".join(ride_details.split(", ")[1:])
        source, vehicle, vehicle_number, destination = details.split(", ");
        if driver_name in self.rides.keys():
            flag = False
            for ride in self.rides[driver_name]:
                if flag == True:
                    break;
                source1, _, vehicle1, vehicle_number1, destination1 = ride.split(", ")
                if (source, vehicle, vehicle_number, destination) == (source1, vehicle1, vehicle_number1, destination1):
                    # Removing ride from the storage as the offered ride has ended 
                    self.rides[driver_name].remove(ride)
                    print("Ride ended successfully.")
                    flag = True
                    break
            if flag == False:
                print("No such ride exists.")
                    
        else:
            print("No such ride exists.")
            
    # According to my defination if a user had offered a valid ride then we count it as ride offered 
    def print_ride_stats(self):
        for user in self.users:
            taken = self.ride_taken[user]
            offered = self.ride_offered[user]
            print(f"{user}: {taken} Taken, {offered} Offered")


if __name__ == "__main__":
    app = RideSharingApp()

    app.add_user("Rohan, M, 36")
    app.add_vehicle("Rohan, Swift, KA-01-12345")
    app.add_user("Shashank, M, 29")
    app.add_vehicle("Shashank, Baleno, TS-05-62395")
    app.add_user("Nandini, F, 29")
    app.add_user("Shipra, F, 27")
    app.add_vehicle("Shipra, Polo, KA-05-41491")
    app.add_vehicle("Shipra, Activa, KA-12-12332")
    app.add_user("Gaurav, M, 29")
    app.add_user("Rahul, M, 35")
    app.add_vehicle("Rahul, XUV, KA-05-1234")

    app.offer_ride("Rohan, Origin=Hyderabad, Available Seats=1, Vehicle=Swift, KA-01-12345, Destination=Bangalore")
    app.offer_ride("Shipra, Origin=Bangalore, Available Seats=1, Vehicle=Activa, KA-12-12332, Destination=Mysore")
    app.offer_ride("Shipra, Origin=Bangalore, Available Seats=2, Vehicle=Polo, KA-05-41491, Destination=Mysore")
    app.offer_ride("Shashank, Origin=Hyderabad, Available Seats=2, Vehicle=Baleno, TS-05-62395, Destination=Bangalore")
    app.offer_ride("Rahul, Origin=Hyderabad, Available Seats=5, Vehicle=XUV, KA-05-1234, Destination=Bangalore")
    app.offer_ride("Rohan, Origin=Bangalore, Available Seats=1, Vehicle=Swift, KA-01-12345, Destination=Pune")

    app.select_ride("Nandini, Origin=Bangalore, Destination=Mysore, Seats=1, Most Vacant")
    app.select_ride("Gaurav, Origin=Bangalore, Destination=Mysore, Seats=1, Preferred Vehicle=Activa")
    app.select_ride("Shashank, Origin=Mumbai, Destination=Bangalore, Seats=1, Most Vacant")
    app.select_ride("Rohan, Origin=Hyderabad, Destination=Bangalore, Seats=1, Preferred Vehicle=Baleno")
    app.select_ride("Shashank, Origin=Hyderabad, Destination=Bangalore, Seats=1, Preferred Vehicle=Polo")


    # We are ending rides based on username , vehicle details , origin , destination and not based on avaialble seats ,
    # as avaialble seats is dynamically updated on taking up rides 
    app.end_ride("Rohan, Origin=Hyderabad, Vehicle=Swift, KA-01-12345, Destination=Bangalore")
    app.end_ride("Shipra, Origin=Bangalore, Vehicle=Activa, KA-12-12332, Destination=Mysore")
    app.end_ride("Shipra, Origin=Bangalore, Vehicle=Polo, KA-05-41491, Destination=Mysore")
    app.end_ride("Shashank, Origin=Hyderabad, Vehicle=Baleno, TS-05-62395, Destination=Bangalore")

    app.print_ride_stats()

    #Run command on terminal : python3 assignment.py

    #Output ->

    # User Rohan added successfully.
    # Vehicle added successfully for Rohan.
    # User Shashank added successfully.
    # Vehicle added successfully for Shashank.
    # User Nandini added successfully.
    # User Shipra added successfully.
    # Vehicle added successfully for Shipra.
    # Vehicle added successfully for Shipra.
    # User Gaurav added successfully.
    # User Rahul added successfully.
    # Vehicle added successfully for Rahul.
    # Ride offered successfully by Rohan.
    # Ride offered successfully by Shipra.
    # Ride offered successfully by Shipra.
    # Ride offered successfully by Shashank.
    # Ride offered successfully by Rahul.
    # Ride already offered by Rohan.
    # Selected ride: Origin=Bangalore, Available Seats=2, Vehicle=Polo, KA-05-41491, Destination=Mysore
    # Selected ride: Origin=Bangalore, Available Seats=1, Vehicle=Activa, KA-12-12332, Destination=Mysore
    # No rides found.
    # Selected ride: Origin=Hyderabad, Available Seats=2, Vehicle=Baleno, TS-05-62395, Destination=Bangalore
    # No rides found.
    # Ride ended successfully.
    # Ride ended successfully.
    # Ride ended successfully.
    # Ride ended successfully.
    # Rohan: 1 Taken, 1 Offered
    # Shashank: 0 Taken, 1 Offered
    # Nandini: 1 Taken, 0 Offered
    # Shipra: 0 Taken, 2 Offered
    # Gaurav: 1 Taken, 0 Offered
    # Rahul: 0 Taken, 1 Offered



    #For Bonus question run the following main function 

    # app = RideSharingApp()

    # app.add_user("Shivam, M, 24")
    # app.add_user("Rohan, M, 36")
    # app.add_vehicle("Rohan, Swift, KA-01-12345")
    # app.add_user("Shashank, M, 29")
    # app.add_vehicle("Shashank, Baleno, TS-05-62395")
    # app.add_user("Nandini, F, 29")
    # app.add_user("Shipra, F, 27")
    # app.add_vehicle("Shipra, Polo, KA-05-41491")
    # app.add_vehicle("Shipra, Activa, KA-12-12332")
    # app.add_user("Gaurav, M, 29")
    # app.add_user("Rahul, M, 35")
    # app.add_vehicle("Rahul, XUV, KA-05-1234")

    # app.offer_ride("Shipra, Origin=Bangalore, Available Seats=1, Vehicle=Activa, KA-12-12332, Destination=Mysore")
    # app.offer_ride("Shipra, Origin=Bangalore, Available Seats=2, Vehicle=Polo, KA-05-41491, Destination=Mysore")
    # app.offer_ride("Shashank, Origin=Hyderabad, Available Seats=2, Vehicle=Baleno, TS-05-62395, Destination=Bangalore")
    # app.offer_ride("Rahul, Origin=Hyderabad, Available Seats=5, Vehicle=XUV, KA-05-1234, Destination=Bangalore")
    # app.offer_ride("Rohan, Origin=Bangalore, Available Seats=1, Vehicle=Swift, KA-01-12345, Destination=Pune")

    # app.find_connecting_ride("Hyderabad", "Pune", "Shivam")

    # output ->

    # User Shivam added successfully.
    # User Rohan added successfully.
    # Vehicle added successfully for Rohan.
    # User Shashank added successfully.
    # Vehicle added successfully for Shashank.
    # User Nandini added successfully.
    # User Shipra added successfully.
    # Vehicle added successfully for Shipra.
    # Vehicle added successfully for Shipra.
    # User Gaurav added successfully.
    # User Rahul added successfully.
    # Vehicle added successfully for Rahul.
    # Ride offered successfully by Shipra.
    # Ride offered successfully by Shipra.
    # Ride offered successfully by Shashank.
    # Ride offered successfully by Rahul.
    # Ride offered successfully by Rohan.
    # Path exists: ['Hyderabad', 'Bangalore', 'Pune']
    # Selected ride: Origin=Hyderabad, Available Seats=5, Vehicle=XUV, KA-05-1234, Destination=Bangalore
    # Selected ride: Origin=Bangalore, Available Seats=1, Vehicle=Swift, KA-01-12345, Destination=Pune




