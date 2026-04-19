import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_htmlnode_init(self):
        node = HTMLNode("p", "this is some text", None, {"class":"text text-sm"})
        expected = 'tag: "p", value: "this is some text", children: "None", props: "{\'class\': \'text text-sm\'}"'
        self.assertEqual(repr(node), expected)
    
    def test_props_to_html(self):
        node = HTMLNode("p", "this is some text", None, {"class":"text text-sm"})
        expected = 'class="text text-sm"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html2(self):
        node = HTMLNode(None,None,None,{"href": "https://www.google.com","target": "_blank",})
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html3(self):
        node = HTMLNode("a", "linktext", None, {"style":"background:red; color:white;", "href":"https://www.boot.dev/"})
        expected = 'style="background:red; color:white;" href="https://www.boot.dev/"'
        self.assertEqual(node.props_to_html(), expected)

    # Leaf Node Tests

    def test_leaf_init(self):
        node = LeafNode("p", "this is some text", {"class":"text text-sm"})
        expected = 'tag: "p", value: "this is some text", props: "{\'class\': \'text text-sm\'}"'
        self.assertEqual(repr(node), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Best Headline ever!", {"class": "h1 large bold", "id": "heading123"})
        self.assertEqual(node.to_html(), "<h1 class=\"h1 large bold\" id=\"heading123\">Best Headline ever!</h1>")

    def test_leaf_to_html_empty(self):
        node = LeafNode(None, value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_error(self):
        with self.assertRaises(ValueError) as cm:
            node = LeafNode(None, None)
            html = node.to_html()
        self.assertEqual(str(cm.exception), "Leaf node must have a value")
    
    def test_leaf_to_html_error2(self):
        node = LeafNode(None, value="")
        self.assertEqual(node.to_html(), "")

        # Parent Node Test

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )

    def test_parent_init(self):
        child_node = LeafNode("span", "child")
        node = ParentNode("div", [child_node], {"class": "wrapper"})
        expected = f'tag: "div", children: "{[child_node]}", props: "{{\'class\': \'wrapper\'}}"'
        self.assertEqual(repr(node), expected)

    def test_parent_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "wrapper", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="wrapper" id="main"><span>child</span></div>',
        )

    def test_parent_to_html_with_multiple_children(self):
        child_one = LeafNode("span", "first")
        child_two = LeafNode("span", "second")
        parent_node = ParentNode("div", [child_one, child_two])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><span>second</span></div>",
        )

    def test_parent_to_html_with_mixed_nested_children(self):
        nested_parent = ParentNode("span", [LeafNode("b", "bold")])
        trailing_child = LeafNode(None, "plain")
        parent_node = ParentNode("p", [nested_parent, trailing_child])
        self.assertEqual(
            parent_node.to_html(),
            "<p><span><b>bold</b></span>plain</p>",
        )

    def test_parent_to_html_error_without_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [child_node]).to_html()
        self.assertEqual(str(cm.exception), "Parent node must have a tag")

    def test_parent_to_html_error_without_children(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", None).to_html()
        self.assertEqual(str(cm.exception), "Parent node must have at least one child")

    def test_parent_to_html_error_with_empty_children(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", []).to_html()
        self.assertEqual(str(cm.exception), "Parent node must have at least one child")

    def test_parent_to_html_with_five_nested_nodes_and_props(self):
        first_branch = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "Paragraph", {"class": "copy", "data-kind": "primary"}),
                        LeafNode("i", "Italic", {"class": "accent", "aria-hidden": "true"}),
                    ],
                    {"class": "inner", "data-depth": "2"},
                )
            ],
            {"class": "column", "id": "left"},
        )
        second_branch = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("span", "Span", {"class": "label", "data-kind": "secondary"}),
                        LeafNode("strong", "Strong", {"class": "weight", "title": "emphasis"}),
                    ],
                    {"class": "inner", "data-depth": "2"},
                )
            ],
            {"class": "column", "id": "right"},
        )
        section_node = ParentNode(
            "section",
            [first_branch, second_branch],
            {"class": "layout", "data-theme": "feature"},
        )
        self.assertEqual(
            section_node.to_html(),
            '<section class="layout" data-theme="feature"><div class="column" id="left"><div class="inner" data-depth="2"><p class="copy" data-kind="primary">Paragraph</p><i class="accent" aria-hidden="true">Italic</i></div></div><div class="column" id="right"><div class="inner" data-depth="2"><span class="label" data-kind="secondary">Span</span><strong class="weight" title="emphasis">Strong</strong></div></div></section>',
        )




if __name__ == "__main__":
    unittest.main()