import re

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from block import block_to_block_type, BlockType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        else: 
            split_n = n.text.split(delimiter)
            i = 0
            while i < len(split_n):
                if i % 2 == 0:
                    new_element = split_n[i]
                    new_node = TextNode(new_element, TextType.TEXT)
                    new_nodes.append(new_node)
                else:
                    new_element = split_n[i]
                    new_node = TextNode(new_element, text_type)
                    new_nodes.append(new_node)
                i += 1

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        elif n.text != "": 
            n_images = extract_markdown_images(n.text)
            remaining_text = n.text
            for im in n_images:
                split_text = remaining_text.split(f"![{im[0]}]({im[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(im[0], TextType.IMAGE, im[1]))
                remaining_text = split_text[-1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        elif n.text != "": 
            n_images = extract_markdown_links(n.text)
            remaining_text = n.text
            for im in n_images:
                split_text = remaining_text.split(f"[{im[0]}]({im[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(im[0], TextType.LINK, im[1]))
                remaining_text = split_text[-1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    bolds = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    italics = split_nodes_delimiter(bolds, "_", TextType.ITALIC)
    codes = split_nodes_delimiter(italics, "`", TextType.CODE)
    images = split_nodes_image(codes)
    links = split_nodes_link(images)
    return links

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filled_blocks = []
    for b in blocks:
        if b !="":
            filled_blocks.append(b.strip())

    return filled_blocks

def markdown_to_html_node(markdown):
        markdown_blocks = markdown_to_blocks(markdown)
        result = []
        for block in markdown_blocks:
            if block_to_block_type(block) == BlockType.PARAGRAPH:
                condensed_block = block.replace("\n", " ")
                result.append(ParentNode("p", text_to_children(condensed_block), ))
            elif block_to_block_type(block) == BlockType.HEAD:
                condensed_block = block.replace("\n", " ")
                headless = condensed_block.split(" ", 1)
                header_size = len(headless[0])
                result.append(ParentNode(f"h{header_size}", text_to_children(headless[1]), ))
            elif block_to_block_type(block) == BlockType.CODE:
                code_inner = block.strip("```")
                code_inner_2 = code_inner.split("\n", 1)
                code_text = TextNode(code_inner_2[1], TextType.CODE)
                
                pre_code_text = ParentNode("pre", [text_node_to_html_node(code_text)])
                result.append(pre_code_text)

            # elif block_to_block_type(block) == BlockType.QUOTE:
            #     condensed_block = block.replace("\n", " ")
            #     result.append(ParentNode("blockquote", text_to_children(condensed_block), ))
            elif block_to_block_type(block) == BlockType.QUOTE:
                split_block = block.split('\n')
                #print(split_block)
                children =""
                for line in split_block:
                    headless = line.split(">", 1)
                    children += headless[1] + " "
                stripped_children = children.strip()
                result.append(ParentNode("blockquote", text_to_children(stripped_children), ))
            elif block_to_block_type(block) == BlockType.UNORDERED:
                split_block = block.split('\n')
                #print(split_block)
                children = []
                for line in split_block:
                    headless = line.split(" ", 1)
                    children.append(ParentNode("li", text_to_children(headless[1]), ))
                result.append(ParentNode("ul", children))
            else:
                split_block = block.split('\n')
                children = []
                for line in split_block:
                    headless = line.split(" ", 1)
                    children.append(ParentNode("li", text_to_children(headless[1]), ))
                result.append(ParentNode("ol", children))

        final_result = ParentNode("div", result)
        return final_result
    

def text_to_children(text):
    result2 = []
    #condensed_text = text.replace("\n", " ")
    result = text_to_textnodes(text)
            #if block_to_block_type(block) == BlockType.PARAGRAPH:
    for node in result:
        result2.append(text_node_to_html_node(node))

    #paragraph_node = ParentNode("p", result2, )

    return result2

