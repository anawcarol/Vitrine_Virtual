from fastapi import HTTPException, status

# Exemplo de erro quando o vídeo não tem pessoas
def video_processing_error(detail: str = "Erro ao processar vídeo"):
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail
    )

# Exemplo de erro quando não encontra dados no banco
def not_found_error(detail: str = "Recurso não encontrado"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )