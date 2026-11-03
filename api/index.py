from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.tasks import router as tasks_router

app = FastAPI(
    title="Neobrutalist Task List API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Configuração de CORS para permitir requisições locais e remotas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rotas
app.include_router(tasks_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "neobrutalist-task-list"}
