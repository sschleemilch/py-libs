from unittest import mock, TestCase, main
import os
import shutil
import lib.json_database
import json

TEST_DIR = os.path.abspath('test_json_database')
TEST_DATABASE_NAME = 'test_json_database.json'

TEST_DATABASE_TEMPLATE = {
    'testelement': 'testcontent'
}


@mock.patch('lib.json_database.LOGGER', mock.Mock())
class TestJsonDatabase(TestCase):
    def setUp(self):
        try:
            os.makedirs(TEST_DIR)
        except FileExistsError:
            pass
        self.json_db = lib.json_database.JSONDatabase(TEST_DATABASE_NAME, TEST_DATABASE_TEMPLATE, TEST_DIR)

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_json_database_init(self):
        self.assertEqual(self.json_db.database_path, os.path.join(TEST_DIR, TEST_DATABASE_NAME))

    def test_json_database_load(self):
        self.assertEqual(self.json_db.data['testelement'], TEST_DATABASE_TEMPLATE['testelement'])

    def test_json_database_delete(self):
        self.json_db.delete()
        self.assertFalse(os.path.exists(self.json_db.database_path))

    def test_json_database_save(self):
        self.json_db.data['new_test_element'] = True
        self.json_db.save()
        with open(self.json_db.database_path, 'r') as f:
            data = json.load(f)
        self.assertTrue(data['new_test_element'])


if __name__ == '__main__':
    main()
