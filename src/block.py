from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(block):
    headings = ('# ', '## ', '### ', '#### ', '##### ', '###### ')
    split_block = block.split('\n')
    i = 1
    ordered_res = True
    for line in split_block:
        if line.startswith(f"{i}. ") == False:
            ordered_res = False
            break
        i += 1
    if block.startswith(headings):
        return BlockType.HEAD
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    elif all(line.startswith('>') for line in split_block):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in split_block):
        return BlockType.UNORDERED
    elif ordered_res == True:
        return BlockType.ORDERED
    else:
        return BlockType.PARAGRAPH


    
    
    

