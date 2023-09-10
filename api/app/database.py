import psycopg2
import os
import traceback

def connect():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password= os.getenv("POSTGRES_PASSWORD"))
        return conn
    except Exception:
        traceback.print_exc()

def create_question(question_id, title, description, category, complexity):
    try:
        conn = connect()
        with conn, conn.cursor() as cur:
            cur.execute("INSERT INTO questions (question_id, title, description, category, complexity) VALUES (%s, %s, %s, %s, %s)", (question_id, title, description, category, complexity))
            conn.commit()
            return True
    except Exception:
        traceback.print_exc()
        return False

def get_question(question_id):
    try:
        conn = connect()
        FIELD_NAMES = ['question_id', 'title', 'description', 'category', 'complexity']

        with conn, conn.cursor() as cur:
            if question_id == "all":
                cur.execute(f"SELECT {', '.join(FIELD_NAMES)} FROM questions")
                rows = cur.fetchall()
                questions = [dict(zip(FIELD_NAMES, row)) for row in rows]
                return questions

            cur.execute(f"SELECT {', '.join(FIELD_NAMES)} FROM questions WHERE question_id = %s", (question_id,))
            row = cur.fetchone()
            if row is None:
                return False
            question = dict(zip(FIELD_NAMES, row))
            return question
    except Exception:
        traceback.print_exc()

def update_question_info(question_id, title, description, category, complexity):
    values = []
    set_clauses = []

    if title is not None:
        values.append(title)
        set_clauses.append("title = %s")

    if description is not None:
        values.append(description)
        set_clauses.append("description = %s")

    if category is not None:
        values.append(category)
        set_clauses.append("category = %s")

    if complexity is not None:
        values.append(complexity)
        set_clauses.append("complexity = %s")

    set_clause = ", ".join(set_clauses)
    if not set_clause:
        return False

    values.append(question_id)

    try:
        conn = connect()
        with conn, conn.cursor() as cur:
            cur.execute(f"""UPDATE questions
                        SET {set_clause}
                        WHERE question_id = %s""",
                        tuple(values))
            return True
    except Exception:
        traceback.print_exc()
        return False

def delete_question(question_id):
    try:
        conn = connect()
        with conn, conn.cursor() as cur:
            if question_id == "all":
                cur.execute("DELETE FROM questions")
            else:
                cur.execute("DELETE FROM questions WHERE question_id = %s", (question_id,))
            conn.commit()
            return True
    except Exception:
        traceback.print_exc()
        return False
