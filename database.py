import sqlite3
import hashlib
import os
import json

DB_FILE = "wanderai.db"

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema for users and saved trips."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create saved_trips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        days INTEGER NOT NULL,
        budget TEXT NOT NULL,
        interests TEXT,
        places_to_visit TEXT,
        itinerary_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    """Securely hash a password using PBKDF2 with salt."""
    if salt is None:
        salt = os.urandom(16).hex()
    
    # Compute password hash
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    
    return pw_hash, salt

def register_user(username, password):
    """Register a new user. Returns (success, message)."""
    username = username.strip().lower()
    if not username or not password:
        return False, "Username and password cannot be empty"
        
    pw_hash, salt = hash_password(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
            (username, pw_hash, salt)
        )
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials. Returns True if valid, False otherwise."""
    username = username.strip().lower()
    if not username or not password:
        return False
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return False
        
    db_hash = row['password_hash']
    salt = row['salt']
    
    test_hash, _ = hash_password(password, salt)
    return test_hash == db_hash

def save_trip(username, source, destination, days, budget, interests, places_to_visit, itinerary_data):
    """Save a generated trip itinerary to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert interests list to string if needed
    if isinstance(interests, list):
        interests_str = ", ".join(interests)
    else:
        interests_str = str(interests)
        
    # If itinerary data is a dict/list, serialize it to JSON
    if isinstance(itinerary_data, (dict, list)):
        itinerary_str = json.dumps(itinerary_data)
    else:
        itinerary_str = str(itinerary_data)
        
    try:
        cursor.execute("""
        INSERT INTO saved_trips (username, source, destination, days, budget, interests, places_to_visit, itinerary_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, source, destination, days, budget, interests_str, places_to_visit, itinerary_str))
        conn.commit()
        return True, "Trip saved successfully!"
    except Exception as e:
        return False, f"Error saving trip: {str(e)}"
    finally:
        conn.close()

def get_saved_trips(username):
    """Retrieve all saved trips for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, source, destination, days, budget, interests, places_to_visit, itinerary_data, created_at
    FROM saved_trips
    WHERE username = ?
    ORDER BY created_at DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    
    trips = []
    for row in rows:
        trips.append({
            "id": row["id"],
            "source": row["source"],
            "destination": row["destination"],
            "days": row["days"],
            "budget": row["budget"],
            "interests": row["interests"],
            "places_to_visit": row["places_to_visit"],
            "itinerary_data": row["itinerary_data"],
            "created_at": row["created_at"]
        })
    return trips

def delete_saved_trip(trip_id, username):
    """Delete a saved trip."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM saved_trips WHERE id = ? AND username = ?", (trip_id, username))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()
