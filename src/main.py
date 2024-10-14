import os, shutil
from copystatic import copy_files
from generate_page import generate_page_recursively

root = "/home/andrew/workspace/github.com/akshelstad/ssgen/"
dir_path_static = root + "static/"
dir_path_public = root + "public/"
dir_content = root + "content/"

f_content = dir_content + "index.md"
f_template = root + "template.html"
# f_page = dir_path_public + "index.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)

    generate_page_recursively(dir_content, f_template, dir_path_public)

if __name__ == "__main__":
    main()