import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct_return = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, correct_return)

    def test_split_delim_missing(self):
        node = TextNode("code block delim not in string", TextType.TEXT)
        # Correct usage of assertRaises
        self.assertRaises(
            ValueError, 
            split_nodes_delimiter,
            [node], "`", TextType.CODE
        )

    def test_split_beginning_delim(self):
        node = TextNode("`code block` delim at str beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct_return = [
            TextNode("code block", TextType.CODE),
            TextNode(" delim at str beginning", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, correct_return)

    def test_split_end_delim(self):
        node = TextNode(" delim at str end `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct_return = [
            TextNode(" delim at str end ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
            ]
        self.assertEqual(new_nodes, correct_return)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        correct = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), correct)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        correct = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), correct)
    

   




if __name__ == "__main__":
    unittest.main()