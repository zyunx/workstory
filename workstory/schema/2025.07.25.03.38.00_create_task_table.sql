CREATE TYPE TASK_STATUS AS ENUM ('TODO', 'IN_PROGRESSING', 'COMPLETE', 'CANCEL');

CREATE TABLE task (
    id VARCHAR(36) PRIMARY KEY,
    content VARCHAR(1000) NOT NULL,
    status TASK_STATUS DEFAULT 'TODO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
