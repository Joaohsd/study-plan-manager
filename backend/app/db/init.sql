DO $$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database
      WHERE datname = 'study-plan'
   ) THEN
      CREATE DATABASE "study-plan";
   END IF;
END
$$;

DROP TABLE IF EXISTS "plan";
DROP TABLE IF EXISTS "task";

CREATE TABLE plan (
    id SERIAL PRIMARY KEY,                 
    goal TEXT NOT NULL,                  
    deadline DATE NOT NULL,              
    daily_hours INTEGER NOT NULL,        
    created_at TIMESTAMP DEFAULT NOW(),  
    progress FLOAT DEFAULT 0.0           
);

CREATE TABLE task (
    id SERIAL PRIMARY KEY,                  
    plan_id INTEGER NOT NULL,                 
    description TEXT NOT NULL,             
    week INTEGER NOT NULL,                 
    completed BOOLEAN DEFAULT FALSE,       
    FOREIGN KEY (plan_id) REFERENCES plan(id) ON DELETE CASCADE
);

