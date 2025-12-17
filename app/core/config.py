from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Metadados da API
    PROJECT_NAME: str = "Vitrine Virtual API"
    API_V1_STR: str = "/api/v1"
    
    # Segurança
    SECRET_KEY: str = "segredo_temporario_hackathon"
    
    # Banco de Dados (Supabase)
    # O Pydantic vai buscar uma variável chamada DATABASE_URL no seu .env
    DATABASE_URL: str

    # Permite CORS (Importante para o Frontend Next.js acessar a API)
    # Em produção seria uma lista específica, no Hackathon liberamos tudo ("*")
    BACKEND_CORS_ORIGINS: list = ["*"]

    class Config:
        # Indica que deve ler o arquivo .env da raiz
        env_file = ".env"
        case_sensitive = True

settings = Settings()