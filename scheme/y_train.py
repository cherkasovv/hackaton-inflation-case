from pydantic import BaseModel


class Ytrain(BaseModel):
    data: float
    month: int
    year: int


class YtrainOut(Ytrain):
    id: int

    class Config:
        from_orm = True