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


def start_neural_network(file_path_csv: str, file_path_y_train: str):
    results = json.loads(run_neural_network(file_path_csv, False, file_path_y_train))['data']

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


def download_file(file: UploadFile):
    file_path = f"data/{file.filename}"
    if not os.path.exists(file_path):
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    
    return file_path


@router.post("/send-file")
def send_file_in_nn(csv_data: UploadFile, y_train_data: UploadFile, start_neural_network_task: BackgroundTasks):
    file_path_csv_data = download_file(csv_data)
    file_path_train_data = download_file(y_train_data)

    start_neural_network_task.add_task(start_neural_network, file_path_csv=file_path_csv_data, file_path_train=file_path_train_data)
    return {
        "result": f"{file_path_csv_data} is upload, {file_path_train_data} is uploaded"
    }


@router.get("/inflation-info", response_model=List[YtrainOut])
def get_inflation_info():
    return current_session.query(YTrain).order_by(YTrain.year, YTrain.month).all()
