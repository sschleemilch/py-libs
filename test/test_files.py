from unittest import mock, TestCase, main
import os
import shutil
import lib.files

TEST_DIR = 'test_files_tmp'


@mock.patch('lib.files.LOGGER', mock.Mock())
class TestFiles(TestCase):
    def setUp(self):
        try:
            os.makedirs(TEST_DIR + '/.hidden')
        except FileExistsError:
            pass
        with open(TEST_DIR + '/test.txt', 'a') as f:
            f.write('test')
        open(TEST_DIR + '/test.md', 'a').close()
        open(TEST_DIR + '/.hidden/test.txt', 'a').close()
        open(TEST_DIR + '/.hidden/.hidden.txt', 'a').close()

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_hash_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            lib.files.hash_file('not_existing.txt')

    def test_hash_file(self):
        hashed_file = lib.files.hash_file(TEST_DIR + '/test.txt')
        self.assertEqual('05a671c66aefea124cc08b76ea6d30bb', hashed_file)

    def test_hash_file_large(self):
        hashed_file = lib.files.hash_file(TEST_DIR + '/test.txt', large=True)
        self.assertEqual('098f6bcd4621d373cade4e832627b4f6', hashed_file)

    def test_get_files_with_pattern(self):
        result = lib.files.get_files_with_pattern('*.txt', start=TEST_DIR)
        self.assertTrue(len(result) == 1)
        self.assertTrue('test.txt' in result[0])

    def test_get_files_with_pattern_hidden(self):
        result = lib.files.get_files_with_pattern('*.txt', start=TEST_DIR, skip_hidden_dirs=False)
        self.assertTrue(len(result) == 2)

    def test_get_files_with_pattern_hidden_non_recursive(self):
        result = lib.files.get_files_with_pattern('*.txt', start=TEST_DIR, recursive=False, skip_hidden_dirs=False)
        self.assertTrue(len(result) == 1)

    def test_get_files_with_pattern_hidden_files(self):
        result = lib.files.get_files_with_pattern('*.txt', start=TEST_DIR, skip_hidden_dirs=False, skip_hidden_files=False)
        self.assertTrue(len(result) == 3)

    def test_get_files_with_patterns(self):
        result = lib.files.get_files_with_patterns(['*.txt', '*.md'], start=TEST_DIR)
        self.assertTrue(len(result) == 2)

    def test_get_files_with_patterns_no_list(self):
        with self.assertRaises(TypeError):
            lib.files.get_files_with_patterns('*.txt')

    def test_get_files_with_pattern_non_existing_start(self):
        with self.assertRaises(FileNotFoundError):
            lib.files.get_files_with_pattern('*.txt', start='IAMNOTEXISTING')


if __name__ == '__main__':
    main()
