import os
import shutil
import sys

from convert_block import markdown_to_html_node
from convert_inline import extract_title

def copy_static_to_public(source="./static", target="./public", delete=False):
  if not os.path.exists(source):
    raise Exception("Source-Folder for static content doesn't exist")
  if delete and os.path.exists(target):
    shutil.rmtree(target)
  if not os.path.exists(target):
    os.mkdir(target)
  child_dirs = os.listdir(source)
  if child_dirs:
    for element in child_dirs:
      src_path = os.path.join(source, element)
      target_path = os.path.join(target, element)
      if os.path.isfile(src_path):
        shutil.copy(src_path, target_path)
        print(f"copied {src_path} to {target_path}")
      else:
        copy_static_to_public(src_path, target_path)

def generate_page(from_path, template_path, dest_path, basepath):
  print(f"Generating Page from {from_path} to {dest_path} using {template_path}")
  with open(from_path) as file:
    markdown = file.read()
  with open(template_path) as temp:
    template = temp.read()
  html = markdown_to_html_node(markdown).to_html()
  title = extract_title(markdown)
  template = template.replace("{{ Title }}",title).replace("{{ Content }}",html).replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
  dest_directories = dest_path.split("/")
  dest_directories.pop()
  dest_directory = "/".join(dest_directories)
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory, exist_ok=True)
  with open(dest_path, "w") as file:
    file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
  child_dirs = os.listdir(dir_path_content)
  if child_dirs:
    for element in child_dirs:
      src_path = os.path.join(dir_path_content, element)
      html_element = element[0:-3] + ".html"
      target_path = os.path.join(dest_dir_path, element)
      target_file_name = os.path.join(dest_dir_path, html_element)
      if os.path.isfile(src_path):
        if element[-3:] == ".md":
          generate_page(src_path, template_path, target_file_name, basepath)
          print(f"transformed {src_path} to {target_file_name}")
      else:
        generate_pages_recursive(src_path, template_path, target_path, basepath)



def main():
  TARGET_PATH = "./docs"
  basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
  copy_static_to_public("./static",TARGET_PATH,delete=True)
  generate_pages_recursive(f"./content","./template.html",TARGET_PATH, basepath)
  


if __name__ == "__main__":
  main()
