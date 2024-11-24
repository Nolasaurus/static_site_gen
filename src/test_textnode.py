import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("just text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "just text")

    def test_bold(self):
        node = TextNode("just text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "just text")

    def test_italic(self):
        node = TextNode("just text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "just text")

    def test_code(self):
        node = TextNode("just text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "just text")
        
    def test_link(self):
        node = TextNode("just text", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "just text")
        self.assertEqual(html_node.props, "href")
        
    def test_image(self):
        node = TextNode("just alt text", TextType.IMAGE, "this is url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {'src': "this is url", 'alt': "just alt text"}
)




if __name__ == "__main__":
    unittest.main()