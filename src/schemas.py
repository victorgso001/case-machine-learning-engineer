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


class Outputs(Inputs):
    """
        Class to save predictions in database
    """
    id: str = ""
    predicted_arr_delay: float = 0.0


def output_serialized(output):
    """
        Serialization function to a single output
        Returns a single output
    """
    output['id'] = str(output['_id'])
    output.pop('_id')
    return output


def outputs_serialized(outputs):
    """
        Serialization function of a list of outputs
        Returns a list of serialized outputs
    """
    return [output_serialized(output) for output in outputs]
