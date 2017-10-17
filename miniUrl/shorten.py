from time import time
from datetime import timedelta
from encode import encode, decode


QUERY_RETRIEVE_TARGET = '''
    select targetUrl, typeId
    from miniUrls m
         join targetUrls t on m.id = t.miniUrlId
         join targetTypes tt on t.typeId = tt.id 
    where m.id = {0} and tt.type IN ('default', '{1}')
    order by case tt.type when 'default' then 1 else 0 end
    limit 1;'''

QUERY_INSERT_MINI = '''
    insert into miniUrls (createdTimestamp) values ({0!s});'''

QUERY_INSERT_TARGETS = '''
    create temp table tempTargets(url text, targetType text);
    insert into tempTargets (url, targetType) values {0};
    insert into targetUrls (miniUrlId, targetUrl, typeId) 
    select {1}, t.url, tt.id 
    from tempTargets t 
         join 
         targetTypes tt on t.targetType = tt.type;
    drop table tempTargets;'''

QUERY_GET_STATS = '''
    select m.id, createdTimestamp, t.targetUrl, hits
    from miniUrls m join targetUrls t on m.id = t.miniUrlId
    order by m.id'''

QUERY_UPDATE_HITS = '''
    update targetUrls
    set hits = hits + 1
    where miniUrlId = '{0}' and typeId = {1}'''


def add_mini_url(db, targets_json, base_url):
    """
    Adds row to miniUrls table for the new miniUrl and commits change.
    Retrieves the id of the inserted row using cursor.lastrowid after commit
    which should avoid issues with concurrency since cursor.lawrowid is a
    connection-specific property. Adds a row to targetUrls table for each supplied
    targetUrl. Encodes the id as a base 62 string and returns the new mini_url
    :param db: connection to db
    :param targets_dict: json object containing urls for each device as key value pairs
    :param base_url: base for mini url
    :return: new mini url
    """
    cursor = db.cursor()
    query = QUERY_INSERT_MINI.format(int(time()))
    cursor.execute(query)
    db.commit()
    mini_url_id = cursor.lastrowid
    values = ["( '{1}', '{0}' )".format(device, targets_json[device]) for device in targets_json]
    query = QUERY_INSERT_TARGETS.format(','.join(values), mini_url_id)
    cursor.executescript(query)
    db.commit()
    return create_url(mini_url_id, base_url)


def stats(db, base_url):
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
            {"target": row[2], "hits": row[3]}
        )
    return stats


def retrieve_url(db, mini_url, device):
    """
    Decodes the mini url to its id, then runs a query returning the appropriate target url.
    The query returns the device specific target url if available or the default url if not
    :param db: database connection
    :param mini_url: the mini url
    :param device: one of 'mobile', 'tablet' or 'default'
    :return: target url for redirect
    """
    cursor = db.cursor()
    mini_url_id = decode(mini_url)
    query = QUERY_RETRIEVE_TARGET.format(mini_url_id, device)
    cursor.execute(query)
    row = cursor.fetchone()
    if row is not None:
        cursor.execute(QUERY_UPDATE_HITS.format(mini_url_id, row[1]))
        db.commit()
        return row[0]
    else:
        return None


def create_url(mini_url_id, base_url):
    return base_url + encode(mini_url_id)


