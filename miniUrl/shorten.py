from time import time
from encode import encode, decode


def add_mini_url(db, targets_dict):
    cursor = db.cursor()
    query = QUERY_INSERT_MINI.format(int(time()))
    cursor.execute(query)
    db.commit()
    mini_url_id = cursor.lastrowid
    values = ["( '{1}', '{0}' )".format(device, targets_dict[device]) for device in targets_dict]
    query = QUERY_INSERT_TARGETS.format(','.join(values), mini_url_id)
    cursor.executescript(query)
    db.commit()
    return create_url(mini_url_id)


def stats(db):
    cursor = db.cursor()
    cursor.execute(QUERY_GET_STATS)
    rows = cursor.fetchall()
    stats = {}
    now = int(time())
    for row in rows:
        mini_url = create_url(row[0])
        if mini_url not in stats:
            stats[mini_url] = { "age": seconds_to_time(now - row[1]),
                                "targets": []}
        stats[mini_url]['targets'].append(
            {"target": row[2], "hits": row[3]}
        )
    return stats


def retrieve_url(db, mini_url, user_agent):
    cursor = db.cursor()
    mini_url_id = decode(mini_url)
    query = QUERY_RETRIEVE_TARGET.format(mini_url_id, user_agent)
    cursor.execute(query)
    rows = cursor.fetchall()
    if len(rows) > 0:
        cursor.execute(QUERY_UPDATE_HITS.format(mini_url_id, rows[0][1]))
        db.commit()
        return rows[0][0]
    else:
        return None


def create_url(mini_url_id):
    return MINI_URL_BASE + encode(mini_url_id)


def seconds_to_time(seconds):
    minutes, secs = divmod(seconds, 60)
    hrs, minutes = divmod(minutes, 60)
    return "%d hrs %02d mins %02d sec" % (hrs, minutes, secs)


MINI_URL_BASE = 'http://localhost:5000/mini/'

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
