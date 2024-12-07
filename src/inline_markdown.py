import re
from textnode import TextNode, TextType

def main():
    textnode = [TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)]
    print('RESULT:', split_nodes_link(textnode))


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



def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        current_node = []
        node_text = node.text
        images = extract_markdown_images(node_text)


        for image in images:
            alt_text, image_link = image
            before, after = node_text.split(f"![{alt_text}]({image_link})", 1)
            if before != '':
                current_node.append(TextNode(before, TextType.TEXT))
            
            current_node.append(TextNode(alt_text, TextType.IMAGE, image_link))


            node_text = after

    return current_node

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        current_node = []
        node_text = node.text
        links = extract_markdown_links(node_text)

        for link in links:
            # unpack link
            hyperlink_text, link_url = link
            hyperlink_text = hyperlink_text.strip()
            link_url = link_url.strip()

            before, after = node_text.split(f"[{hyperlink_text}]({link_url})", 1)
            
            if before != '':
                current_node.append(TextNode(before, TextType.TEXT))
            
            current_node.append(TextNode(hyperlink_text, TextType.LINK, link_url))
            node_text = after

    return current_node


    # split_nodes_link(old_nodes, delimiter, text_type):
    #     new_nodes = []

    #     for node in old_nodes:
    #         current_node = []
    #         if node.text_type != TextType.TEXT:
    #             new_nodes.append(node)
    #             continue

    #         if delimiter not in node.text:
    #             raise ValueError('Delimiter not in Node - Invalid Markdown Text')

    #         node_text = str(node.text)
    #         text_sections = node_text.split(delimiter)
    #         for i, section in enumerate(text_sections):
    #             if not section:
    #                 continue
    #             if i % 2 == 0:
    #                 current_node.append(TextNode(section, TextType.TEXT))
    #             else:
    #                 current_node.append(TextNode(section, text_type))

    #         new_nodes.extend(current_node)
    #     return new_nodes


if __name__=="__main__":
    main()