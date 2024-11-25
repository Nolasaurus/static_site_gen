import re
from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        current_node = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            raise ValueError('Delimiter not in Node - Invalid Markdown Text')

        node_text = str(node.text)
        text_sections = node_text.split(delimiter)
        for i, section in enumerate(text_sections):
            if not section:
                continue
            if i % 2 == 0:
                current_node.append(TextNode(section, TextType.TEXT))
            else:
                current_node.append(TextNode(section, text_type))

        new_nodes.extend(current_node)
    return new_nodes


def extract_markdown_images(text):
    images = []
    outer_pattern = r'(!\[.*?\]\(.*?\))'
    inner_patten = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(outer_pattern, text)
    for match in matches:
        inner_match = re.match(inner_patten, match)
        if inner_match:
            alt_text, url = inner_match.groups()
            images.append((alt_text, url))
    return images

def extract_markdown_links(text):
    links = []
    outer_pattern = r'(\[.*?\]\(.*?\))'
    inner_patten = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(outer_pattern, text)
    for match in matches:
        inner_match = re.match(inner_patten, match)
        if inner_match:
            link_text, url = inner_match.groups()
            links.append((link_text, url))
    return links
