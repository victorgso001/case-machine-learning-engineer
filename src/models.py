"""
    General models
"""
from pydantic import BaseModel


class Inputs(BaseModel):
    """
        LinearRegression inputs model
    """
    dep_time: float
    sched_dep_time: float
    dep_delay: float
    sched_arr_time: float
    distance: float
    wind_speed_origin: float
    wind_speed_dest: float
