import psycopg2.extras

def get_by_id(id):
    from workstory import db

    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
                SELECT id, content, created_at, status
                FROM task
                WHERE id = %s
                """, (id, ))
    return cur.fetchone()
