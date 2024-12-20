from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from schemas import Plan, CreatePlan, UpdatePlan, Task, CreateTask, UpdateTask
from llm_integration import generateTasks
from typing import List
import time
import os
import asyncpg

DAYS_IN_WEEK = 7

# Get database connection
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/study-plan") 
    return await asyncpg.connect(DATABASE_URL)

async def startDB():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "study-plan database resetted successfully!"}
    except Exception as e:
        return {"error": f"Failed to initialize the database: {str(e)}"}
    finally:
        await conn.close()

# Start FastAPI application
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    result = await startDB()
    print(result)

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
        query_plan = """
        INSERT INTO plan (goal, deadline, daily_hours, created_at, progress)
        VALUES ($1, $2, $3, NOW(), $4)
        RETURNING *;
        """

        query_task = """
        INSERT INTO task (plan_id, description, week, completed)
        VALUES ($1, $2, $3, $4);
        """

        async with conn.transaction():
            new_plan = await conn.fetchrow(
                query_plan,
                plan.goal,
                plan.deadline,
                plan.daily_hours,
                0.0  # Initial plan with 0
            )
        
        current_date = datetime.now().date() 

        number_of_weeks = ((plan.deadline - current_date).days)/DAYS_IN_WEEK

        prompt = f"""
            Generate a study plan for {plan.goal}.
            The daily time for studying is {time}.
            The number of weeks is {number_of_weeks}.
         """
         
        tasks = generateTasks(prompt)
        
        async with conn.transaction():
            for task in tasks:
                await conn.fetchrow(
                    query_task,
                    new_plan['id'],
                    task['description'],
                    task['week'],
                    False
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
        query = "SELECT * FROM plan ORDER BY plan.id"
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

@app.patch("/api/v1/plans/{plan_id}", status_code=200)
async def update_plan(plan_id: int, updated_plan: UpdatePlan):
    conn = await get_database()
    try:
        query_check_plan = "SELECT * FROM plan WHERE id = $1"
        plan_exists = await conn.fetchrow(query_check_plan, plan_id)
        if not plan_exists:
            raise HTTPException(status_code=404, detail="Plan not found.")

        query_update_plan = """
        UPDATE plan
        SET goal = COALESCE($1, goal), 
            deadline = COALESCE($2, deadline), 
            daily_hours = COALESCE($3, daily_hours), 
            progress = COALESCE($4, progress)
        WHERE id = $5
        RETURNING *;
        """
        updated_plan_data = await conn.fetchrow(
            query_update_plan,
            updated_plan.goal,
            updated_plan.deadline,
            updated_plan.daily_hours,
            updated_plan.progress,
            plan_id,
        )

        return {"message": "Plan updated successfully!", "task": dict(updated_plan_data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while updating plan: {str(e)}")
    finally:
        await conn.close()

@app.delete("/api/v1/plans/")
async def reset_plans():
    try:
        await startDB()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while resetting study-plan database: {str(e)}")


@app.delete("/api/v1/plans/{id}")
async def delete_plan_by_id(id: int):
    conn = await get_database()
    try:
        query_check_plan = "SELECT * FROM plan WHERE id = $1"
        plan = await conn.fetchrow(query_check_plan, id)
        if plan is None:
            raise HTTPException(status_code=404, detail="Plan not found.")
        query_delete_plan = "DELETE FROM plan WHERE id = $1"
        await conn.execute(query_delete_plan, id)
        return {"message": "Plan removed successfully!"}
    finally:
        await conn.close()

@app.post("/api/v1/plans/{plan_id}/tasks/", status_code=201)
async def add_task(plan_id: int, task: CreateTask):
    conn = await get_database()
    try:
        query_check_plan = "SELECT * FROM plan WHERE id = $1"
        plan_exists = await conn.fetchrow(query_check_plan, plan_id)
        if not plan_exists:
            raise HTTPException(status_code=404, detail="Plan not found.")

        query = """
        INSERT INTO task (plan_id, description, week, completed)
        VALUES ($1, $2, $3, $4)
        RETURNING *;
        """
        async with conn.transaction():
            new_task = await conn.fetchrow(
                query,
                plan_id,
                task.description,
                task.week,
                task.completed
            )
            return {"message": "Task successfully created!", "task": dict(new_task)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while adding task: {str(e)}")
    finally:
        await conn.close()

@app.get("/api/v1/plans/{plan_id}/tasks/", response_model=List[Task], status_code=200)
async def get_tasks(plan_id: int):
    conn = await get_database()
    try:
        query_check_plan = "SELECT * FROM plan WHERE id = $1"
        plan_exists = await conn.fetchrow(query_check_plan, plan_id)
        if not plan_exists:
            raise HTTPException(status_code=404, detail="Plan not found.")

        query = "SELECT * FROM task WHERE plan_id = $1 ORDER BY task.id"
        rows = await conn.fetch(query, plan_id)
        tasks = [dict(row) for row in rows]
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while getting tasks: {str(e)}")
    finally:
        await conn.close()

@app.patch("/api/v1/plans/{plan_id}/tasks/{task_id}", status_code=200)
async def update_task(plan_id: int, task_id: int, updated_task: UpdateTask):
    conn = await get_database()
    try:
        query_check_plan = "SELECT * FROM plan WHERE id = $1"
        plan_exists = await conn.fetchrow(query_check_plan, plan_id)
        if not plan_exists:
            raise HTTPException(status_code=404, detail="Plan not found.")

        query_check_task = "SELECT * FROM task WHERE id = $1 AND plan_id = $2"
        task_exists = await conn.fetchrow(query_check_task, task_id, plan_id)
        if not task_exists:
            raise HTTPException(status_code=404, detail="Task not found.")

        query_update_task = """
        UPDATE task
        SET description = COALESCE($1, description), 
            week = COALESCE($2, week), 
            completed = COALESCE($3, completed)
        WHERE id = $4 AND plan_id = $5
        RETURNING *;
        """
        updated_task_data = await conn.fetchrow(
            query_update_task,
            updated_task.description,
            updated_task.week,
            updated_task.completed,
            task_id,
            plan_id
        )

        return {"message": "Task updated successfully!", "task": dict(updated_task_data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while updating task: {str(e)}")
    finally:
        await conn.close()

@app.delete("/api/v1/plans/{plan_id}/tasks/{task_id}", status_code=200)
async def delete_task(plan_id: int, task_id: int):
    conn = await get_database()
    try:
        query_check_plan = "SELECT * FROM plan WHERE id = $1"
        plan_exists = await conn.fetchrow(query_check_plan, plan_id)
        if not plan_exists:
            raise HTTPException(status_code=404, detail="Plan not found.")

        query_check_task = "SELECT * FROM task WHERE id = $1 AND plan_id = $2"
        task_exists = await conn.fetchrow(query_check_task, task_id, plan_id)
        if not task_exists:
            raise HTTPException(status_code=404, detail="Task not found.")

        query_delete_task = "DELETE FROM task WHERE id = $1 AND plan_id = $2;"

        await conn.fetchrow(
            query_delete_task,
            task_id,
            plan_id
        )

        return {"message": "Task deleted successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed while deleting task: {str(e)}")
    finally:
        await conn.close()