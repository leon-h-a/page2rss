import os
import json
import unittest
from pathlib import Path
from page2rss import TEST_OUTPUT_DIR, TEST_PAGE_LIST
from page2rss.models.filesystem import PageEntry
from page2rss.models.rss20 import RSSPage, RSSArticle
from page2rss.filesystem.operators import (
    xml_page_save,
    xml_page_remove,
    page_def_read,
    page_def_update,
    page_def_remove
)

from test.test_page2rss import logger


class TestFileSystemXML(unittest.TestCase):
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


class TestFilesystemPageDefs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TEST_PAGE_LIST, "w") as pgl:
            page_list_file = {}
            entry = PageEntry(
                nick="some_site",
                url="https://some.url.com",
                tag="a",
                css="article-row"
            )
            page_list_file[entry.nick] = dict(
                url=entry.url,
                tag=entry.tag,
                css=entry.css
            )
            json.dump(page_list_file, pgl, indent=2)

    def test_page_def_read(self):
        success = page_def_read("some_site", page_list_dir=TEST_PAGE_LIST)
        self.assertEqual(success.url, "https://some.url.com")
        not_found = page_def_read("does_not_exist", page_list_dir=TEST_PAGE_LIST)
        self.assertEqual(not_found, None)

    def test_page_def_update(self):
        new_entry = PageEntry(
            nick="new_site",
            url="https://new.url.com",
            tag="a",
            css="article-row"
        )
        res = page_def_update(page=new_entry, page_list_dir=TEST_PAGE_LIST)
        self.assertTrue(res, True)
        res = page_def_read("new_site", page_list_dir=TEST_PAGE_LIST)
        self.assertEqual(res.url, "https://new.url.com")

    def test_page_def_remove(self):
        new_entry = PageEntry(
            nick="to_be_deleted",
            url="https://de.le.ted",
            tag="a",
            css="article-row"
        )
        res = page_def_update(new_entry, page_list_dir=TEST_PAGE_LIST)
        self.assertEqual(res, True)
        res = page_def_read("to_be_deleted", page_list_dir=TEST_PAGE_LIST)
        self.assertEqual(res.url, "https://de.le.ted")
        res = page_def_remove(new_entry, page_list_dir=TEST_PAGE_LIST)
        self.assertEqual(res, True)
        res = page_def_read("to_be_deleted", page_list_dir=TEST_PAGE_LIST)
        self.assertEqual(res, None)

    @classmethod
    def tearDownClass(cls):
        with open(TEST_PAGE_LIST, "w") as pgl:
            json.dump({}, pgl, indent=2)
