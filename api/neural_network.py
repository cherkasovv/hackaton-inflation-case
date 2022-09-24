from fastapi import APIRouter, UploadFile, BackgroundTasks
from db.session import current_session
from models.y_train import YTrain
from scheme.y_train import YtrainOut

router = APIRouter()


def start_neural_network(file):
    pass


@router.post("/send-file")
def send_file_in_nn(file: UploadFile, start_neural_network: BackgroundTasks):
    start_neural_network.add_task(start_neural_network, file=file)
    return {
        "result": f"{file.filename} is upload"
    }


@router.get("/inflation-info", response_model=list[YtrainOut])
def get_inflation_info():
    return current_session.query(YTrain).order_by(YTrain.year, YTrain.month).all()