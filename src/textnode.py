from enum import Enum

class TextType(Enum):
    NORMAL = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINKS = 'links'
    IMAGES = 'images'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        same_text = (self.text == other.text)
        same_text_type = (self.text_type == other.text_type)
        same_url =  (self.url == other.url)

        return same_text and same_text_type and same_url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
