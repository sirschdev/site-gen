import re
from enum import Enum

from htmlnode import ParentNode, LeafNode
from convert_inline import markdown_to_children_html_nodes, unordered_list_to_li, ordered_list_to_li, quote_to_html_node

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

class BlockNode():
  def __init__(self, text, block_type):
    self.block_type = block_type
    self.text = text

  def __eq__(self, other):
    if self.text == other.text and self.block_type == other.block_type:
      return True
    return False

  def __repr__(self):
    return f"BlockNode({self.text}, {self.block_type.value})"



def markdown_to_blocks(markdown):
  splitted = markdown.split("\n\n")
  new_blocks = []
  for block in splitted:
    new_block = block.strip()
    extra_new_block = new_block.strip("\n")
    new_blocks.append(extra_new_block)
  return list(filter(None, new_blocks))


def block_to_block_type(block):
  if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
    return BlockType.HEADING
  if block.startswith("```\n") and block.endswith("```"):
    return BlockType.CODE
  lines = block.split("\n")
  ol_index = 2
  if lines[0].startswith(">"):
    this_type = BlockType.QUOTE
    this_prefix = ">"
  elif lines[0].startswith("- "):
    this_type = BlockType.UNORDERED_LIST
    this_prefix = "- "
  elif lines[0].startswith("1. "):
    this_type = BlockType.ORDERED_LIST
    this_prefix = f"{ol_index}. "
  else:
    return BlockType.PARAGRAPH

  for line in lines[1:]:
    if line.startswith(this_prefix):
      if this_type == BlockType.ORDERED_LIST:
        ol_index += 1
        this_prefix = f"{ol_index}. "
      continue
    else:
      return BlockType.PARAGRAPH
  return this_type


def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  block_nodes = []
  for block in blocks:
    match block_to_block_type(block):
      case BlockType.CODE:
        cleaned_block = block[3:len(block) - 3].lstrip("\n")
        code_leaf_node = LeafNode("code", cleaned_block)
        block_node = ParentNode("pre",[code_leaf_node])

      case BlockType.HEADING:
        splitted = block.split(' ',maxsplit=1)
        prefix = splitted[0]
        content = splitted[1]
        child_nodes = markdown_to_children_html_nodes(content)
        block_node = ParentNode(f"h{len(prefix)}",child_nodes)

      case BlockType.QUOTE:
        child_nodes = quote_to_html_node(block)
        block_node = ParentNode("blockquote",child_nodes)
      
      case BlockType.UNORDERED_LIST:
        child_nodes = unordered_list_to_li(block)
        block_node = ParentNode("ul",child_nodes)
      
      case BlockType.ORDERED_LIST:
        child_nodes = ordered_list_to_li(block)
        block_node = ParentNode("ol",child_nodes)
      
      case BlockType.PARAGRAPH:
        child_nodes = markdown_to_children_html_nodes(block.replace("\n"," "))
        block_node = ParentNode("p",child_nodes)

      case _:
        raise NameError("BlockType not found")

    block_nodes.append(block_node)
  return ParentNode("div",block_nodes)



