from enum import Enum
from htmlnode import HTMLNode, LeafNode

def text_node_to_html_node(text_node):

    if text_node.text_type.value == "text":
        return LeafNode(None, text_node.text)
    elif text_node.text_type.value == "bold":
        return LeafNode("b", text_node.text)
    elif text_node.text_type.value == "italic":
        return LeafNode("i", text_node.text)
    elif text_node.text_type.value == "code":
        return LeafNode("code", text_node.text)
    elif text_node.text_type.value == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type.value == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("invalid texttype")

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_text):
        if self.text == other_text.text and self.text_type == other_text.text_type and self.url == other_text.url:
            return True
        else:
            return False
        
    def __repr__(self):
        url_ending = ""
        if self.url != None:
            url_ending += ", "+self.url


        return (f"TextNode({self.text}, {self.text_type}{url_ending})")
    
    
