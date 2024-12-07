import unittest

from textnode import TextNode, TextType

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link
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
    



   
class TestSplitTextNodes(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])

        correct = [
                        TextNode("This is text with a link ", TextType.TEXT),
                        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                        TextNode(" and ", TextType.TEXT),
                        TextNode(
                            "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                        ),
                    ]

        self.assertEqual(new_nodes, correct)

    def test_split_nodes_image(self):
        node = TextNode(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        correct = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                        TextNode(" and ", TextType.TEXT),
                        TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    ]

        self.assertEqual(new_nodes, correct)



if __name__ == "__main__":
    unittest.main()