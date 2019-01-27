from unittest import mock, TestCase, main
import os
import shutil
import lib.files

TEST_DIR = 'test_files_tmp'


@mock.patch('lib.files.LOGGER', mock.Mock())
class TestFilesMethods(TestCase):

    def test_hash_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            lib.files.hash_file('not_existing.txt')

    def setUp(self):
        os.makedirs(TEST_DIR + '/.hidden')
        open(TEST_DIR + '/test.txt', 'a').close()
        open(TEST_DIR + '/.hidden', 'a').close()

    def tearDown(self):
        shutil.rmtree(TEST_DIR)


if __name__ == '__main__':
    main()
