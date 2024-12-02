from fastapi import FastAPI, HTTPException, Request
from schemas import Plan, CreatePlan
from typing import List
import time
import os
import asyncpg

# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/study-plan") 
    return await asyncpg.connect(DATABASE_URL)

# Inicializar a aplicação FastAPI
app = FastAPI()

# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

@app.post("/api/v1/plans/", status_code=201)
async def add_plan(plan: CreatePlan):
    conn = await get_database()
    try:
        query = """
        INSERT INTO plan (goal, deadline, daily_hours, created_at, progress)
        VALUES ($1, $2, $3, NOW(), $4)
        RETURNING *;
        """
        async with conn.transaction():
            new_plan = await conn.fetchrow(
                query,
                plan.goal,
                plan.deadline,
                plan.daily_hours,
                0.0  # Initial plan with 0
            )
            return {"message": "Plan successfully created!", "plan": new_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while adding plan: {str(e)}")
    finally:
        await conn.close()


@app.get("/api/v1/plans/", response_model=List[Plan])
async def get_all_plans():
    conn = await get_database()
    try:
        # Recuperar todos os planos
        query = "SELECT * FROM plan"
        rows = await conn.fetch(query)
        plans = [dict(row) for row in rows]
        return plans
    finally:
        await conn.close()

@app.get("/api/v1/plans/{id}", response_model=Plan)
async def get_plan_by_id(id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM plan WHERE id = $1"
        plan = await conn.fetchrow(query, id)
        if plan is None:
            raise HTTPException(status_code=404, detail="Plan not found.")
        return dict(plan)
    finally:
        await conn.close()

@app.delete("/api/v1/plans/")
async def reset_plans():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "study-plan database resetted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while resetting study-plan database: {str(e)}")
    finally:
        await conn.close()

@app.delete("/api/v1/plans/{id}")
async def delete_plan_by_id(id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM plan WHERE id = $1"
        plan = await conn.fetchrow(query, id)
        if plan is None:
            raise HTTPException(status_code=404, detail="Plan not found.")
        delete_query = "DELETE FROM plan WHERE id = $1"
        await conn.execute(delete_query, id)
        return {"message": "Plan removed successfully!"}
    finally:
        await conn.close()

