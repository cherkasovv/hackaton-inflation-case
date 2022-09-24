from fastapi import APIRouter, UploadFile, BackgroundTasks
from db.session import current_session
from models.y_train import YTrain
from scheme.y_train import YtrainOut
from typing import List
from neural_network import run_neural_network
import shutil

router = APIRouter()


def start_neural_network(file_path: str):
    run_neural_network(file_path, False)


@router.post("/send-file")
def send_file_in_nn(file: UploadFile, start_neural_network_task: BackgroundTasks):
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    start_neural_network_task.add_task(start_neural_network, file_path=file_path)
    return {
        "result": f"{file.filename} is upload"
    }


@router.get("/inflation-info", response_model=List[YtrainOut])
def get_inflation_info():
    return current_session.query(YTrain).order_by(YTrain.year, YTrain.month).all()
