import unittest

from textnode import TextNode, TextType
from convert_inline import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_children_html_nodes
from htmlnode import LeafNode


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertIsInstance(html_node, LeafNode)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
      node = TextNode("This is a BOLD node", TextType.BOLD)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "b")
      self.assertEqual(html_node.value, "This is a BOLD node")


    def test_italic(self):
      node = TextNode("This is an italic node", TextType.ITALIC)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "i")
      self.assertEqual(html_node.value, "This is an italic node")


    def test_code(self):
      node = TextNode("print('hello world')", TextType.CODE)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "code")
      self.assertEqual(html_node.value, "print('hello world')")


    def test_link(self):
      node = TextNode("Go to link node", TextType.LINK, "https://www.boot.dev")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "a")
      self.assertEqual(html_node.value, "Go to link node")
      self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})


    def test_image(self):
      node = TextNode("Boot-Dev logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-150.png")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "img")
      self.assertEqual(html_node.value, "")
      self.assertEqual(html_node.props, {'src': 'https://www.boot.dev/img/bootdev-logo-full-150.png', 'alt': 'Boot-Dev logo'})


    def test_empty_text_is_preserved(self):
      node = TextNode("", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "")


    def test_string_text_type_is_normalized(self):
      node = TextNode("Normalized from a string", "italic")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "i")
      self.assertEqual(html_node.value, "Normalized from a string")


    def test_invalid_converted_text_type_raises_value_error(self):
      node = TextNode("This node has an invalid converted type", TextType.TEXT)
      node.text_type = None
      with self.assertRaises(ValueError) as cm:
        text_node_to_html_node(node)
      self.assertEqual(str(cm.exception), "Text has no valid type")


    def test_link_allows_missing_url(self):
      node = TextNode("Link text without a target", TextType.LINK)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "a")
      self.assertEqual(html_node.value, "Link text without a target")
      self.assertEqual(html_node.props, {'href': None})


    def test_image_allows_empty_alt_text(self):
      node = TextNode("", TextType.IMAGE, "https://example.com/image.png")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "img")
      self.assertEqual(html_node.value, "")
      self.assertEqual(html_node.props, {'src': 'https://example.com/image.png', 'alt': ''})

    def test_none(self):
      with self.assertRaises(AttributeError) as cm:
        node = TextNode("This node is broken", TextType.BROKEN)
        html_node = text_node_to_html_node(node)
      self.assertEqual(str(cm.exception), "type object 'TextType' has no attribute 'BROKEN'")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty_list(self):
      self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_non_text_nodes_are_unchanged(self):
      node = TextNode("already bold", TextType.BOLD)
      self.assertEqual(
        split_nodes_delimiter([node], "`", TextType.CODE),
        [node],
      )

    def test_text_without_delimiter_is_unchanged(self):
      node = TextNode("plain text only", TextType.TEXT)
      self.assertEqual(
        split_nodes_delimiter([node], "`", TextType.CODE),
        [node],
      )

    def test_split_text(self):
      node = TextNode("This is text with a `code block` word", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
      self.assertEqual(
        new_nodes,
        [
          TextNode("This is text with a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" word", TextType.TEXT),
        ],
      )

    def test_split_multiple_texts(self):
      node = TextNode("This is text with a `code block` word", TextType.TEXT)
      node2 = TextNode("This is also text with a `code block` word", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node,node2], "`", TextType.CODE)
      self.assertEqual(
        new_nodes,
        [
          TextNode("This is text with a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" word", TextType.TEXT),
          TextNode("This is also text with a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" word", TextType.TEXT),
        ],
      )

    def test_delimiter_at_start(self):
      node = TextNode("`This` is text with multiple `code block` `words`", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
      self.assertEqual(
        new_nodes,
        [
          TextNode("This", TextType.CODE),
          TextNode(" is text with multiple ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" ", TextType.TEXT),
          TextNode("words", TextType.CODE),
        ],
      )

    def test_only_delimited_text(self):
      node = TextNode("`code`", TextType.TEXT)
      self.assertEqual(
        split_nodes_delimiter([node], "`", TextType.CODE),
        [TextNode("code", TextType.CODE)],
      )

    def test_delimiter_at_end(self):
      node = TextNode("text with `code`", TextType.TEXT)
      self.assertEqual(
        split_nodes_delimiter([node], "`", TextType.CODE),
        [
          TextNode("text with ", TextType.TEXT),
          TextNode("code", TextType.CODE),
        ],
      )

    def test_adjacent_delimited_sections(self):
      node = TextNode("`a``b`", TextType.TEXT)
      self.assertEqual(
        split_nodes_delimiter([node], "`", TextType.CODE),
        [
          TextNode("a", TextType.CODE),
          TextNode("b", TextType.CODE),
        ],
      )

    def test_bold_delimiter(self):
      node = TextNode("This has **bold** text", TextType.TEXT)
      self.assertEqual(
        split_nodes_delimiter([node], "**", TextType.BOLD),
        [
          TextNode("This has ", TextType.TEXT),
          TextNode("bold", TextType.BOLD),
          TextNode(" text", TextType.TEXT),
        ],
      )

    def test_bold_delimiter_with_spaces_is_not_markdown(self):
      node = TextNode(
        "This text wont be ** bold ** since there is spaces in there.",
        TextType.TEXT,
      )
      self.assertEqual(
        split_nodes_delimiter([node], "**", TextType.BOLD),
        [node],
      )

class TestFindingImgsLinks(unittest.TestCase):
  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text [to youtube](https://www.youtube.com/@bootdotdev) with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png)"
    )
    self.assertListEqual(
      [
        ("image", "https://i.imgur.com/zjjcJKZ.png"),
        ("second image", "https://i.imgur.com/3elNhQu.png"),
      ],
      matches,
    )

  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
      "This is text with a link [](https://www.boot.dev) ![image](https://i.imgur.com/zjjcJKZ.png) and [to youtube](https://www.youtube.com/@bootdotdev)"
    )
    self.assertListEqual(
      [
        ("", "https://www.boot.dev"),
        ("to youtube", "https://www.youtube.com/@bootdotdev"),
      ],
      matches,
    )

class TestSplitNodesImage(unittest.TestCase):
  def test_links_list(self):
    node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT,)
    matches = split_nodes_image([node])
    self.assertListEqual([TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT,)],
    matches,
  )

  def test_split_images(self):
      node = TextNode(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
          TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
          [
              TextNode("This is text with an ", TextType.TEXT),
              TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
              TextNode(" and another ", TextType.TEXT),
              TextNode(
                  "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
              ),
          ],
          new_nodes,
      )

  def test_split_images_back_to_back(self):
    node = TextNode(
      "![first](https://example.com/first.png)![second](https://example.com/second.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("first", TextType.IMAGE, "https://example.com/first.png"),
        TextNode("second", TextType.IMAGE, "https://example.com/second.png"),
      ],
      new_nodes,
    )

  def test_split_images_at_start_and_end(self):
    node = TextNode(
      "![start](https://example.com/start.png) middle ![end](https://example.com/end.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
        TextNode(" middle ", TextType.TEXT),
        TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
      ],
      new_nodes,
    )

  def test_split_images_preserves_links_as_text(self):
    node = TextNode(
      "Before [docs](https://example.com/docs) ![diagram](https://example.com/diagram.png) after",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("Before [docs](https://example.com/docs) ", TextType.TEXT),
        TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.png"),
        TextNode(" after", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_images_multiple_nodes(self):
    nodes = [
      TextNode("Before ![one](https://example.com/one.png) after", TextType.TEXT),
      TextNode("already linked", TextType.LINK, "https://example.com"),
      TextNode("![two](https://example.com/two.png) tail", TextType.TEXT),
    ]
    new_nodes = split_nodes_image(nodes)
    self.assertListEqual(
      [
        TextNode("Before ", TextType.TEXT),
        TextNode("one", TextType.IMAGE, "https://example.com/one.png"),
        TextNode(" after", TextType.TEXT),
        TextNode("already linked", TextType.LINK, "https://example.com"),
        TextNode("two", TextType.IMAGE, "https://example.com/two.png"),
        TextNode(" tail", TextType.TEXT),
      ],
      new_nodes,
    )
        

class TestSplitNodesLink(unittest.TestCase):
  def test_split_images(self):
      node = TextNode(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
          TextType.TEXT,
      )
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
          [
              TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),],
          new_nodes,
      )

  def test_split_links(self):
    node = TextNode(
      "This is text with [docs](https://example.com/docs) and [blog](https://example.com/blog)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with ", TextType.TEXT),
        TextNode("docs", TextType.LINK, "https://example.com/docs"),
        TextNode(" and ", TextType.TEXT),
        TextNode("blog", TextType.LINK, "https://example.com/blog"),
      ],
      new_nodes,
    )

  def test_split_links_back_to_back(self):
    node = TextNode(
      "[docs](https://example.com/docs)[blog](https://example.com/blog)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("docs", TextType.LINK, "https://example.com/docs"),
        TextNode("blog", TextType.LINK, "https://example.com/blog"),
      ],
      new_nodes,
    )

  def test_split_links_at_start_and_end(self):
    node = TextNode(
      "[start](https://example.com/start) middle [end](https://example.com/end)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("start", TextType.LINK, "https://example.com/start"),
        TextNode(" middle ", TextType.TEXT),
        TextNode("end", TextType.LINK, "https://example.com/end"),
      ],
      new_nodes,
    )

  def test_split_links_preserves_images_as_text(self):
    node = TextNode(
      "Before ![diagram](https://example.com/diagram.png) [docs](https://example.com/docs) after",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("Before ![diagram](https://example.com/diagram.png) ", TextType.TEXT),
        TextNode("docs", TextType.LINK, "https://example.com/docs"),
        TextNode(" after", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_links_multiple_nodes(self):
    nodes = [
      TextNode("Before [one](https://example.com/one) after", TextType.TEXT),
      TextNode("already image", TextType.IMAGE, "https://example.com/img.png"),
      TextNode("[two](https://example.com/two) tail", TextType.TEXT),
    ]
    new_nodes = split_nodes_link(nodes)
    self.assertListEqual(
      [
        TextNode("Before ", TextType.TEXT),
        TextNode("one", TextType.LINK, "https://example.com/one"),
        TextNode(" after", TextType.TEXT),
        TextNode("already image", TextType.IMAGE, "https://example.com/img.png"),
        TextNode("two", TextType.LINK, "https://example.com/two"),
        TextNode(" tail", TextType.TEXT),
      ],
      new_nodes,
    )
class TestTextToTextNodes(unittest.TestCase):
  def test_text_to_textnodes_inline_formatting(self):
      markdown = "This has **bold**, _italic_, and `code`."
      nodes = text_to_textnodes(markdown)
      self.assertListEqual(
          [
              TextNode("This has ", TextType.TEXT),
              TextNode("bold", TextType.BOLD),
              TextNode(", ", TextType.TEXT),
              TextNode("italic", TextType.ITALIC),
              TextNode(", and ", TextType.TEXT),
              TextNode("code", TextType.CODE),
              TextNode(".", TextType.TEXT),
          ],
          nodes,
      )


class TestMarkdownToInlineHTML(unittest.TestCase):
  def test_plain_text_returns_single_leaf_node(self):
    child_nodes = markdown_to_children_html_nodes("plain text")
    self.assertEqual(len(child_nodes), 1)
    self.assertIsInstance(child_nodes[0], LeafNode)
    self.assertEqual(child_nodes[0].tag, None)
    self.assertEqual(child_nodes[0].value, "plain text")

  def test_mixed_inline_markdown_returns_leaf_nodes_in_order(self):
    child_nodes = markdown_to_children_html_nodes("Start **bold** then _italic_ then `code`.")
    self.assertEqual([node.to_html() for node in child_nodes], [
      "Start ",
      "<b>bold</b>",
      " then ",
      "<i>italic</i>",
      " then ",
      "<code>code</code>",
      ".",
    ])

  def test_links_and_images_are_converted_to_leaf_nodes(self):
    child_nodes = markdown_to_children_html_nodes(
      "Open [docs](https://example.com/docs) and view ![logo](https://example.com/logo.png)."
    )
    self.assertEqual([node.to_html() for node in child_nodes], [
      "Open ",
      '<a href="https://example.com/docs">docs</a>',
      " and view ",
      '<img src="https://example.com/logo.png" alt="logo"></img>',
      ".",
    ])

  def test_text_to_textnodes_links_and_images(self):
      markdown = "Open [docs](https://example.com/docs) and view ![logo](https://example.com/logo.png)."
      nodes = text_to_textnodes(markdown)
      self.assertListEqual(
          [
              TextNode("Open ", TextType.TEXT),
              TextNode("docs", TextType.LINK, "https://example.com/docs"),
              TextNode(" and view ", TextType.TEXT),
              TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
              TextNode(".", TextType.TEXT),
          ],
          nodes,
      )

  def test_text_to_textnodes_mixed_markdown(self):
      markdown = (
          "Start **bold** then _italic_ then `code` "
          "then ![img](https://example.com/img.png) "
          "then [site](https://example.com)."
      )
      nodes = text_to_textnodes(markdown)
      self.assertListEqual(
          [
              TextNode("Start ", TextType.TEXT),
              TextNode("bold", TextType.BOLD),
              TextNode(" then ", TextType.TEXT),
              TextNode("italic", TextType.ITALIC),
              TextNode(" then ", TextType.TEXT),
              TextNode("code", TextType.CODE),
              TextNode(" then ", TextType.TEXT),
              TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
              TextNode(" then ", TextType.TEXT),
              TextNode("site", TextType.LINK, "https://example.com"),
              TextNode(".", TextType.TEXT),
          ],
          nodes,
      )

if __name__ == "__main__":
    unittest.main()