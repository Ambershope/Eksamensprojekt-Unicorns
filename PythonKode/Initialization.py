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

    cursor.execute('''INSERT OR REPLACE INTO pieces(pieceId, pieceName, north, east, south, west, artPath, effektId, flavorText) VALUES
                (1, 'Totally unicorn', 3, 1, 0, 1, 'totallyUnicorn', 0, 'You can be anything you want to be!'),
                (2, 'Fire Breathing Unicorn', 1, 3, 1, 2, 'FireBreathingUnicorn', 3, 'Attacks 2 tiles away'),
                (3, 'Normie', 0, 0, 0, 0, 'Normiecorn', 1, 'Wait, jeg troede dette var lol'), 
                (4, 'Coolicorn', 0, 1, 3, 1, 'CoolUnicorn', 0, '*sunglasses*'), 
                (5, 'Ice breathing Unicorn', 1, 2, 1, 3, 'FrostUnicorn', 0, 'Refreshing in summer'), 
                (6, 'Big Corn', 4, 1, 4, 1, 'BigCorn', 0, 'One of a kind'), 
                (7, 'Unicake', 2, 2, 2, 2, 'Unicake',0, 'Mums!'), 
                (8, 'Sleepiecorn', 1, 2, 4, 1, 'SleepyUnicorn', 0, 'Nimble like a cat, and sleepy too'), 
                (9, 'Sea Unicorn', 1, 2, 3, 3, 'SeaUnicorn', 0, 'Very nimble in the sea'), 
                (10, 'Rainbowsprint', 1, 1, 3, 2, 'RainbowSprint', 2, 'Legally distinct'), 
                (11, 'Bicorn', 1, 4, 1, 4, 'BiCorn', 0, 'Twice as magical');'''
                )
    # (https://stockcake.com/i/majestic-horse-posing_720055_761979)
    # (https://stockcake.com/i/fiery-unicorn-blaze_234695_44744)
    # (https://stockcake.com/i/majestic-unicorn-magic_176901_30135)
    # Anna har tegnet og givet os copyright på dette billede
    # (https://stockcake.com/i/mystical-unicorn-scene_828530_804034)
    # (https://animalia.bio/white-rhinoceros)
    # Har fået billedet fra free image librariet Stockcake.com (https://stockcake.com/i/unicorn-cupcake-delight_134375_15991)
    # (https://stockcake.com/i/whimsical-unicorn-bedroom_575124_928066)
    # (https://www.deviantart.com/pulchridude/art/Lil-Narwhal-783280497)
    # (https://stockcake.com/i/majestic-sky-unicorn_815280_976023)
    # (https://stockcake.com/i/bull-in-motion_753655_971346)
    
    # Effekt 0: No effect
    # Effekt 1: (normie aura): Reduce attack of surrounding Unicorns to 1
    # Effekt 2: (legendary )Removes all other [Cardname] from the battlefield     #
    # Effekt 3: Attacks 2 tiles from tile     #done
    # Template (id, 'Name', north, east, south, west, artpath, effektId, 'flavorText'),

    # Commit changes
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()
if __name__== "__main__":
    innitialise()