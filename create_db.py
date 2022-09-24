from models.y_train import YTrain
from db.session import engine

if __name__ == "__main__":
    YTrain.__table__.create(bind = engine)