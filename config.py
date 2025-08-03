import os
from typing import List

class Settings:
    # Configurações de CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",    # React dev server
        "http://localhost:8080",    # Vue dev server  
        "http://localhost:5173",    # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080", 
        "http://127.0.0.1:5173",
        "http://192.168.1.100:3000",  # IP adicional - substitua pelo IP desejado
        "http://192.168.1.100:8080",
    ]
    
    # Permite configurar origens adicionais via variável de ambiente
    ADDITIONAL_CORS_ORIGINS = os.getenv("ADDITIONAL_CORS_ORIGINS", "")
    
    def __init__(self):
        # Adiciona origens extras da variável de ambiente
        if self.ADDITIONAL_CORS_ORIGINS:
            additional_origins = [
                origin.strip() 
                for origin in self.ADDITIONAL_CORS_ORIGINS.split(",")
                if origin.strip()
            ]
            self.CORS_ORIGINS.extend(additional_origins)

settings = Settings()
