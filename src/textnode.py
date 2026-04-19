from enum import Enum

class TextType(Enum):
  BOLD = "BOLD"
  ITALIC = "ITALIC"
  LINK = "LINK"
  CODE = "CODE"
  IMAGE = "IMAGE"
  TEXT = "TEXT"

class TextNode():
  def __init__(self, text, text_type, url=None):
    if isinstance(text_type, TextType):
        self.text_type = text_type
    elif isinstance(text_type, str):
        self.text_type = TextType[text_type.upper()] 
    self.text = text
    self.url = url

  def __eq__(self, other):
    if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
      return True
    return False

  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

