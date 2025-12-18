import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Adicionamos 'analise_final' na importação
from app.api.v1.endpoints import analysis, analysis_temp, analise_final

app = FastAPI(title="Vitrine Virtual API")

# 1. Configura o CORS primeiro (Essencial para o Dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Inclui as rotas
# Rota antiga (apenas vídeo)
app.include_router(analysis.router, prefix="/api/v1", tags=["Legacy Analysis"])

# Rota de Clima (apenas temperatura/chuva)
app.include_router(analysis_temp.router, prefix="/api/v1", tags=["Weather Intelligence"])

# ✅ NOVA ROTA PRINCIPAL (Vídeo + Clima + Inteligência)
app.include_router(analise_final.router, prefix="/api/v1", tags=["Final Product"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)