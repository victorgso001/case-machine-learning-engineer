"""
    API's main module
"""
import pickle
from typing import Optional
import uvicorn
import numpy as np
from fastapi import FastAPI, File, HTTPException
from sklearn.linear_model import LinearRegression
from src.schemas import Inputs, Outputs, outputs_serialized
from src.database import db_client


app = FastAPI()
db = db_client()
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

    if not isinstance(MODEL, LinearRegression):
        raise HTTPException(
            status_code=403,
            detail="Model not loaded. Please load model first"
        )
    values = [
        inputs.dep_time,
        inputs.sched_dep_time,
        inputs.dep_delay,
        inputs.sched_arr_time,
        inputs.distance,
        inputs.wind_speed_origin,
        inputs.wind_speed_dest
    ]

    prediction = MODEL.predict(np.array(values).reshape(1, -1))

    output = Outputs(**inputs.model_dump())
    output.predicted_arr_delay = prediction[0]

    db.outputs.insert_one(output.model_dump())

    return {"message": {
        "arr_delay": prediction[0]
    }}


@app.get(
    "/model/history",
    tags=["Model predictions history"],
    summary="Get a list of historic model predictions"
)
def history():
    """
        History routes function
    """
    outputs = list(db.outputs.find())
    return outputs_serialized(outputs)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
