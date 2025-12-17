import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import analysis, analysis_temp

app = FastAPI(title="Vitrine Virtual API")

# 1. Configura o CORS primeiro (Essencial para o Dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Inclui a rota
app.include_router(analysis.router, prefix="/api/v1", tags=["Video Analysis"])
app.include_router(analysis_temp.router, prefix="/api/v1", tags=["Weather Intelligence"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)