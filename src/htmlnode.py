class HTMLNode():
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def __repr__(self):
    print(f'tag: "{self.tag}", value: "{self.value}", children: "{self.children}", props: "{self.props}"')
    return f'tag: "{self.tag}", value: "{self.value}", children: "{self.children}", props: "{self.props}"'


  def to_html(self):
    raise NotImplementedError

  def props_to_html(self):
    if self.props == None or len(self.props) == 0:
      return ''
    prop_str = []
    for k, v in self.props.items():
      prop_str.append(f'{k}="{v}"')
    return " ".join(prop_str)


class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def __repr__(self):
    print(f'tag: "{self.tag}", value: "{self.value}", props: "{self.props}"')
    return f'tag: "{self.tag}", value: "{self.value}", props: "{self.props}"'

    
  def to_html(self):
    if self.value == None:
      raise ValueError("Leaf node must have a value")
    if self.tag == None:
      return str(self.value)
    if self.props == None:
      start_tag = f"<{self.tag}>"
    else:
      start_tag = f"<{self.tag} {self.props_to_html()}>"
    return f"{start_tag}{self.value}</{self.tag}>"



class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def __repr__(self):
    print(f'tag: "{self.tag}", children: "{self.children}", props: "{self.props}"')
    return f'tag: "{self.tag}", children: "{self.children}", props: "{self.props}"'


  def to_html(self):
    if self.tag == None:
      raise ValueError("Parent node must have a tag")
    if self.children == None or len(self.children) == 0:
      raise ValueError("Parent node must have at least one child")
    if self.props == None:
      start_tag = f"<{self.tag}>"
    else:
      start_tag = f"<{self.tag} {self.props_to_html()}>"
    children_html = []
    for child in self.children:
      children_html.append(child.to_html())
    return f"{start_tag}{''.join(children_html)}</{self.tag}>"