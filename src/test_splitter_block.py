import unittest

from textnode import TextNode, TextType
from splitter import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from block import block_to_block_type, BlockType

class TestSplitter(unittest.TestCase):

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
    def test_block_type(self):
        block = ">This is another paragraph with _italic_ text and `code` here\n>This is the same paragraph on a new line\n>^%*&#%This is a new line\n>"
        
        self.assertEqual(
            block_to_block_type(block),

                BlockType.QUOTE,
        )

    def test_block_type_2(self):
        block = "```###### 1. This is another paragraph with _italic_ text and `code` here\n2. This is the same paragraph on a new line\n3. This is a new line\n5. This is not.```"
        
        self.assertEqual(
            block_to_block_type(block),
                BlockType.CODE,
        )
    def test_block_type_3(self):
        block = "###### 1. This is a header"
        block2 = "# 1. This is a header"
        
        self.assertEqual(
            block_to_block_type(block),
            block_to_block_type(block2),
        )
    def test_block_type_4(self):
        block = "1. This is the first\n2. This is the second\n3.This is a mistake"
        
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )
    def test_block_type_5(self):
        block = ">This is the first>This is the second>This is the third"
        
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )
        
        
        



if __name__ == "__main__":
    unittest.main()





