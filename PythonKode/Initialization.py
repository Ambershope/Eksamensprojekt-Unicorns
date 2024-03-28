import sqlite3
import Database

def innitialise():
    conn = sqlite3.connect(Database.pathToGameFolder('Databases')+'/Database.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS pieces (
                    pieceId INTEGER PRIMARY KEY,
                    pieceName TEXT NOT NULL,
                    north INTEGER,
                    east INTEGER,
                    south INTEGER,
                    west INTEGER,
                    artPath TEXT NOT NULL,
                    effektId INTEGER,
                    flavorText TEXT)''')

    # Insert or update data into the table
    # piece_data = (1, 'Fluttershy', 3, 1, 0, 1, 'Fluttershy_Main_Box', 0, 'Cute and bubbly')
    # cursor.execute("INSERT OR REPLACE INTO pieces(pieceId, pieceName, north, east, south, west, artPath, effektId, flavorText) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", piece_data)

    cursor.execute("INSERT OR REPLACE INTO pieces(pieceId, pieceName, north, east, south, west, artPath, effektId, flavorText) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (1, 'Fluttershy', 3, 1, 0, 1, 'Fluttershy_Main_Box', 0, 'Cute and bubbly'),
                (id, 'piecename', north, east, south, west, 'artPath', effektId, 'flavorText'),
                (id, 'piecename', north, east, south, west, 'artPath', effektId, 'flavorText'),
                (id, 'piecename', north, east, south, west, 'artPath', effektId, 'flavorText'),
                (id, 'piecename', north, east, south, west, 'artPath', effektId, 'flavorText'),
                (id, 'piecename', north, east, south, west, 'artPath', effektId, 'flavorText'),
                )

    # Commit changes
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()
if __name__== "__main__":
    innitialise()