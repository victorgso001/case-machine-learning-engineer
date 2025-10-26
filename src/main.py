"""
    API's main module
"""
import pickle
from typing import Optional
import uvicorn
import numpy as np
from fastapi import FastAPI, File, HTTPException
from sklearn.linear_model import LinearRegression
from src.models import Inputs
# from src.database import InMemoryDatabase


app = FastAPI()
MODEL = Optional[LinearRegression]


@app.get(
    "/health",
    status_code=200,
    tags=["healthcheck"],
    summary="Health check"
)
def healthcheck():
    """
        API healthcheck
    """
    return {"status": "ok"}


@app.post(
    "/model/load",
    status_code=200,
    tags=["model_load"],
    summary="Loads a model into API for prediction"
)
def model_load(data: bytes = File(...)):
    """
        Route for model loading as pickle file
    """
    global MODEL
    try:
        MODEL = pickle.loads(data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Cannot load model"
        ) from e

    print(MODEL, flush=True)

    if not isinstance(MODEL, LinearRegression):
        raise HTTPException(
            status_code=403,
            detail="Cannot load model."
        )
    return {"message": "Model loaded successfully"}


@app.post(
    "/model/predict",
    tags=["Model Prediction"],
    summary="Predict arrival delay based on input variables"
)
def predict(inputs: Inputs):
    """
        Model prediction route
    """
    global MODEL
    values = [
        inputs.dep_time,
        inputs.sched_dep_time,
        inputs.dep_delay,
        inputs.sched_arr_time,
        inputs.distance,
        inputs.wind_speed_origin,
        inputs.wind_speed_dest
    ]

    predict = MODEL.predict(np.array(values).reshape(1, -1))
    print(predict)
    return {"message": {
        "arr_delay": predict[0]
    }}
# @app.post("/user/", tags=["example"], summary="Insert user")
# async def insert(data: dict):
#     """
#         Insert user to database
#     """
#     db = InMemoryDatabase()
#     users = db.get_collection('users')
#     users.insert_one(data)
#     return {"status": "ok"}


# @app.get(
#   "/user/{name}",
#   status_code=200,
#   tags=["example"],
#   summary="Get user by name"
# )
# async def get(name: str):
#     """
#         Get user from database
#     """
#     db = InMemoryDatabase()
#     users = db.get_collection('users')
#     user = users.find_one({"name": name})
#     return {"status": "ok", "user": user}


# @app.get("/user/", tags=["example"], summary="List all users")
# async def user_list():
#     """
#         Get all users from database
#     """
#     db = InMemoryDatabase()
#     users = db.get_collection('users')
#     return {"status": "ok", "users": list(users.find({}, {"_id": 0}))}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
