import os
from markdown_blocks import markdown_to_blocks, markdown_to_html


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("#").strip()
    raise Exception("No h1 header found.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, 'r') as f:
        md_file = f.read()
    with open(template_path, 'r') as f:
        tmp_file = f.read()
    
    html_string = markdown_to_html(md_file).to_html()
    title = extract_title(md_file)
    html_file = tmp_file.replace(
        "{{ Title }}", title).replace(
            "{{ Content }}", html_string)
    
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    
    with open(dest_path + "index.html", 'w') as f:
        f.write(html_file)

def generate_page_recursively(dir_path_content, template_path, dest_dir_path):
    # print(os.listdir(dir_path_content))

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, dest_dir_path)
        else:
            item_path += "/"
            dest_path = os.path.join(dest_dir_path, item + "/")
            generate_page_recursively(item_path, template_path, dest_path)


