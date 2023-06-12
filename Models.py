import sqlite3 as sql


def insertUser(id, name, email, password, password_re_enter):
    con = sql.connect(r"C:\Users\lenovo\Desktop\Preduict_Save_Life\DB\pythonsqlite.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO USER (id,name,email,password,password_re_enter) VALUES (?,?,?,?,?)",
                    (id, name, email, password, password_re_enter))
        con.commit()
        con.close()
        return True
    except:
        return False


def retrieveUsers(id,password):
    con = sql.connect(r"C:\Users\lenovo\Desktop\Preduict_Save_Life\DB\pythonsqlite.db")
    cur = con.cursor()
    cur.execute('SELECT id, password FROM USER WHERE id = ? AND password = ?', (id, password))
    users = cur.fetchall()
    con.close()
    return users


def forgetPassword(name,email):
    con = sql.connect(r"C:\Users\lenovo\Desktop\Preduict_Save_Life\DB\pythonsqlite.db")
    cur = con.cursor()
    cur.execute('SELECT  id, password  FROM USER WHERE name = ? AND email = ?', (name,email))
    users = cur.fetchall()
    con.close()
    return users