from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

tag_dict = {
    block_type_paragraph : "p",
    block_type_heading : ["h1", "h2", "h3", "h4", "h5", "h6"],
    block_type_code : ["code", "pre"],
    block_type_quote : "blockquote",
    block_type_olist : ["ol", "li"],
    block_type_ulist : ["ul", "li"]
}

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return create_node_paragraph(block)
    if block_type == block_type_heading:
        return create_node_heading(block)
    if block_type == block_type_code:
        return create_node_code(block)
    if block_type == block_type_olist:
        return create_node_olist(block)
    if block_type == block_type_ulist:
        return create_node_ulist(block)
    if block_type == block_type_quote:
        return create_node_blockquote(block)
    raise ValueError("Invalid block type.")

def create_node_heading(text):
    heading_num = text.count("#") - 1
    outer_tag = tag_dict[block_to_block_type(text)][heading_num]
    value = text[heading_num + 2:]
    return ParentNode(outer_tag, text_to_children(value))

def create_node_code(text):
    outer_tag = tag_dict[block_type_code][1]
    inner_tag = tag_dict[block_type_code][0]
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("Invalid code block.")
    value = text[4:-3]
    code = ParentNode(inner_tag, text_to_children(value))
    return ParentNode(outer_tag, [code])

def create_node_olist(text):
    outer_tag = tag_dict[block_type_olist][0]
    inner_tag = tag_dict[block_type_olist][1]
    child_nodes = []
    for line in text.split("\n"):
        value = line[3:]
        child_nodes.append(ParentNode(inner_tag, text_to_children(value)))
    return ParentNode(outer_tag, child_nodes)

def create_node_ulist(text):
    outer_tag = tag_dict[block_type_ulist][0]
    inner_tag = tag_dict[block_type_ulist][1]
    child_nodes = []
    for line in text.split("\n"):
        value = line[2:]
        child_nodes.append(ParentNode(inner_tag, text_to_children(value)))
    return ParentNode(outer_tag, child_nodes)

def create_node_blockquote(text):
    outer_tag = tag_dict[block_type_quote]
    new_lines = []
    for line in text.split("\n"):
        if not line.startswith(">"):
            raise ValueError("Invalid quote block.")
        new_lines.append(line.lstrip(">").strip())
    value = " ".join(new_lines)
    return ParentNode(outer_tag, text_to_children(value))

def create_node_paragraph(text):
    outer_tag = tag_dict[block_type_paragraph]
    lines = text.split("\n")
    paragraph = " ".join(lines)
    return ParentNode(outer_tag, text_to_children(paragraph))

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return children_nodes



