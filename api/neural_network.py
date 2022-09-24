from fastapi import APIRouter, UploadFile, BackgroundTasks
from db.session import current_session, scope
from models.y_train import YTrain
from scheme.y_train import YtrainOut
from typing import List
from neural_network import run_neural_network
import shutil
import json
import os.path

from uuid import uuid4

router = APIRouter()


def start_neural_network(file_path: str):
    results = json.loads(run_neural_network(file_path, False))['data']

    for result in results:
        model = current_session.query(YTrain).filter_by(year=int(result[0]['qyear']), month=int(result[0]['month']))
        if not model:
            model = YTrain(
                year=result[0]['qyear'],
                month=result[0]['month'],
                data=result[1]
            )
        else:
            model.data = result[1]
            
        current_session.add(model)

    current_session.commit()


@router.post("/send-file")
def send_file_in_nn(file: UploadFile, start_neural_network_task: BackgroundTasks):
    file_path = f"data/{file.filename}"
    if not os.path.exists(file_path):
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    start_neural_network_task.add_task(start_neural_network, file_path=file_path)
    return {
        "result": f"{file.filename} is upload"
    }


@router.get("/inflation-info", response_model=List[YtrainOut])
def get_inflation_info():
    return current_session.query(YTrain).order_by(YTrain.year, YTrain.month).all()
