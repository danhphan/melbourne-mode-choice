import json
import os
from datetime import datetime
from here_location_services import LS
from here_location_services.config.routing_config import ROUTING_RETURN


def get_info(los_res):
    """
    This function parse result from HERE route api, and return travel_time and trip length
    """
    res = los_res.routes[0]['sections'][0]['summary']
    return res['duration'], res['length']


def collect_here_los(ls, orig, dest, start_time):
    """
    This function collect level of service (travel time) from HERE APIs
    """    
    # Get car duration and length
    car_res = ls.car_route(origin=orig, destination=dest, departure_time=start_time, 
                        return_results=[ROUTING_RETURN.summary])
    car_dur, car_len = get_info(car_res)
    # Get cycle duration and length
    cycle_res = ls.bicycle_route(origin=orig, destination=dest, departure_time=start_time, 
                        return_results=[ROUTING_RETURN.summary])
    cycle_dur, cycle_len = get_info(cycle_res)
    # Get walk duration and length
    walk_res = ls.pedestrian_route(origin=orig, destination=dest, departure_time=start_time, 
                        return_results=[ROUTING_RETURN.summary])
    walk_dur, walk_len = get_info(walk_res)
    return [car_dur, car_len, cycle_dur, cycle_len, walk_dur, walk_len]   