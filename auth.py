import bcrypt
from database import conectar

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

def verificar_senha(senha, senha_hash):
    if isinstance(senha_hash, str):
        senha_hash = senha_hash.encode()
    return bcrypt.checkpw(senha.encode(), senha_hash)

def registrar(username, senha):
    conn = conectar()
    cursor = conn.cursor()

    senha_hash = hash_senha(senha)

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, senha_hash)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def login(username, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM usuarios WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()

    conn.close()

    if user:
        user_id, senha_hash = user
        if verificar_senha(senha, senha_hash):
            return user_id

    return None