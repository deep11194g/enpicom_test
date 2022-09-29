import os

import psycopg2

from src import get_levenshtein_score

db_conn = psycopg2.connect(
    host=os.environ.get('PGSQL_HOST'),
    port=os.environ.get('PGSQL_PORT'),
    database=os.environ.get('PGSQL_DB'),
    user=os.environ.get('PGSQL_USERNAME'),
    password=os.environ.get('PGSQL_PASSWORD')
)


def insert_dna(sequence):
    """
    Create a new entry in "dna" table with the given sequence

    :param(str) sequence: DNA Sequence string
    :return(int): DNA ID in table
    """
    insert_sql = """
    INSERT INTO dnas(sequence_string)
    VALUES(%s) RETURNING id;
    """
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (sequence,))
    dna_id = cursor.fetchone()[0]
    db_conn.commit()
    cursor.close()
    return dna_id


def fetch_dna(search_term, threshold=0):
    """
    Fetch all DNA sequences matching the `search_term`

    :param(str) search_term: Search Term to match against
    :param(int) threshold: Optional threshold to check against Levenshtein distance
    :return(list of str): List of all (closely) matching sequences
    """
    fetch_sql = "SELECT sequence_string FROM dnas;"
    cursor = db_conn.cursor()
    cursor.execute(fetch_sql)
    matching_sequences = []
    for dna_row in cursor.fetchall():
        if threshold == 0 and dna_row[0] == search_term:
            matching_sequences.append(dna_row[0])
            continue
        lev_score = get_levenshtein_score(search_term, dna_row[0])
        if lev_score <= threshold:
            matching_sequences.append(dna_row[0])
    return matching_sequences

