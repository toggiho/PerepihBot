import sqlite3 as sql
import random

con = sql.connect("data.db")
cur = con.cursor()

def add_user(discord_id, temp_code=random.randint(100000,999999)): #Discord command
    while unicTempCode(temp_code):
        temp_code = random.randint(100000,999999)

    if cur.execute("SELECT discord_id FROM users WHERE discord_id = ?", (discord_id,)).fetchone() is None:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (discord_id, None, True, temp_code))
        con.commit()
        return temp_code


def tempcode_check(temp_code):
    if cur.execute("SELECT temp_code FROM users WHERE temp_code = ?", (temp_code,)).fetchone() is None:
        return False
    else: 
        return True

def add_tg_id(temp_code, tg_id):
    cur.execute("UPDATE users SET telegram_id = ? WHERE temp_code = ?", (tg_id, temp_code))
    #delete temp_code
    #cur.execute("DELETE FROM users WHERE temp_code = ?", (temp_code,))
    con.commit()

def allow_alert(tg_id):
    cur.execute("UPDATE users SET allow_alert = ? WHERE telegram_id = ?", (True, tg_id))
    con.commit()

def deny_alert(tg_id):
    cur.execute("UPDATE users SET allow_alert = ? WHERE telegram_id = ?", (False, tg_id))
    con.commit()

def unicTempCode(temp_code):
    if cur.execute("SELECT temp_code FROM users WHERE temp_code = ?", (temp_code,)).fetchone() is None:
        return False
    else:
        return True
    
def user_exists(discord_id):
    if cur.execute("SELECT discord_id FROM users WHERE discord_id = ?", (discord_id,)).fetchone() is None:
        return False
    else:
        return True

def get_tg_by_discord(discord_id):
    if cur.execute("SELECT discord_id FROM users WHERE discord_id = ?", (discord_id,)).fetchone() is None:
        return None
    return cur.execute("SELECT telegram_id FROM users WHERE discord_id = ?", (discord_id,)).fetchone()[0]

def get_tempcode_by_discord(discord_id):
    return cur.execute("SELECT temp_code FROM users WHERE discord_id = ?", (discord_id,)).fetchone()[0]

def get_tg_by_tempcode(temp_code):
    return cur.execute("SELECT telegram_id FROM users WHERE temp_code = ?", (temp_code,)).fetchone()[0]

def is_discord_id_used(discord_id):
    return cur.execute("SELECT discord_id FROM users WHERE discord_id = ?", (discord_id,)).fetchone() is not None
