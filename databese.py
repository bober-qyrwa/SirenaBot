import sqlite3

'''----Get func-s----'''


def getUserFromDB():
    conn = sqlite3.connect("us_chat_room_copy.db")
    cursor = conn.cursor()
    cursor.execute(''' SELECT username FROM us_chat_room_copy''')
    data = cursor.fetchall()
    conn.close()
    return data


def getRoomByUsername(username):
    conn = sqlite3.connect("us_chat_room_copy.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT room FROM us_chat_room_copy WHERE username = ?''', (username,))
    result = cursor.fetchone()  # Используем fetchone вместо fetchall
    conn.close()
    return result[0] if result else None  # Возвращаем конкретное значение или None


def getRoomByID(chat_id):  # Переименовал параметр для ясности
    conn = sqlite3.connect("us_chat_room_copy.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT room FROM us_chat_room_copy WHERE chat_id = ?''', (chat_id,))  # Исправлен столбец
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def getIDsFromDB():
    conn = sqlite3.connect("us_chat_room_copy.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT chat_id FROM us_chat_room_copy''')
    data = [row[0] for row in cursor.fetchall()]  # Извлекаем все ID в список
    conn.close()
    return data


'''----Create DB func'''
def create_table():
    connect = sqlite3.connect('us_chat_room_copy.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS us_chat_room_copy (chat_id INTEGER, username TEXT, room TEXT)''')
    connect.commit()
    connect.close()


'''----Create row in DB func----'''
def stack_db(chat_id, username, room):
    try:
        connect = sqlite3.connect('us_chat_room_copy.db')
        cursor = connect.cursor()
        cursor.execute('''INSERT INTO us_chat_room_copy (chat_id, username, room) VALUES (?, ?, ?)''', (chat_id, username, room))
        connect.commit()
        connect.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as goid:
        print(f"Error adding: {goid}")
        return False
