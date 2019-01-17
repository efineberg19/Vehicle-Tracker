#!/usr/bin/python
#ezgui.py

'''Used template from modules project to build this. Prompts user to pick a game
mode and allows user to either find the vehicle closest to a given location or
find when the next train is arriving at a certain station on the Green Line. I 
stuck with Green line, because it is busy and made it doable to code.'''

import easygui
import tracking_utility

def main():
    easygui.msgbox(msg="Welcome to Vehicle Tracker!", title="Welcome!")    
    run_app()
    
def run_app():
    modes = ["Next Train Arriving", "Find the Nearest Vehicle", "Quit"]
    
    mode_selected = easygui.buttonbox(msg="Which mode would you like to play?",\
                                title="Pick a Mode", choices=modes)     
    
    if mode_selected == "Next Train Arriving":
        #stations chosen on green line
        stations = ["Symphony", "Kenmore", "North Station", "Copley"]
        
        directions = ["Inbound", "Outbound"]
        
        station = easygui.buttonbox(msg="Which train station would you like" +\
                                    "to go to?", title="Pick a Station", \
                                    choices=stations)
        
        direction = easygui.buttonbox(msg="Which direction are you going?",\
                       title="Pick a Direction", choices=directions)
        
        #the 1/0 setting is determined by the mbta
        if direction == "Inbound":
            direction = 1
        elif direction == "Outbound":
            direction = 0
        
        #finds which train is arriving next and at what time
        train_result = tracking_utility.get_arrival_time(station, direction)
        
        #must do this just in case result comes back as none
        try:
            if train_result[0] is not None:
                arrival_message = "The next train will arrive at: " +\
                    train_result[0]
                
                
                options = ["See Location of Train and Replay", "Quit"]
                
                #shows arrival time and allows user to quit or see on google map
                decision = easygui.buttonbox(msg=arrival_message, title=\
                                             "Arrival Time", choices=options)
                
                if decision == "See Location of Train and Replay":
                    #opens google map of where the vehicle is based on its id
                    tracking_utility.open_google_maps(train_result[1])
                    main()
                    
                elif decision == "Quit":
                    exit(0) 
                    
                else:
                    exit(0)
                
        except: #if no data is found, happens if no train is arriving soon
            options = ["Try Again", "Quit"]
            
            decision = easygui.buttonbox(msg="Sorry, no train at the moment.",\
                                         title="Sorry", choices=options) 
            
            if decision == "Quit":
                exit(0)
            elif decision == "Try Again":
                main()
            
    elif mode_selected == "Find the Nearest Vehicle":
        #interesting locations with transit nearby in Boston Area
        location_choices = ["CCHS", "Prudential Tower", "Boston Commons",\
                            "Harvard University", "Fenway", \
                            "Boston Logan Airport"]
        
        #allows user to pick location to find the nearest vehicle
        location = easygui.buttonbox(msg="Where are you?", title="Location",\
                                     choices=location_choices)  
        
        #opens up google map with location of closest vehicle to given coords
        if location == "CCHS":
            tracking_utility.show_closest_vehicle(42.4476, -71.3480)
            
        elif location == "Prudential Tower":
            tracking_utility.show_closest_vehicle(42.3471, -71.0825)  
            
        elif location == "Boston Commons":
            tracking_utility.show_closest_vehicle(42.3550, -71.0655) 
            
        elif location == "Harvard University":
            tracking_utility.show_closest_vehicle(42.3770, -71.1167) 
            
        elif location == "Fenway":
            tracking_utility.show_closest_vehicle(42.3429, -71.1003) 
            
        elif location == "Boston Logan Airport":
            tracking_utility.show_closest_vehicle(42.3656, -71.0096)  
            
        #automatically has user replay
        main()
            
    elif mode_selected == "Quit":
        pass
main()