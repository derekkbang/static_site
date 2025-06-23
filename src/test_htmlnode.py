import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from block import block_to_block_type, BlockType
from splitter import *

class TestHTMLNode(unittest.TestCase):


    def test_value(self):
        node = HTMLNode("e", "eeeee")
        node_i = HTMLNode("i", "iiiii")
        node2 = HTMLNode("e", "eeeee",  [node, node_i] , {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node.value, node2.value)

    def test_props(self):
        node = HTMLNode("e", "eeeee")
        node_i = HTMLNode("i", "iiiii")
        node2 = HTMLNode("e", "eeeee",  [node, node_i] , {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node2.props_to_html())

    def test_none(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_none(self):
        node = LeafNode(None, "HEY!")
        self.assertEqual(node.to_html(), "HEY!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_two_children(self):
        child1_node = LeafNode("span", "child1")
        child2_node = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child1_node, child2_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_2(self):
        sansei_node1 = LeafNode("b", "mago1")
        sansei_node2 = LeafNode("b", "mago2")
        nisei_node1 = ParentNode("span", [sansei_node1])
        nisei_node2 = ParentNode("span", [sansei_node2])
        issei_node = ParentNode("div", [nisei_node1, nisei_node2])
        self.assertEqual(
            issei_node.to_html(),
            "<div><span><b>mago1</b></span><span><b>mago2</b></span></div>",
        )

    def test_to_html_with_sumiko(self):
        sansei_node1 = LeafNode("b", "akb")
        sansei_node2 = LeafNode("b", "dtkb")
        sansei_node3 = LeafNode("b", "khkb")
        nisei_node1 = ParentNode("span", [sansei_node1, sansei_node2, sansei_node3])
        nisei_node2 = LeafNode("b", "tdk")
        nisei_node3 = LeafNode("b", "knj")
        issei_node = ParentNode("div", [nisei_node1, nisei_node2, nisei_node3])
        self.assertEqual(
            issei_node.to_html(),
            "<div><span><b>akb</b><b>dtkb</b><b>khkb</b></span><b>tdk</b><b>knj</b></div>",
        )

    def test_to_html_with_unmarried_middle_child(self):
        sansei_node1 = LeafNode("b", "leaf1")
        sansei_node2 = LeafNode("b", "leaf2")
        sansei_node3 = LeafNode("b", "leaf3")
        sansei_node4 = LeafNode("b", "leaf4")
        sansei_node5 = LeafNode("b", "leaf5")
        nisei_node1 = ParentNode("span", [sansei_node1, sansei_node2, sansei_node3])
        nisei_node2 = LeafNode("b", "upper-leaf")
        nisei_node3 = ParentNode("span", [sansei_node4, sansei_node5])
        issei_node = ParentNode("div", [nisei_node1, nisei_node2, nisei_node3])
        self.assertEqual(
            issei_node.to_html(),
            "<div><span><b>leaf1</b><b>leaf2</b><b>leaf3</b></span><b>upper-leaf</b><span><b>leaf4</b><b>leaf5</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_link_text(self):
        node = TextNode("This is a link node", TextType.LINK, "www.href.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {'href': 'www.href.com'})

    def test_link_image(self):
        node = TextNode("This is alt text", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'www.image.com', 'alt': 'This is alt text'})

    #def test_no_children(self):
        #child_node = LeafNode("span", "child")
    #    parent_node = ParentNode("div", None)
    #    self.assertRaises(ValueError("parent node needs children"), parent_node.to_html())

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

if __name__ == "__main__":
    unittest.main()
