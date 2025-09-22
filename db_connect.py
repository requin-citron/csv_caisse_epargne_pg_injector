from os import environ

from psycopg2 import pool

# Initialisation du pool (au chargement du module)
try:
    db_pool = pool.ThreadedConnectionPool(
        minconn=int(environ.get("DB_POOL_MINCONN", 1)),
        maxconn=int(environ.get("DB_POOL_MAXCONN", 30)),
        dbname=environ.get("DB_NAME", "agrosync"),
        user=environ.get("DB_USER", "postgres"),
        password=environ.get("DB_PASSWORD", "postgres"),
        host=environ.get("DB_HOST", "localhost"),
        port=environ.get("DB_PORT", "5432")
    )
except Exception as e:
    db_pool = None

def get_db_connection():
    """
    Récupère une connexion depuis le pool.
    N'oubliez pas de la restituer via release_db_connection().
    """
    if not db_pool:
        return None
    try:
        return db_pool.getconn()
    except Exception as e:
        return None

def release_db_connection(conn):
    """
    Restitue la connexion dans le pool.
    """
    if not db_pool or conn is None:
        return None
    try:
        db_pool.putconn(conn)
    except Exception as e:
        return None

def insert_transaction(transaction: dict) -> bool:
    """
    Insère une transaction dans la base de données.
    """
    conn = get_db_connection()
    flag = True
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bank_transactions (date_comptabilisation, libelle_simplifie, libelle_operation, reference, information, type_operation, categorie, sous_categorie, debit, credit, date_operation, date_de_valeur, pointage_operation)
            VALUES (%s                                     ,%s                               , %s                              , %s                      , %s                                         , %s                           , %s                      , %s                           , %s                  , %s                   , %s                           , %s                           , %s               )
        """,       (transaction['Date de comptabilisation'], transaction['Libelle simplifie'], transaction['Libelle operation'], transaction['Reference'], transaction['Informations complementaires'], transaction['Type operation'], transaction['Categorie'], transaction['Sous categorie'], transaction['Debit'], transaction['Credit'], transaction['Date operation'], transaction['Date de valeur'], transaction['Pointage operation']))
        conn.commit()

    except Exception as e:
        conn.rollback()
        flag = False

    cursor.close()
    release_db_connection(conn)
    return flag


