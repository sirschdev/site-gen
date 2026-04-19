import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node3 = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        node4 = TextNode("This is a text node", 'link', "www.boot.dev")
        self.assertEqual(node3, node4)

    
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node3)

    
    def test_eq4(self):
        node5 = TextNode("This is a text node", TextType.ITALIC)
        node6 = TextNode("This is a text node", TextType.ITALIC, "www.boot.dev")
        self.assertNotEqual(node5, node6)





if __name__ == "__main__":
    unittest.main()