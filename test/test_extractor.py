import sys
import unittest
from unittest.mock import MagicMock

# Mock the network dependency before importing the plugin so the test is
# deterministic and never touches the network or a real feedparser install.
sys.modules.setdefault("feedparser", MagicMock())

from ovos_plugin_manager.templates.ocp import OCPStreamExtractor

from ovos_ocp_rss_plugin import OCPRSSFeedExtractor


class TestOCPRSSFeedExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = OCPRSSFeedExtractor()

    def test_is_stream_extractor_subclass(self):
        self.assertTrue(issubclass(OCPRSSFeedExtractor, OCPStreamExtractor))
        self.assertIsInstance(self.extractor, OCPStreamExtractor)

    def test_declares_base_methods(self):
        # methods/properties declared by the base class must be present
        self.assertTrue(hasattr(OCPRSSFeedExtractor, "supported_seis"))
        self.assertTrue(callable(getattr(self.extractor, "extract_stream")))
        self.assertTrue(callable(getattr(self.extractor, "validate_uri")))

    def test_supported_seis(self):
        self.assertEqual(OCPRSSFeedExtractor.supported_seis, ["rss"])

    def test_validate_uri(self):
        # matches via sei prefix
        self.assertTrue(self.extractor.validate_uri("rss//http://example.com/feed"))
        # unrelated uri
        self.assertFalse(self.extractor.validate_uri("youtube//abc"))

    def test_settings_from_ocp(self):
        ext = OCPRSSFeedExtractor({"rss": {"foo": "bar"}})
        self.assertEqual(ext.settings, {"foo": "bar"})

    def test_settings_default(self):
        self.assertEqual(self.extractor.settings, {})

    def test_extract_stream_swallows_errors(self):
        # bad/empty input must not raise and returns an empty dict
        self.assertEqual(self.extractor.extract_stream("rss//"), {})


class TestEntryPointGroup(unittest.TestCase):

    def test_canonical_entrypoint_group(self):
        import os
        import re

        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(here, "pyproject.toml")) as f:
            pyproject_src = f.read()
        # the canonical stream-extractor group read by ovos-plugin-manager
        self.assertIn('[project.entry-points."opm.ocp.extractor"]', pyproject_src)
        # the deprecated form must be gone
        self.assertIsNone(re.search(r'"ovos\.ocp\.extractor"', pyproject_src))


if __name__ == "__main__":
    unittest.main()
