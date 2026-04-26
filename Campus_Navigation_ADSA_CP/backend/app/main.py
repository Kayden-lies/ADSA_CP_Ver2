from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.routing import route
from app.graph.data import NODES

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/nodes")
def get_nodes():
    return NODES

@app.get("/route")
def get_route(start: str, end: str, algo: str = "dijkstra"):
    return route(start, end, algo)