DROP TABLE IF EXISTS "task";
DROP TABLE IF EXISTS "plan";

CREATE TABLE IF NOT EXISTS plan (
    id SERIAL PRIMARY KEY,                 
    goal TEXT NOT NULL,                  
    deadline DATE NOT NULL,              
    daily_hours INTEGER NOT NULL,        
    created_at TIMESTAMP DEFAULT NOW(),  
    progress FLOAT DEFAULT 0.0           
);

CREATE TABLE IF NOT EXISTS task (
    id SERIAL PRIMARY KEY,                  
    plan_id INTEGER NOT NULL,                 
    description TEXT NOT NULL,             
    week INTEGER NOT NULL,                 
    completed BOOLEAN DEFAULT FALSE,       
    FOREIGN KEY (plan_id) REFERENCES plan(id) ON DELETE CASCADE
);

