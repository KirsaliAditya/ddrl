from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from matrix import is_deadlocked
from rag_wfg import run_deadlock_detection
import json

app = FastAPI()

class MatrixInput(BaseModel):
    available: List[int]
    allocation: List[List[int]]
    request: List[List[int]]
    simulation_id: str = "matrix_sim"

class WFGInput(BaseModel):
    available: List[int]
    allocation: List[List[int]]
    request: List[List[int]]
    simulation_id: str = "wfg_sim"

@app.post("/api/matrix")
def matrix_simulation(input_data: MatrixInput):
    try:
        deadlocked = is_deadlocked(
            input_data.available,
            input_data.allocation,
            input_data.request,
            input_data.simulation_id
        )

        # Load the simulation steps from the log file
        with open("matrix_simulations.json", "r") as f:
            simulations = json.load(f)
            matching_sim = next((sim for sim in simulations if sim["simulation_id"] == input_data.simulation_id), None)

        return {
            "deadlocked": deadlocked,
            "simulation": matching_sim
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matrix deadlock check failed: {str(e)}")

@app.post("/api/wfg")
def wfg_simulation(input_data: WFGInput):
    try:
        deadlocked, cycle_nodes, file_path = run_deadlock_detection(
            input_data.available,
            input_data.allocation,
            input_data.request,
            input_data.simulation_id
        )

        # Load the simulation steps from the log file
        with open("deadlock_simulations.json", "r") as f:
            simulations = json.load(f)
            matching_sim = next((sim for sim in simulations if sim["simulation_id"] == input_data.simulation_id), None)

        return {
            "deadlocked": deadlocked,
            "cycle_nodes": list(cycle_nodes),
            "simulation": matching_sim
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"WFG deadlock check failed: {str(e)}")
