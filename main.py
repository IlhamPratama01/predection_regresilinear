from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle

app = FastAPI()

# Definisikan model input
class HouseData(BaseModel):
    LB: float
    LT: float
    KT: int
    KM: int
    GRS: int

# Muat model yang sudah disimpan
with open('lin_reg_model.pkl', 'rb') as f:
    lin_reg = pickle.load(f)

@app.put("/predict")
def update_item(data: HouseData):
    # Buat prediksi
    prediction = lin_reg.predict([[data.LB, data.LT, data.KT, data.KM, data.GRS]])
    harga_prediksi = round(prediction[0], 0)
    
    return {"predicted_price": harga_prediksi}

# Endpoint root untuk pengujian
@app.get("/")
def read_root():
    return {"Hello": "World"}
