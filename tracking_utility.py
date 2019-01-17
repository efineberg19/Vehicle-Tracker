#!/usr/bin/python
#tracking_utility.py

'''File provides methods to be called by GUI that perform action or return 
information about the train/vehicle specified by the user in the GUI.'''

__author__ = "Beth Fineberg"
__version__ = "1.0"

import requests
import webbrowser
import json
import util
import datetime
import iso8601

def get_arrival_time(station, direction):
    """returns the predicted arrival time of the next train coming to a specific
    station going in a certain direction
    
    :param: station: station that user wants prediction for
    :param: direction: 1 if going inboud, 0 if going outbound
    
    :return: time: the time the next train is arriving at station
    :return: vehicle_id: id of the next train arriving at station
    """       
    
    ##################################################
    ### Gets MBTA data is usable dictionary format ###
    ##################################################
    
    vehicle_link = "https://api-v3.mbta.com/vehicles"
    predict_link = ""
    
    vehicle_data = requests.get(vehicle_link)
    predictions_data = ""
    
    vehicle_file = json.loads(vehicle_data.text)
    prediction_file = ""
    
    vehicles = vehicle_file["data"]
    predictions = ""
    
    vehicle_id = ""
    station_name = station
    
    if station == "Symphony":
        if direction == 0:
            #mbta code for trains going outbound to Symphony
            station_name = "70241"
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B"\
                + "stop%5D=place-symcl&amp;filter%5Bdirection_id%5D=0&amp;" +\
                "include=stop"
            
        elif direction == 1:
            #mbta code for trains going inbound to Symphony
            station_name = "70242"
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B"\
                + "stop%5D=place-symcl&amp;filter%5Bdirection_id%5D=1&amp;" +\
                "include=stop"
            
        predictions_data = requests.get(predict_link)      
        prediction_file = json.loads(predictions_data.text)
        predictions = prediction_file["data"]
        
    elif station == "Kenmore": 
        #mbta code for trains going outbound to Kenmore
        if direction == 0:
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B" +\
                "stop%5D=place-kencl&amp;filter%5Bdirection_id%5D=0&amp;" +\
                "include=stop"
            station_name = "70150"
        
        #mbta code for trains going inbound to Kenmore
        elif direction == 1:
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B" +\
                "stop%5D=place-kencl&amp;filter%5Bdirection_id%5D=1&amp;" +\
                "include=stop"
            station_name = "70151"
        
        predictions_data = requests.get(predict_link)
        prediction_file = json.loads(predictions_data.text)
        predictions = prediction_file["data"]        
        
    elif station == "North Station":
        if direction == 0:
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B" +\
                "stop%5D=place-north&amp;filter%5Bdirection_id%5D=0&amp;" +\
                "include=stop"
            
        elif direction == 1:
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B" +\
                "stop%5D=place-north&amp;filter%5Bdirection_id%5D=1&amp;" +\
                "include=stop"
        
        predictions_data = requests.get(predict_link)
        prediction_file = json.loads(predictions_data.text)
        predictions = prediction_file["data"]
    
    elif station == "Copley":
        #mbta code for trains going outbound to Copley
        if direction == 0:
            station_name = "70155"
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B" +\
                "stop%5D=place-coecl&amp;filter%5Bdirection_id%5D=0&amp;" +\
                "include=stop"
        
        #mbta code for trains going outbound to Copley
        elif direction == 1:
            station_name = "70154"
            predict_link = "https://api-v3.mbta.com/predictions?filter%5B" +\
                "stop%5D=place-coecl&amp;filter%5Bdirection_id%5D=1&amp;" +\
                "include=stop"
            
        predictions_data = requests.get(predict_link)
        prediction_file = json.loads(predictions_data.text)
        predictions = prediction_file["data"]
        
    for vehicle in vehicles:
        #can come back as none, so use try
        try:
            if vehicle["relationships"]["stop"]["data"]["id"] is not None:
                if vehicle["relationships"]["stop"]["data"]["id"] == station_name: 
                    #saves vehicle id if train is going to correct stop
                    vehicle_id = vehicle["relationships"]["trip"]["data"]["id"] 
        except:
            pass  
            
    for prediction in predictions: #goes through predictions
        #if finds matching id, predicted arrival time returned
        if vehicle_id == prediction["relationships"]["trip"]["data"]["id"]:
            #original time in dictionary is in iso8601 form
            og_time = prediction["attributes"]["arrival_time"]
            
            #parses as usable iso8601 format
            iso_time = iso8601.parse_date(og_time)
            
            #saves time as string in readable hours/minutes format
            time = str(iso_time.time())
            
            #just in case if return is none
            try:
                return [time, vehicle_id]
            except:
                pass
                                   
def open_google_maps(vehicle_id):
    """opens google map of where the the vehicle with the given id is
    
    :param: vehicle_id: identifying number of a specific vehicle
    """    
    
    ##################################################
    ### Gets MBTA data is usable dictionary format ###
    ##################################################
    vehicle_link = "https://api-v3.mbta.com/vehicles"
    vehicle_data = requests.get(vehicle_link)
    vehicle_file = json.loads(vehicle_data.text)
    vehicles = vehicle_file["data"]
    
    for vehicle in vehicles: #goes through all vehicle
        if vehicle_id == vehicle["relationships"]["trip"]["data"]["id"]:
            #if id matches one specified, google map of its location opened
            webbrowser.open_new("http://maps.google.com/maps?q=" +
                                str(vehicle["attributes"]["latitude"]) + "," + 
                                str(vehicle["attributes"]["longitude"]))
            

def show_closest_vehicle(longitude, latitude):
    """opens google map of where the closest vehicle to the coordinates 
    specified by the user is
    
    :param: longitude: longitude of location specified by user
    :param: latitude: latitude of location specified by user
    """
    
    ##################################################
    ### Gets MBTA data is usable dictionary format ###
    ##################################################
    vehicle_link = "https://api-v3.mbta.com/vehicles"
    vehicle_data = requests.get(vehicle_link)
    vehicle_file = json.loads(vehicle_data.text)
    vehicles = vehicle_file["data"]
    
    #sets min_dist to big #, because initial dist value needs to be smaller than
    min_dist = 100000000000
    closest_lat = ""
    closest_long = ""
    
    for vehicle in vehicles:
        
            if vehicle["attributes"]["direction_id"] == 1:
                #goes through all vehicles, sees if it is closest to given coords
                if util.get_distance_between_coords(vehicle["attributes"]["latitude"],
                                                    vehicle["attributes"]["longitude"],
                                                    longitude, latitude) < min_dist:
                    
                    min_dist = util.get_distance_between_coords(\
                        vehicle["attributes"]["latitude"],\
                        vehicle["attributes"]["longitude"], longitude, latitude)
                    
                    #if distance is smaller than last minimum, currend coords saved
                    closest_lat = vehicle["attributes"]["latitude"]
                    closest_long = vehicle["attributes"]["longitude"]
                    label = vehicle["attributes"]["label"]      
    
    #opens up google map with coordinates of closest vehicle
    webbrowser.open_new("http://maps.google.com/maps?q=" + str(closest_lat) + \
                        "," + str(closest_long))      