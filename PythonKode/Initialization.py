import sqlite3
import Database

def innitialise():
    databaseConnection = sqlite3.connect(Database.pathToGameFolder('Databases')+'/Database.db')

    # Create a cursor object
    cursor = databaseConnection.cursor()

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
                    flavorTextId INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS flavortextTable (
                    flavortextId INTEGER PRIMARY KEY,
                    flavorText TEXT)''')
    
    # Insert or update data into the table
    # piece_data = (pieceId, pieceName, north, east, south, west, artPath, effektId, flavorText)

    cursor.execute('''INSERT OR REPLACE INTO pieces(pieceId, pieceName, north, east, south, west, artPath, effektId, flavorTextId) VALUES
                (1, 'Totally unicorn', 3, 1, 0, 1, 'totallyUnicorn', 0, 1),
                (2, 'Fire Breathing Unicorn', 1, 3, 1, 2, 'FireBreathingUnicorn', 3, 2),
                (3, 'Normie', 1, 2, 1, 2, 'Normiecorn', 1, 3), 
                (4, 'Coolicorn', 0, 1, 3, 1, 'CoolUnicorn', 0, 4), 
                (5, 'Ice breathing Unicorn', 1, 2, 1, 3, 'FrostUnicorn', 0, 5), 
                (6, 'Big Corn', 4, 1, 4, 1, 'BigCorn', 0, 6), 
                (7, 'Unicake', 2, 2, 2, 2, 'Unicake',0, 7), 
                (8, 'Sleepiecorn', 1, 2, 4, 1, 'SleepyUnicorn', 0, 8), 
                (9, 'Sea Unicorn', 1, 2, 3, 3, 'SeaUnicorn', 0, 9), 
                (10, 'Rainbowsprint', 1, 1, 3, 2, 'RainbowSprint', 2, 10), 
                (11, 'Bicorn', 1, 4, 1, 4, 'BiCorn', 0, 11);'''
                )
    
    cursor.execute('''INSERT OR REPLACE INTO flavortextTable(flavortextId, flavorText) VALUES
                   
                   (1, 'You can be anything you want to be!'),
                   (2, 'Attacks 2 tiles away'),
                   (3, 'Wait, jeg troede dette var lol'),
                   (4, '*sunglasses*'),
                   (5, 'Refreshing in summer'),
                   (6, 'One of a kind'),
                   (7, 'Mums!'),
                   (8, 'Nimble like a cat, and sleepy too'),
                   (9, 'Very nimble in the sea'),
                   (10, 'Legally distinct'),
                   (11, 'Twice as magical');''')
    
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
    databaseConnection.commit()

    # Close cursor and connection
    cursor.close()
    databaseConnection.close()
if __name__== "__main__":
    innitialise()