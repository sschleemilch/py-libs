from unittest import mock, TestCase, main
import os
import shutil
import lib.files

TEST_DIR = 'test_files_tmp'


@mock.patch('lib.files.LOGGER', mock.Mock())
class TestFilesMethods(TestCase):
    def setUp(self):
        try:
            os.makedirs(TEST_DIR + '/.hidden')
        except FileExistsError:
            pass
        open(TEST_DIR + '/test.txt', 'a').close()
        open(TEST_DIR + '/test.md', 'a').close()
        open(TEST_DIR + '/.hidden/test.txt', 'a').close()
        open(TEST_DIR + '/.hidden/.hidden.txt', 'a').close()

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_hash_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            lib.files.hash_file('not_existing.txt')

    def test_get_files_with_pattern(self):
        result = lib.files.get_files_with_pattern('*.txt', start=TEST_DIR)
        self.assertTrue(len(result) == 1)
        self.assertTrue('test.txt' in result[0])

    def test_get_files_with_pattern_hidden(self):
        result = lib.files.get_files_with_pattern('*.txt', start=TEST_DIR, skip_hidden_dirs=False)
        self.assertTrue(len(result) == 2)

    def test_get_files_with_pattern_hidden_files(self):
        result = lib.files.get_files_with_pattern('*.txt', start=TEST_DIR, skip_hidden_dirs=False, skip_hidden_files=False)
        self.assertTrue(len(result) == 3)

    def test_get_files_with_patterns(self):
        result = lib.files.get_files_with_patterns(['*.txt', '*.md'], start=TEST_DIR)
        self.assertTrue(len(result) == 2)


if __name__ == '__main__':
    main()
