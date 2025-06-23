import re
import os
from pathlib import Path
import shutil
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

from splitter import *
from block import block_to_block_type, BlockType

def copy(source, destination):

    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    entries = os.listdir(source)
    for entry in entries:
    
        src = os.path.join (source, entry)
        dest = os.path.join (destination, entry)
        if os.path.isfile(src):
                #path = os.path.join (source, entry)
                shutil.copy(src,dest)
                #print(dest)
        elif os.path.isdir(src):
             copy(src, dest)
             #print(dest)



def extract_title(markdown):
    if markdown.startswith("# ") == False:
        raise Exception("h1 header not found")
    else:
        header = markdown.split("# ", 1)
        header_s = header[1].strip()
        #return header_s

        header_s2 = header_s.split("\n", 1)
        return header_s2[0]
    
def change_extension(file_path, new_extension):
    base_name, _ = os.path.splitext(file_path)
    new_file_path = base_name +"." + new_extension
    return 
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path)
    from_content = from_file.read()
    from_file.close()

    template_file = open(template_path)
    template_content = template_file.read()
    template_file.close()

    content_node = markdown_to_html_node(from_content)
    content = content_node.to_html()
    #print(content)
    title = extract_title(from_content)
    #print(title)
    x = template_content.replace( "{{ Title }}" , title)
    y = x.replace( "{{ Content }}" , content)
    if not os.path.exists(os.path.dirname(dest_path)) and os.path.dirname(dest_path) is not "":
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(y)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    #print(os.listdir(dir_path_content))
    #print(os.listdir(dest_dir_path))

    entries = os.listdir(dir_path_content)
    for entry in entries:
    
        src = os.path.join (dir_path_content, entry)
        dest = os.path.join (dest_dir_path, entry)
        #print(src)
        if os.path.isfile(src):
           #print(src)
           #print(dest)
           #print(template_path)
           if Path(src).suffix == ".md":
               dest = Path(dest).with_suffix(".html")
               
           generate_page(src, template_path, dest)
        # if os.path.isdir(src):
        #     generate_pages_recursive(src, template_path, dest_dir_path)
        # elif os.path.isfile(src):
        #     print (src)
        elif os.path.isdir(src):
           generate_pages_recursive(src, template_path, dest)


def main():
    #print("youkoso, sekai yo")
    # items = []

    copy("static", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")
    #print (extract_title("# Hello"))
    # print (new_items)

    




    

main()
