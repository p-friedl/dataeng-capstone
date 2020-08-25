import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Batch drop tables.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Batch create tables.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Connect to Redshift, cleanup and create new tables."""
    # read config file
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # connect to Redshift
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
                   .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    # execute queries
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
