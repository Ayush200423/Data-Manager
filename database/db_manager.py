from . import conn, c

def create():
    c.execute("""CREATE TABLE IF NOT EXISTS user_verification (
            master_user TEXT,
            salt_verify TEXT,
            master_pass TEXT
        )""")

    c.execute("""CREATE TABLE IF NOT EXISTS user_images (
            master_user TEXT,
            title TEXT,
            description TEXT,
            image BLOB
        )""")

    c.execute("""CREATE TABLE IF NOT EXISTS user_credentials (
            master_user TEXT,
            salt_encrypt TEXT,
            website TEXT,
            user TEXT,
            pass TEXT
        )""")
    return commit()

def insert_record(*args):
    if len(args) == 3:
        c.execute("INSERT INTO user_verification VALUES (?,?,?)", args)
    elif len(args) == 4:
        c.execute("INSERT INTO user_images VALUES (?,?,?,?)", args)
    elif len(args) == 5:
        c.execute("INSERT INTO user_credentials VALUES (?,?,?,?,?)", args)
    return commit()

def read_record(username, type):
    c.execute(f"SELECT * FROM user_{type} WHERE master_user='"+username+"'")
    return c.fetchall()

def delete_record(username, account = None, website = None, title = None):
    if account != None:
        c.execute("DELETE FROM user_verification WHERE master_user='"+username+"'")
        c.execute("DELETE FROM user_credentials WHERE master_user='"+username+"'")
        c.execute("DELETE FROM user_images WHERE master_user='"+username+"'")
    elif website != None:
        if c.execute("SELECT * FROM user_credentials WHERE master_user='"+username+"' AND website = '"+website+"'") == []:
            raise Exception(f"No website found with the name {website}.")
        else:
            c.execute("DELETE FROM user_credentials WHERE master_user = '"+username+"' AND website = '"+website+"'")
    elif title != None:
        if c.execute("SELECT * FROM user_images WHERE master_user='"+username+"' AND title = '"+title+"'") == []:
            raise Exception(f"No image found with the name {title}.")
        else:
            c.execute("DELETE FROM user_images WHERE master_user = '"+username+"' AND title = '"+title+"'")
    return commit()

def commit():
    return conn.commit()

def close_conn():
    return conn.close()