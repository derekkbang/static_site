import unittest

from textnode import TextNode, TextType
from splitter import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "melonparty.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "fakecarts.com")
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

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

    def test_split_no_images(self):
        node = TextNode(
            "How can you read this? There's no pictures!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("How can you read this? There's no pictures!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_first(self):
        node = TextNode(
            "![cheems](https://i.imgur.com/l9dPufI.jpeg) and nothing else",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cheems", TextType.IMAGE, "https://i.imgur.com/l9dPufI.jpeg"),
                TextNode(" and nothing else", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)![cheems](https://i.imgur.com/l9dPufI.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("cheems", TextType.IMAGE, "https://i.imgur.com/l9dPufI.jpeg"),
            ],
            new_nodes,
        )
    def test_split_image_others(self):
        node_1  = TextNode(
            "first some text here",
            TextType.TEXT,
        )
        img_node = TextNode(
            "![some alt text](a link here) some more text after that",
            TextType.TEXT,
        )
        node_2  = TextNode(
            "and finally some text here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node_1, img_node, node_2])
        self.assertListEqual(
            [
                TextNode("first some text here", TextType.TEXT),
                TextNode("some alt text", TextType.IMAGE, "a link here"),
                TextNode(" some more text after that", TextType.TEXT),
                TextNode("and finally some text here", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_image_others_2(self):
        node_1  = TextNode(
            "first some bold text here",
            TextType.BOLD,
        )
        img_node = TextNode(
            "![some alt text](a link here) some more text after that",
            TextType.TEXT,
        )
        node_2  = TextNode(
            "and finally some italic text here",
            TextType.ITALIC,
        )
        new_nodes = split_nodes_image([node_1, img_node, node_2])
        self.assertListEqual(
            [
                TextNode("first some bold text here", TextType.BOLD),
                TextNode("some alt text", TextType.IMAGE, "a link here"),
                TextNode(" some more text after that", TextType.TEXT),
                TextNode("and finally some italic text here", TextType.ITALIC),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_textnodes_bold_sandwich(self):
        text = "**This is bold text with** an ![image sandwiched between](https://i.imgur.com/l9dPufI.jpeg) **both ends**"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is bold text with", TextType.BOLD),
                TextNode(" an ", TextType.TEXT),
                TextNode("image sandwiched between", TextType.IMAGE, "https://i.imgur.com/l9dPufI.jpeg"),
                TextNode(" ", TextType.TEXT),
                TextNode("both ends", TextType.BOLD),

            ],
            textnodes,
        )

    def test_textnodes_links_and_images(self):
        text = "[link](link text)![image sandwiched between](https://i.imgur.com/l9dPufI.jpeg)[link](link text)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "link text"),
                TextNode("image sandwiched between", TextType.IMAGE, "https://i.imgur.com/l9dPufI.jpeg"),
                TextNode("link", TextType.LINK, "link text"),

            ],
            textnodes,
        )
    def test_textnodes_backwards(self):
        text = "[link](link text)![image](https://i.imgur.com/l9dPufI.jpeg)`with code`_ and some italics_** and finally some bold text**"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "link text"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/l9dPufI.jpeg"),
                TextNode("with code", TextType.CODE),
                TextNode(" and some italics", TextType.ITALIC),
                TextNode(" and finally some bold text", TextType.BOLD),

            ],
            textnodes,
        )
    def test_textnodes_nestled(self):
        text = "![**how does this work?**](https://i.imgur.com/l9dPufI.jpeg)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("![", TextType.TEXT),
                TextNode("how does this work?", TextType.BOLD),
                TextNode("](https://i.imgur.com/l9dPufI.jpeg)", TextType.TEXT),

            ],
            textnodes,
        )
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_single(self):
        md = """
this is a single block
separated by newlines
all by its lonesome
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "this is a single block\nseparated by newlines\nall by its lonesome",
            ],
        )
    
    def test_markdown_to_blocks_multi(self):
        md = """
this is three lines

separated by newlines

divided into three
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "this is three lines","separated by newlines","divided into three",
            ],
        )

    def test_markdown_to_blocks_whitespace(self):
        md = """
 This is the start


                        some space here                        


 This is the end          
     """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the start","some space here","This is the end",
            ],
        )

    def test_markdown_to_blocks_whitespace_2(self):
        md = """
This is the start











This is the end          
     """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the start","This is the end",
            ],
        )


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
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
### Header Here

- Here is the first element of the list
- As you can see, it is an unordered list

- This is a separate unordered list

-However, this is a paragraph.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Header Here</h3><ul><li>Here is the first element of the list</li><li>As you can see, it is an unordered list</li></ul><ul><li>This is a separate unordered list</li></ul><p>-However, this is a paragraph.</p></div>",
        )  
    

    def test_ordered_list(self):
        md = """
1. One
2. Two

Skip a few!

1. Ninety Nine
2. A Hundred!
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>One</li><li>Two</li></ol><p>Skip a few!</p><ol><li>Ninety Nine</li><li>A Hundred!</li></ol></div>",
        )  
        
    def test_images_(self):
        md = """
This is text that _should not_ remain
the **same** since it is not code
and ![cheems](https://i.imgur.com/l9dPufI.jpeg) is here too.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is text that <i>should not</i> remain the <b>same</b> since it is not code and <img src=\"https://i.imgur.com/l9dPufI.jpeg\" alt=\"cheems\"></img> is here too.</p></div>",
        )




if __name__ == "__main__":
    unittest.main()
