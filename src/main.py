import os
import shutil
from textnode import TextNode, TextType

def copy_static_to_public(source="./static", target="./public", delete=False):
  if not os.path.exists(source):
    raise Exception("Source-Folder for static content doesn't exist")
  shutil.rmtree()
  if not os.path.exists(target):






def main():
  copy_static_to_public(delete=True)






if __name__ == "__main__":
  main()
