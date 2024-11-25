import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode()
        node1 = HTMLNode('test_tag', 'test_value', 'test_children', {'test_key':'test_value'})
        self.assertEqual(node.__repr__(), 'HTMLNode, None, None, None, None')
        self.assertEqual(node1.__repr__(), "HTMLNode, test_tag, test_value, test_children, {'test_key': 'test_value'}")

    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://www.google.com", 
            "target": "_blank",
            })
        
        self.assertEqual(node.props_to_html(),  ' href="https://www.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        leaf_node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        
        self.assertEqual(leaf_node.to_html(), '<p>This is a paragraph of text.</p>')        
        self.assertEqual(leaf_node1.to_html(), '<a href="https://www.google.com">Click me!</a>')        



class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
