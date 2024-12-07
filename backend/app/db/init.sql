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

INSERT INTO plan (goal, deadline, daily_hours, progress) VALUES
('Learn PostgreSQL', '2024-12-31', 2, 0.5),
('Develop a personal project', '2025-03-15', 3, 0.333),
('Complete React course', '2024-12-20', 1, 0.5);

INSERT INTO task (plan_id, description, week, completed) VALUES
(1, 'Watch introductory SQL lessons', 1, TRUE),
(1, 'Practice basic queries in the database', 2, FALSE),
(2, 'Define project scope', 1, TRUE),
(2, 'Create initial wireframes', 2, FALSE),
(2, 'Implement authentication', 5, FALSE),
(3, 'Complete hooks module', 1, TRUE),
(3, 'Create final project', 3, FALSE);
