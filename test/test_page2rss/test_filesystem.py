import os
import unittest
from pathlib import Path
from page2rss import TEST_OUTPUT_DIR
from page2rss.models.rss20 import RSSPage, RSSArticle
from page2rss.filesystem.operators import xml_page_save, xml_page_remove


class TestFileSystemOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_xml_page_save(self):
        article1 = RSSArticle(title="first article")
        article2 = RSSArticle(title="second article")
        page = RSSPage(
            title="some main page",
            link="some article",
            description="some article",
            articles=[article1, article2]
        )
        xml_page_save(page=page, output_dir=TEST_OUTPUT_DIR)
        self.assertTrue("some_main_page.xml" in os.listdir(TEST_OUTPUT_DIR))

    def test_xml_page_remove_success(self):
        with open(TEST_OUTPUT_DIR / "test_remove.xml", "a"):
            pass
        self.assertTrue("test_remove.xml" in os.listdir(TEST_OUTPUT_DIR))
        xml_page_remove(output_dir=TEST_OUTPUT_DIR, filename="test_remove.xml")
        self.assertEqual([], os.listdir(TEST_OUTPUT_DIR))

    def test_xml_page_remove_fail(self):
        xml_page_remove(output_dir=TEST_OUTPUT_DIR, filename="file_not_found.xml")

    @classmethod
    def tearDownClass(cls):
        for file in Path(TEST_OUTPUT_DIR).rglob("*.xml"):
            os.remove(file)
