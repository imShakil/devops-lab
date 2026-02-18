import ldap3
import psycopg2
from psycopg2 import sql

# LDAP connection settings
LDAP_SERVER = "ldaps://192.168.0.144:1636"
LDAP_BASE_DN = "o=gluu"
LDAP_BIND_DN = "cn=directory manager"
LDAP_PASSWORD = "#####"

# PostgreSQL connection settings
PG_HOST = "192.168.0.145"
PG_PORT = "5432"
PG_DATABASE = "gluudb"
PG_USER = "gluu"
PG_PASSWORD = "#####"

def connect_ldap():
    server = ldap3.Server(LDAP_SERVER, use_ssl=True, get_info=ldap3.ALL)
    ldap_conn = ldap3.Connection(server, LDAP_BIND_DN, LDAP_PASSWORD, auto_bind=True, client_strategy='SYNC')
    ldap_conn.open()
    ldap_conn.bind()
    return ldap_conn
 
def connect_postgresql():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )

def extract_ldap_data(ldap_conn):
    search_filter = "(objectClass=*)"
    attributes = ["*"]
    print("searching for data")
    ldap_conn.search(
        search_base=LDAP_BASE_DN,
        search_scope=ldap3.SUBTREE,
        search_filter=search_filter,
        attributes=attributes
    )
    print("data extracted")
    for entry in ldap_conn.response:
        print(entry)
    return ldap_conn.response   

def transform_data(ldap_data):
    print("transforming data")
    transformed_data = []
    for dn, attrs in ldap_data:
        record = {
            "dn": dn,
            "attributes": {k: v[0].decode() if isinstance(v[0], bytes) else v[0] for k, v in attrs.items() if v}
        }
        transformed_data.append(record)
    print("data transformed")
    return transformed_data

def create_table(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ldap_data (
                id SERIAL PRIMARY KEY,
                dn TEXT,
                attributes JSONB
            )
        """)
    pg_conn.commit()

def load_data_to_postgresql(pg_conn, transformed_data):
    with pg_conn.cursor() as cur:
        for record in transformed_data:
            cur.execute(
                sql.SQL("INSERT INTO ldap_data (dn, attributes) VALUES (%s, %s)"),
                (record["dn"], psycopg2.Json(record["attributes"]))
            )
    pg_conn.commit()

def main():
    ldap_conn = connect_ldap()
    pg_conn = connect_postgresql()

    try:
        ldap_data = extract_ldap_data(ldap_conn)
        print("extracted ldap data: ", ldap_data)
        transformed_data = transform_data(ldap_data)
        print("transformed data: ", transformed_data)
    
        create_table(pg_conn)
        print("created table")
    except Exception as e:
        print(e)


#        load_data_to_postgresql(pg_conn, transformed_data)

#         print("Migration completed successfully.")
#     finally:
#         ldap_conn.unbind_s()
#         pg_conn.close()

if __name__ == "__main__":
    main()
