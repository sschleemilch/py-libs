from unittest import mock, TestCase, main
import os
import shutil
import lib.portal

TEST_DIR = os.path.abspath('test_portal_tmp')


@mock.patch('lib.portal.LOGGER', mock.Mock())
class TestPortal(TestCase):
    def setUp(self):
        try:
            os.makedirs(TEST_DIR)
        except FileExistsError:
            pass
        self.root = os.getcwd()

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_inDir(self):
        self.assertEqual(self.root, os.getcwd())
        with lib.portal.inDir(TEST_DIR):
            self.assertEqual(os.getcwd(), TEST_DIR)
        self.assertEqual(self.root, os.getcwd())

    def test_inDir_not_existing(self):
        with self.assertRaises(FileNotFoundError):
            lib.portal.inDir('NOT_EXISTING_FOR_SURE')


if __name__ == '__main__':
    main()
