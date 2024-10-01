from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import pickle

# Running Project Html = uvicorn main:app --reload

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Muat model yang sudah disimpan
with open('lin_reg_rumah.pkl', 'rb') as f:
    lin_reg = pickle.load(f)

@app.post("/predict", response_class=HTMLResponse)
async def create(request: Request, pc: int = Form('pc'), cf: int = Form('cf'), yb: int = Form('yb'), ad: int = Form('ad'), ls: float = Form('ls'), br: int = Form('br')):
    # Konversi nilai dari string menjadi tipe numerik

    PC = int(pc)
    CF = int(cf)
    YB = int(yb)
    AD = int(ad)
    LS = float(ls)
    BR = int(br)
    
    prediction = lin_reg.predict([[PC, CF, YB, AD, LS, BR]])
    harga_prediksi = round(prediction[0], 0)

    if harga_prediksi < 0:
        harga_prediksi = -harga_prediksi

    formatted_harga_prediksi = "{:,.0f}".format(harga_prediksi)


    # Render template HTML dengan data prediksi
    return templates.TemplateResponse("index.html", {"request": request, "predicted_price": formatted_harga_prediksi, "tahun":yb, "luas":ls})

    

if __name__ == "__main__":
    app.run(debug=True)
