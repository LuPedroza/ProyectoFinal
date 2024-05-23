from fastapi import FastAPI
from conexion import  seriesPorNombre,TodasSeries,seriePorAudiencia,seriePorTecnica,seriePorCanal,seriesPorCompania, seriesPorNombreYcanal, seriesPorNombreYaudiencia,seriePorTecnicayNombre
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins=[
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/series/")
async def obtener_series(tipo: str = None, valor: str = None,valor2: str = None):
    if tipo == 'canal':
        return seriePorCanal(valor)
    elif tipo=='tecnica':
        return seriePorTecnica(valor)
    elif tipo=='audiencia':
        return seriePorAudiencia(valor)
    elif tipo=='todas':
        return TodasSeries()
    elif tipo=='serie':
        return seriesPorNombre(valor)
    elif tipo=='compania':
        return seriesPorCompania(valor)
    elif tipo =='serieYcanal':
       return seriesPorNombreYcanal(valor,valor2)
    elif  tipo=='serieYaudiencia':
        return seriesPorNombreYaudiencia(valor,valor2)
    elif tipo=='TecnicaYNombre':
        return seriePorTecnicayNombre(valor,valor2) #serie y tecnica
    else:
        return {"error": "Tipo de consulta no válido"}
