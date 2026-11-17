import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "vulnx.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            target TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence TEXT NOT NULL,
            description TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            evidence TEXT,
            FOREIGN KEY (assessment_id) REFERENCES assessments(id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            expected TEXT NOT NULL,
            actual TEXT NOT NULL,
            passed INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (assessment_id) REFERENCES assessments(id)
        )
        """
    )
    conn.commit()
    conn.close()


class AssessmentStore:
    def __init__(self, path=DB_PATH):
        self.path = path
        init_db()

    def save_assessment(self, mode, target, status):
        conn = sqlite3.connect(self.path)
        cursor = conn.execute(
            "INSERT INTO assessments (mode, target, status) VALUES (?, ?, ?)",
            (mode, target, status),
        )
        assessment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return assessment_id

    def save_finding(self, assessment_id, title, severity, confidence, description, recommendation, evidence):
        conn = sqlite3.connect(self.path)
        conn.execute(
            "INSERT INTO findings (assessment_id, title, severity, confidence, description, recommendation, evidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (assessment_id, title, severity, confidence, description, recommendation, evidence),
        )
        conn.commit()
        conn.close()

    def save_test_result(self, assessment_id, test_name, expected, actual, passed):
        conn = sqlite3.connect(self.path)
        conn.execute(
            "INSERT INTO test_results (assessment_id, test_name, expected, actual, passed) VALUES (?, ?, ?, ?, ?)",
            (assessment_id, test_name, expected, actual, passed),
        )
        conn.commit()
        conn.close()

    def list_assessments(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM assessments ORDER BY id DESC").fetchall()
        conn.close()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at: {DB_PATH}")
