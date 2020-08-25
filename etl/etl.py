import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, \
                        drop_staging_only_table_queries


def load_staging_tables(cur, conn):
    """
    Execute Copy Table queries to fill staging tables.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Execute Insert Table queries to fill galaxy schema tables.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def drop_staging_tables(cur, conn):
    """
    Execute Drop Table queries for staging tables only.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    for query in drop_staging_only_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """Connect to Redshift and execute etl process for S3 song and log files."""
    # read config file
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # connect to Redshift
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
                   .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    # execute queries
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)
    #drop_staging_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
