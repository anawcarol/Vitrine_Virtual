import uvicorn
from fastapi import FastAPI
from app.api.v1.endpoints import analysis, analysis_temp

app = FastAPI(title="Vitrine Virtual API", version="1.0.0")

# Inclui as rotas
app.include_router(analysis.router, prefix="/api/v1", tags=["Video Analysis"])
app.include_router(analysis_temp.router, prefix="/api/v1", tags=["Weather Intelligence"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)