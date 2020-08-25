import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, \
                        drop_staging_only_table_queries, qc_queries


def load_staging_tables(cur, conn):
    """
    Execute Copy Table queries to fill staging tables.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    for query in copy_table_queries:
        print(query['desc'])
        cur.execute(query['q'])
        conn.commit()

def insert_tables(cur, conn):
    """
    Execute Insert Table queries to fill galaxy schema tables.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    for query in insert_table_queries:
        print(query['desc'])
        cur.execute(query['q'])
        conn.commit()

def fact_count_check(cur):
    """
    Compare row count for fact tables based on staging tables.

    Arguments:
    cur - DB connection cursor
    """
    for query in qc_queries:
        print(query['desc'])
        cur.execute(query['count_source'])
        count_source = (cur.fetchall()[0][0])
        cur.execute(query['count_dest'])
        count_dest = (cur.fetchall()[0][0])
        diff = count_source - count_dest
        if diff > 0:
            print('Row count does not match. Source: {}, Dest: {}, Diff: {}'
                  .format(count_source, count_dest, diff))
        else:
            print('Row count quality check passed')

def drop_staging_tables(cur, conn):
    """
    Execute Drop Table queries for staging tables only.

    Arguments:
    cur - DB connection cursor
    conn - DB connection object
    """
    print("Drop all staging and ref tables")
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
    fact_count_check(cur)
    drop_staging_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
