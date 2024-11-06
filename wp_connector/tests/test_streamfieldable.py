import json

from django.test import TestCase

from wp_connector.streamfieldable import StreamFieldable


class TestStreamFieldable(TestCase):
    def setUp(self):
        self.html_content = """
            <h1>Heading 1</h1>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
            <p>Paragraph 3</p>
            <blockquote cite="Author">Quote text</blockquote>
            <dl>
                <dt>Term 1</dt><dd>Definition 1</dd>
                <dt>Term 2</dt><dd>Definition 2</dd>
            </dl>
        """
        self.streamfield = StreamFieldable(content=self.html_content)

    def test_initialization(self):
        """Test that StreamFieldable initializes with content and generates streamdata."""
        self.assertIsInstance(self.streamfield.streamdata, str)

        # Decode JSON data to test its content
        streamdata = json.loads(self.streamfield.streamdata)
        self.assertIsInstance(streamdata, list)

    def test_tag_to_block_mapping(self):
        """Test that each HTML tag maps to the correct block type in streamdata."""
        expected_blocks = [
            {"type": "heading", "value": {"text": "Heading 1", "level": "h1"}},
            {
                "type": "paragraph",
                "value": "<p>Paragraph 1</p><p>Paragraph 2</p><p>Paragraph 3</p>",
            },
            {
                "type": "blockquote",
                "value": {"quote": "Quote text", "attribution": "Author"},
            },
            {
                "type": "definition_list",
                "value": {
                    "list": [
                        {"term": "Term 1", "definition": "Definition 1"},
                        {"term": "Term 2", "definition": "Definition 2"},
                    ]
                },
            },
        ]

        streamdata = json.loads(self.streamfield.streamdata)
        self.assertEqual(streamdata, expected_blocks)

    def test_empty_tag(self):
        """Test that empty tags are skipped in streamdata."""
        empty_html_content = "<p></p><h1></h1>"
        streamfield = StreamFieldable(content=empty_html_content)
        streamdata = json.loads(streamfield.streamdata)

        self.assertEqual(streamdata, [])
