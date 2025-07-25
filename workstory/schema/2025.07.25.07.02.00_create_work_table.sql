CREATE TYPE WORK_STATUS AS ENUM ('TODO', 'IN_PROGRESSING', 'COMPLETE', 'CANCEL');

CREATE TABLE work
(
    work_date DATE NOT NULL,
    task_id VARCHAR(36) NOT NULL,
    status WORK_STATUS NOT NULL DEFAULT 'TODO' 
);

CREATE VIEW v_work AS
    SELECT
        work_date, 
        t.content as task_content, 
        w.status
    FROM
        work w join task t on w.task_id = t.id
    WHERE w.work_date = CURRENT_DATE;
