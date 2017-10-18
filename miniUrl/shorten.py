import sqlite3
from time import time, sleep
from datetime import timedelta
from encode import encode, decode


QUERY_RETRIEVE_TARGET = '''
    select targetUrl, typeId
    from miniUrls m
         join targetUrls t on m.id = t.miniUrlId
         join targetTypes tt on t.typeId = tt.id 
    where m.id = ? and tt.type IN ('default', ?)
    order by case tt.type when 'default' then 1 else 0 end
    limit 1;'''

QUERY_GET_STATS = '''
    select m.id, createdTimestamp, t.targetUrl, tt.type, hits
    from miniUrls m 
         join targetUrls t on m.id = t.miniUrlId 
         join targetTypes tt on t.typeId = tt.id 
    order by m.id'''

QUERY_UPDATE_HITS = '''
    update targetUrls
    set hits = hits + 1
    where miniUrlId = ? and typeId = ?'''


def add_mini_url(db, targets, base_url):
    """
    Adds a row to miniUrls table for the new miniUrl, retrieves the id of the
    inserted row, then use the new id to insert new rows for one or more redirect
    targets. Encodes the id as a base 62 string and returns the new mini_url

    Since db here is SQLite, calculation of the createdTimestamp for the inserted
    row is performed in the script rather than on the db (since sqlite is a local
    db the times should be identical)

    Query is wrapped in a transaction to prevent storing of partial information
    SQL injection is protected against both by previous json validation against
    request.schema and by passing parameters to the cursor's execute method (rather
    than using python string.format)

    Use of executescript is not possible here because it does not allow for safe
    parameter passing and because the inserted row id for the mini url must be
    cached mid-SQL
    :param db: connection to db
    :param targets: object containing urls for each device as key value pairs
    :param base_url: base for mini url
    :return: new mini url
    """
    try:
        cursor = db.cursor()
        cursor.execute('begin transaction')
        cursor.execute('insert into miniUrls (createdTimestamp) values (?)', (int(time()),))
        cursor.execute('select last_insert_rowid()')
        mini_url_id = cursor.fetchone()[0]
        values = [[targets[device], device] for device in targets]
        cursor.execute('drop table if exists targets')
        cursor.execute('create temp table targets (integer, url text, type text)')
        cursor.executemany('insert into targets (url, type) values(?, ?)', values)
        cursor.execute('''insert into targetUrls (miniUrlId, targetUrl, typeId)
                          select ?, t.url, tt.Id
                          from targets t join targetTypes tt on t.type = tt.type''',
                          (int(mini_url_id),))
        cursor.execute('commit')
        return create_url(mini_url_id, base_url)
    except sqlite3.Error:
        cursor.execute('rollback')
        raise


def get_stats(db, base_url):
    """
    Returns stats for all stored mini urls as a dictionary of dictionaries
    Runs a query joining the miniUrls table with the targetUrls table, then iterates over
    each row, storing each mini url as a key in a dictionary and creating a dictionary for that key
    to store its age and a list of targets
    :param db: db connection
    :param base_url:
    :return: dictionary (key: mini url; value: dictionary with keys 'age' and 'targets')
    """
    cursor = db.cursor()
    cursor.execute(QUERY_GET_STATS)
    rows = cursor.fetchall()
    stats = {}
    now = int(time())
    for row in rows:
        mini_url = create_url(row[0], base_url)
        if mini_url not in stats:
            stats[mini_url] = { "age": str(timedelta(seconds=now - row[1])),
                                "targets": []}
        stats[mini_url]['targets'].append(
            {"target": row[2], "type": row[3], "hits": row[4]}
        )
    return stats


def retrieve_url(db, mini_url, device):
    """
    Decodes the mini url to its id, then runs a query returning the appropriate target url.
    The query returns the device specific target url if available or the default url if not
    :param db: database connection
    :param mini_url: the mini url
    :param device: one of 'mobile', 'tablet' or 'default'
    :return: target url for redirect, None if mini_url not found in db
    """
    cursor = db.cursor()
    try:
        mini_url_id = decode(mini_url)
    except ValueError:
        return None
    cursor.execute(QUERY_RETRIEVE_TARGET, (mini_url_id, device))
    row = cursor.fetchone()
    if row is None:
        return None
    else:
        cursor.execute(QUERY_UPDATE_HITS, (mini_url_id, row[1]))
        return row[0]


def create_url(mini_url_id, base_url):
    return base_url + encode(mini_url_id)


