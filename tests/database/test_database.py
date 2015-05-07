import unittest

from mock import Mock, call

from odo.database.cassandra_migration import CassandraMigration


class TestCassandraMigrationDatabase(unittest.TestCase):
    def test_setup_creates_table(self):
        session = Mock()
        test_db = CassandraMigration(session, keyspace='test_keyspace', replication_factor='1')

        test_db.setup()

        expected_calls = [
            call(
                "CREATE KEYSPACE IF NOT EXISTS test_keyspace WITH REPLICATION = { 'class': 'SimpleStrategy', "
                "'replication_factor': 1};"),
            call("USE test_keyspace;"),
            call("CREATE TABLE IF NOT EXISTS migrations ('version');")
        ]

        session.execute.assert_has_calls(expected_calls, any_order=False)

    def test_setup_prepares_statements(self):
        session = Mock()
        test_db = CassandraMigration(session, keyspace='test_keyspace', replication_factor='1')

        test_db.setup()

        expected_calls = [
            call("INSERT INTO migrations (version) VALUES ('?');"),
            call("SELECT * FROM migrations ORDER BY (version ASC);")
        ]

        session.prepare.assert_has_calls(expected_calls, any_order=False)




