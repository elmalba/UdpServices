import rethinkdb as r
from random import getrandbits

conn = r.connect(host='localhost',
                 port=28015)



r.table("posts").insert({
    "id": getrandbits(43),
    "title": "fasdfasd mia",
    "content": "Dolor asdfasdf amet"
}).run(conn)


conn.close()