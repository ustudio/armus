class CassandraMigration(object):
    def __init__(self, session, keyspace, replication_factor):
        self.session = session
        self.keyspace = keyspace
        self.replication_factor = replication_factor

    def setup(self):
        create_keyspace = "CREATE KEYSPACE IF NOT EXISTS {0} WITH REPLICATION = {{ 'class': 'SimpleStrategy', " \
                          "'replication_factor': {1}}};".format(self.keyspace, self.replication_factor)

        self.session.execute(create_keyspace)
        self.session.execute("USE {0};".format(self.keyspace))
        self.session.execute("CREATE TABLE IF NOT EXISTS migrations ('version');")
        self.session.prepare("INSERT INTO migrations (version) VALUES ('?');")
        self.session.prepare("SELECT * FROM migrations ORDER BY (version ASC);")

