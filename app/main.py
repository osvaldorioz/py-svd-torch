from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
from typing import List
import matplotlib
import matplotlib.pyplot as plt
import torch
import svd_module
import json

matplotlib.use('Agg')  # Usar backend no interactivo
app = FastAPI()

# Definir el modelo para el vector
class VectorF(BaseModel):
    vector: List[float]
    
@app.post("/singular-value-decomposition")
def calculo(tensor_x: int, tensor_y: int):
    output_file = 'singular-value-decomposition.png'
    # Crear un tensor de mayor tamaño (por ejemplo, 1000x500)
    tensor = torch.randn(tensor_x, tensor_y)

    # Calcular la SVD utilizando el módulo C++
    U, S, V = svd_module.compute_svd(tensor)

    # Convertir los valores singulares a numpy para su visualización
    S_np = S.numpy()

    # Graficar los valores singulares
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(S_np)), S_np, color='blue', label='Valores Singulares')
    plt.xlabel('Índice')
    plt.ylabel('Valor Singular')
    title = "Valores Singulares de la Matriz de Entrada de Tamaño %dx%d" % (tensor_x,tensor_y)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    #plt.show()

    plt.savefig(output_file)
    plt.close()
    
    j1 = {
        "Grafica": output_file
    }
    jj = json.dumps(str(j1))

    return jj

@app.get("/singular-value-decomposition-graph")
def getGraph(output_file: str):
    return FileResponse(output_file, media_type="image/png", filename=output_file)