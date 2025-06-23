class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_string = ""
        if self.props != None:
            for x in self.props:
                props_string += " "+ x + "=\"" + self.props[x] + "\""

        return props_string
    
    def __repr__(self):
        tag_str = ""
        if self.tag != None:
            tag_str = self.tag + ", "
        val_str = ""
        if self.value != None:
            val_str = self.value + ", "
        children_node = ""
        if self.children != None:
            for x in self.children:
                if x.tag == None:
                    children_node += x.value + ", "
                else:
                    children_node += x.tag + ", " + x.value + ", "

        node_props = ""
        if self.props != None:
            node_props = self.props_to_html()
        return "HTMLNode("+ tag_str + val_str + children_node + node_props + ")"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("no value")
        elif self.tag == None:
            return self.value
        html_tag = ""
        html_tag += "<"+ self.tag + self.props_to_html() + ">"+self.value+"</"+ self.tag + ">"
        return html_tag
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None:
            raise ValueError("parent node needs children")
        children_html = ""
        for x in self.children:
            children_html += x.to_html()
        html_tag = ""
        html_tag += "<"+ self.tag + self.props_to_html() + ">"+children_html+"</"+ self.tag + ">"
        return html_tag
    