
import re
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
  match text_node.text_type:
      case TextType.TEXT:
        return LeafNode(None, text_node.text)
      case TextType.BOLD:
        return LeafNode("b", text_node.text)
      case TextType.ITALIC:
        return LeafNode("i", text_node.text)
      case TextType.CODE:
        return LeafNode("code", text_node.text)
      case TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
      case TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
      case _:
        raise ValueError("Text has no valid type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):

  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    # delimiter escape
    len_deli = len(delimiter)
    escaped_deli = re.escape(delimiter)
    if "_" in delimiter or "~" in delimiter:
      split_keys = re.findall(rf"(\b{escaped_deli}\S(?:.*?\S)?{escaped_deli}\b)", node.text)
    elif delimiter == "`":
      split_keys = re.findall(rf"(`[^`]+`)", node.text)
    else:
      split_keys = re.findall(rf"({escaped_deli}\S(?:.*?\S)?{escaped_deli})", node.text)
    if len(split_keys) == 0:
      new_nodes.append(node)
      continue
    new_node = []
    current_text = node.text
    i = 0
    j = len(split_keys)
    for key in split_keys:
      i += 1
      split_text = current_text.split(key,maxsplit=1)
      if split_text[0] != "":
        new_node.append(TextNode(split_text[0],TextType.TEXT))
      clean_key = key[len_deli:len(key)-len_deli]
      new_node.append(TextNode(clean_key,text_type))
      if split_text[1] != "":
        current_text = split_text[1]
        if i == j:
          new_node.append(TextNode(split_text[1],TextType.TEXT))
    new_nodes.extend(new_node)
  return new_nodes


def extract_markdown_images(text):
  new_images = []
  images = re.findall(r"(?<=!\[)(.*?\]\(.*?)(?=\))", text)
  for img in images:
    image = tuple(img.split("]("))
    new_images.append(image)
  return new_images

def extract_markdown_links(text):
  new_links = []
  links = re.findall(r"(?<!!\[)(?<=\[)(.*?\]\(.*?)(?=\))", text)
  for link in links:
    link = tuple(link.split("]("))
    new_links.append(link)
  return new_links


def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    split_keys = extract_markdown_images(node.text)
    if len(split_keys)== 0:
      new_nodes.append(node)
      continue
    new_node = []
    current_text = node.text
    i = 0
    j = len(split_keys)
    for alt_text, url_text in split_keys:
      i += 1
      split_text = current_text.split(f"![{alt_text}]({url_text})",maxsplit=1)
      if split_text[0] != "":
        new_node.append(TextNode(split_text[0],TextType.TEXT))
      new_node.append(TextNode(alt_text,TextType.IMAGE,url_text))
      if split_text[1] != "":
        current_text = split_text[1]
        if i == j:
          new_node.append(TextNode(split_text[1],TextType.TEXT))
    new_nodes.extend(new_node)
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    split_keys = extract_markdown_links(node.text)
    if len(split_keys)== 0:
      new_nodes.append(node)
      continue
    new_node = []
    current_text = node.text
    i = 0
    j = len(split_keys)
    for link_text, url_text in split_keys:
      i += 1
      split_text = current_text.split(f"[{link_text}]({url_text})",maxsplit=1)
      if split_text[0] != "":
        new_node.append(TextNode(split_text[0],TextType.TEXT))
      new_node.append(TextNode(link_text,TextType.LINK,url_text))
      if split_text[1] != "":
        current_text = split_text[1]
        if i == j:
          new_node.append(TextNode(split_text[1],TextType.TEXT))
    new_nodes.extend(new_node)
  return new_nodes


def text_to_textnodes(text):
  start_node = TextNode(text,TextType.TEXT)
  end_nodes = [start_node]
  code_block_nodes = split_nodes_delimiter(end_nodes, "```", TextType.CODE)
  inline_code_block_nodes = split_nodes_delimiter(code_block_nodes, "`", TextType.CODE)
  img_nodes = split_nodes_image(inline_code_block_nodes)
  link_nodes = split_nodes_link(img_nodes)
  bold_nodes = split_nodes_delimiter(link_nodes, "**", TextType.BOLD)
  italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
  return italic_nodes


def markdown_to_children_html_nodes(markdown):
  text_nodes = text_to_textnodes(markdown)
  child_nodes = []
  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    child_nodes.append(html_node)
  return child_nodes


def unordered_list_to_li(markdown):
  #"- Item 1\n- Item 2"
  elements = markdown.split("\n")
  child_nodes = []
  for element in elements:
    content = element.lstrip("-").lstrip()
    grandchildren_nodes = markdown_to_children_html_nodes(content)
    child_nodes.append(ParentNode("li", grandchildren_nodes))
  return child_nodes


def ordered_list_to_li(markdown):
  #"1. Item 1\n2. Item 2"
  elements = markdown.split("\n")
  child_nodes = []
  for element in elements:
    content = element.lstrip("1234567890.").lstrip()
    grandchildren_nodes = markdown_to_children_html_nodes(content)
    child_nodes.append(ParentNode("li", grandchildren_nodes))
  return child_nodes


def quote_to_html_node(markdown):
  #"1. Item 1\n2. Item 2"
  elements = markdown.split("\n")
  full_quote = []
  for element in elements:
    full_quote.append(element.lstrip("> "))
  return markdown_to_children_html_nodes(" ".join(full_quote))

def extract_title(markdown):
  title = re.findall(r"(?<!\S)(# .*?\n)", markdown)[0]
  if title == None:
    raise Exception("No Title in Document. Add Title to doc")
  return title.lstrip("#").lstrip().rstrip("\n")