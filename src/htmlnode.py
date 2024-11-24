class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            return ''.join([f' {k}="{v}"' for k,v in self.props.items()])
        
        return ''
    
    def __repr__(self):
        return f"HTMLNode, {self.tag}, {self.value}, {self.children}, {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            # return value as raw text
            return str(self.value)
        
        if self.props:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode, {self.tag}, {self.value}, {self.props}"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('no tag')

        if not self.children:
            # return value as raw text
            raise ValueError('No children')
        
        node_and_children = ''
        for child in self.children:
            
            node_and_children += child.to_html()

        return f'<{self.tag}>{self.props_to_html()}{node_and_children}</{self.tag}>'
