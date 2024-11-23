import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)


    def test_repr(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node1.__repr__(), 'TextNode(This is a text node, TextType.BOLD, google.com)')
        
    
    def test_no_url(self):
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node2.__repr__(), 'TextNode(This is a text node, TextType.BOLD, None)')
if __name__ == "__main__":
    unittest.main()