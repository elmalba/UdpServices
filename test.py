import rethinkdb as r

temp_conn = r.connect(host='localhost',
                 port=28015)

cursor = r.table("posts").changes().run(temp_conn)
for document in cursor:
    print(document)