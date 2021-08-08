import json
import os
from datetime import datetime
from here_location_services import LS
from here_location_services.config.routing_config import ROUTING_RETURN


def get_info(los_res):
    """
    This function parse result from HERE route api, and return travel_time and trip length
    Parameters
        los_res: result from HERE rout api
    Return
        (trip_duration, trip_length)
    """
    try:
        res = los_res.routes[0]['sections'][0]['summary']
        return res['duration'], res['length']
    except:
        return 0, 0

def collect_here_los(ls, orig, dest, departure_time=None):
    """
    This function collect level of service (travel time) from HERE APIs
    
    Parameters
        ls: HERE location services (LS) object
        orig: origin location as a [lattitue, longtitude] list
        dest: destination location as a [lattitue, longtitude] list
        departure_time: the trip's departure time in datetime format
    Return
        [car_duration, car_length, cycle_duration, cycle_length, walk_duration, walk_length]
    """
    try:
        # Get car duration and length
        car_res = ls.car_route(origin=orig, destination=dest, departure_time=departure_time, 
                            return_results=[ROUTING_RETURN.summary])
        car_dur, car_len = get_info(car_res)
        # Get cycle duration and length
        cycle_res = ls.bicycle_route(origin=orig, destination=dest, departure_time=departure_time, 
                            return_results=[ROUTING_RETURN.summary])
        cycle_dur, cycle_len = get_info(cycle_res)
        # Get walk duration and length
        walk_res = ls.pedestrian_route(origin=orig, destination=dest, departure_time=departure_time, 
                            return_results=[ROUTING_RETURN.summary])
        walk_dur, walk_len = get_info(walk_res)
        return [car_dur, car_len, cycle_dur, cycle_len, walk_dur, walk_len]    
    except:
        return [0, 0, 0, 0, 0, 0]