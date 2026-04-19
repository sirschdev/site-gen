import unittest

from convert_block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_assignment_example(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            list(blocks),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_strips_whitespace_from_each_block(self):
        md = """

  # Heading block  

  Paragraph block with spaces around it.  

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            list(blocks),
            [
                "# Heading block",
                "Paragraph block with spaces around it.",
            ],
        )

    def test_markdown_to_blocks_removes_empty_blocks_from_extra_newlines(self):
        md = """
First block



Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            list(blocks),
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_markdown_to_blocks_preserves_single_newlines_within_block(self):
        md = """
Line one of a paragraph
Line two of the same paragraph

Another paragraph
still the same block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            list(blocks),
            [
                "Line one of a paragraph\nLine two of the same paragraph",
                "Another paragraph\nstill the same block",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_basic_case(self):        
        block = "- This is a list\n- with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.UNORDERED_LIST)

        # --- Heading Tests ---
    def test_heading_valid(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_invalid(self):
        # More than 6 hashes
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)
        # No space after hash
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # --- Code Block Tests ---
    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_code_block_invalid(self):
        # Missing newline after first backticks
        self.assertEqual(block_to_block_type("```print('hi')\n```"), BlockType.PARAGRAPH)
        # Missing closing backticks
        self.assertEqual(block_to_block_type("```\nprint('hi')"), BlockType.PARAGRAPH)

    # --- Quote Block Tests ---
    def test_quote_block(self):
        quote = "> This is a quote\n> with multiple lines"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        # No space after > is allowed
        self.assertEqual(block_to_block_type(">Line without space"), BlockType.QUOTE)

    def test_quote_block_invalid(self):
        # Not every line starts with >
        quote = "> Line 1\nLine 2"
        self.assertEqual(block_to_block_type(quote), BlockType.PARAGRAPH)

    # --- Unordered List Tests ---
    def test_unordered_list(self):
        ul = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        # Missing space after -
        self.assertEqual(block_to_block_type("-Item 1"), BlockType.PARAGRAPH)
        # Mixed lines
        self.assertEqual(block_to_block_type("- Item 1\nItem 2"), BlockType.PARAGRAPH)

    # --- Ordered List Tests ---
    def test_ordered_list(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_start(self):
        # Must start at 1
        self.assertEqual(block_to_block_type("2. First\n3. Second"), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_increment(self):
        # Must increment by 1
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("1.First"), BlockType.PARAGRAPH)

    # --- Paragraph Tests ---
    def test_paragraph(self):
        text = "This is just a normal piece of text\nthat spans two lines."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_markdown_to_html_full_document(self):
        # A "well-written" markdown document with double-newline separation
        md = """# The Title

This is a paragraph with **bold** text and some _italics_ as well.

- This is a list item
- This is another item

> This is a blockquote
> spanning two lines"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = (
            "<div>"
            "<h1>The Title</h1>"
            "<p>This is a paragraph with <b>bold</b> text and some <i>italics</i> as well.</p>"
            "<ul><li>This is a list item</li><li>This is another item</li></ul>"
            "<blockquote>This is a blockquote spanning two lines</blockquote>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_multiple_paragraphs(self):
        md = """First paragraph.

Second paragraph with `inline code`."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<p>First paragraph.</p>"
            "<p>Second paragraph with <code>inline code</code>.</p>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_heading_levels(self):
        md = """# H1

## H2

### H3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3></div>"
        self.assertEqual(html, expected)

    def test_ordered_list_logic(self):
        md = """1. First
2. Second
3. Third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        self.assertEqual(html, expected)

    def test_markdown_to_html_node_long_mixed_document(self):
        md = """## Intro with **bold**

This is the first paragraph with _italic_ text,
and this line should stay in the same paragraph.

- first item with **bold**
- second item with _italic_ and `code`

1. ordered **one**
2. ordered _two_

> quoted _text_
> with **emphasis** inside"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        expected = (
            "<div>"
            "<h2>Intro with <b>bold</b></h2>"
            "<p>This is the first paragraph with <i>italic</i> text, and this line should stay in the same paragraph.</p>"
            "<ul><li>first item with <b>bold</b></li><li>second item with <i>italic</i> and <code>code</code></li></ul>"
            "<ol><li>ordered <b>one</b></li><li>ordered <i>two</i></li></ol>"
            "<blockquote>quoted <i>text</i> with <b>emphasis</b> inside</blockquote>"
            "</div>"
        )

        self.assertEqual(html, expected)

    def test_markdown_to_html_node_long_document_with_code_block(self):
        md = """# Project Overview

This paragraph has **bold**, _italic_, and `inline code`
across two lines in one block.

- alpha entry
- beta entry with **strong** text

```
def greet():
    return \"_not italic_ and **not bold**\"
```

> final _quote_
> line"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        expected = (
            "<div>"
            "<h1>Project Overview</h1>"
            "<p>This paragraph has <b>bold</b>, <i>italic</i>, and <code>inline code</code> across two lines in one block.</p>"
            "<ul><li>alpha entry</li><li>beta entry with <b>strong</b> text</li></ul>"
            "<pre><code>def greet():\n    return \"_not italic_ and **not bold**\"\n</code></pre>"
            "<blockquote>final <i>quote</i> line</blockquote>"
            "</div>"
        )

        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()