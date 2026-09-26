import sqlite3
from pathlib import Path
from datetime import datetime


# ============================================================
# SAMAADHAN AI - DATABASE
# SQLite database for problems, capabilities, stakeholders,
# collaborations, members and tasks.
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "samaadhan.db"


def get_connection():
    """Create and return a SQLite database connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    """Create all required database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # Problems
    # --------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            source TEXT,
            domain_key TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # Capabilities
    # --------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS capabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            domain_key TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # Stakeholders
    # --------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stakeholders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            partner_type TEXT NOT NULL,
            domain_key TEXT NOT NULL,
            capabilities TEXT NOT NULL,
            location TEXT,
            contact_person TEXT,
            email TEXT,
            description TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # Collaborations
    # --------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collaborations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            domain_key TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (problem_id) REFERENCES problems(id)
        )
    """)

    # --------------------------------------------------------
    # Collaboration Members
    # --------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collaboration_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collaboration_id INTEGER NOT NULL,
            stakeholder_id INTEGER,
            name TEXT NOT NULL,
            partner_type TEXT NOT NULL,
            role TEXT NOT NULL,
            added_at TEXT NOT NULL,
            FOREIGN KEY (collaboration_id)
                REFERENCES collaborations(id),
            FOREIGN KEY (stakeholder_id)
                REFERENCES stakeholders(id)
        )
    """)

    # --------------------------------------------------------
    # Tasks
    # --------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collaboration_id INTEGER NOT NULL,
            label TEXT NOT NULL,
            status TEXT NOT NULL,
            task_order INTEGER NOT NULL,
            FOREIGN KEY (collaboration_id)
                REFERENCES collaborations(id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# PROBLEM FUNCTIONS
# ============================================================

def add_problem(
    title,
    description,
    category,
    location,
    source,
    domain_key
):
    """Add a new societal problem."""

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO problems
        (
            title,
            description,
            category,
            location,
            source,
            domain_key,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        category,
        location,
        source,
        domain_key,
        created_at
    ))

    problem_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return problem_id


def get_problem(problem_id):
    """Get one problem by ID."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM problems WHERE id = ?",
        (problem_id,)
    )

    problem = cursor.fetchone()

    connection.close()

    return problem


# ============================================================
# CAPABILITY FUNCTIONS
# ============================================================

def add_capability(label, domain_key):
    """Add a capability."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO capabilities
        (label, domain_key)
        VALUES (?, ?)
    """, (label, domain_key))

    connection.commit()
    connection.close()


def get_capabilities(domain_key):
    """Return capabilities for a specific domain."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM capabilities
        WHERE domain_key = ?
        ORDER BY id
    """, (domain_key,))

    capabilities = cursor.fetchall()

    connection.close()

    return capabilities


# ============================================================
# STAKEHOLDER FUNCTIONS
# ============================================================

def add_stakeholder(
    name,
    partner_type,
    domain_key,
    capabilities,
    location="",
    contact_person="",
    email="",
    description=""
):
    """Add a university, expert or industry partner."""

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO stakeholders
        (
            name,
            partner_type,
            domain_key,
            capabilities,
            location,
            contact_person,
            email,
            description,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        partner_type,
        domain_key,
        capabilities,
        location,
        contact_person,
        email,
        description,
        created_at
    ))

    stakeholder_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return stakeholder_id


def get_stakeholders(domain_key=None):
    """Return stakeholders, optionally filtered by domain."""

    connection = get_connection()
    cursor = connection.cursor()

    if domain_key:
        cursor.execute("""
            SELECT *
            FROM stakeholders
            WHERE domain_key = ?
            ORDER BY id
        """, (domain_key,))
    else:
        cursor.execute("""
            SELECT *
            FROM stakeholders
            ORDER BY id
        """)

    stakeholders = cursor.fetchall()

    connection.close()

    return stakeholders


def get_stakeholder(stakeholder_id):
    """Get one stakeholder by ID."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM stakeholders WHERE id = ?",
        (stakeholder_id,)
    )

    stakeholder = cursor.fetchone()

    connection.close()

    return stakeholder


# ============================================================
# COLLABORATION FUNCTIONS
# ============================================================

def create_collaboration(problem_id, domain_key, status="active"):
    """Create a collaboration for a problem."""

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO collaborations
        (
            problem_id,
            domain_key,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        problem_id,
        domain_key,
        status,
        created_at
    ))

    collaboration_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return collaboration_id


def add_collaboration_member(
    collaboration_id,
    name,
    partner_type,
    role,
    stakeholder_id=None
):
    """Add a stakeholder to a collaboration."""

    connection = get_connection()
    cursor = connection.cursor()

    added_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO collaboration_members
        (
            collaboration_id,
            stakeholder_id,
            name,
            partner_type,
            role,
            added_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        collaboration_id,
        stakeholder_id,
        name,
        partner_type,
        role,
        added_at
    ))

    connection.commit()
    connection.close()


def get_collaboration_members(collaboration_id):
    """Get all members of a collaboration."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM collaboration_members
        WHERE collaboration_id = ?
        ORDER BY id
    """, (collaboration_id,))

    members = cursor.fetchall()

    connection.close()

    return members


# ============================================================
# TASK FUNCTIONS
# ============================================================

def add_task(
    collaboration_id,
    label,
    status,
    task_order
):
    """Add a task to a collaboration."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (
            collaboration_id,
            label,
            status,
            task_order
        )
        VALUES (?, ?, ?, ?)
    """, (
        collaboration_id,
        label,
        status,
        task_order
    ))

    connection.commit()
    connection.close()


def get_tasks(collaboration_id):
    """Get all tasks for a collaboration."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE collaboration_id = ?
        ORDER BY task_order
    """, (collaboration_id,))

    tasks = cursor.fetchall()

    connection.close()

    return tasks


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

if __name__ == "__main__":
    init_database()
    print("SAMAADHAN AI database initialized successfully.")
    print(f"Database location: {DB_PATH}")