import json
import psycopg2.extras

def create_event(db, id, event_type, event_content):
    cur = db.cursor()
    cur.execute("""
                INSERT INTO event (id, event_type, event_content) VALUES (%s, %s, %s)
                """, (id, event_type, json.dumps(event_content)))
    cur.close()
    
def get_all_events(db):
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
                SELECT sn, id, event_type, event_content, happen_at FROM event ORDER BY sn
                """)
    all_events = [dict(r) for r in cur.fetchall()]
    cur.close()
    return all_events
