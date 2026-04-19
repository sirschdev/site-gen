# Static Site Generator

A Python-based static site generator from the [Boot.dev](https://www.boot.dev) course that converts Markdown files into a complete HTML website.

## Features

### Markdown Parsing

The generator supports a comprehensive markdown syntax:

- **Headings**: `# H1` through `###### H6`
- **Block Elements**:
  - Paragraphs with automatic line joining
  - Code blocks with triple backticks
  - Block quotes with `>`
  - Unordered lists with `-`
  - Ordered lists with `1.`, `2.`, etc.
- **Inline Formatting**:
  - **Bold** with `**text**`
  - _Italic_ with `_text_`
  - `Code` with backticks
  - [Links](url) with `[text](url)`
  - ![Images](url) with `![alt](url)`

### Site Generation

- Recursively processes markdown files from a `content/` directory
- Copies static assets (CSS, images) from `static/`
- Generates HTML output to `docs/` directory
- Uses a customizable HTML template with variable substitution (`{{ Title }}`, `{{ Content }}`)
- Supports base path argument for GitHub Pages deployment

## Project Structure

```
.
├── content/              # Markdown source files
│   ├── index.md
│   ├── blog/
│   │   ├── post1/
│   │   │   └── index.md
│   │   └── post2/
│   │       └── index.md
│   └── contact/
│       └── index.md
├── static/               # Static assets
│   ├── index.css
│   └── images/
├── docs/                 # Generated HTML output
├── src/                  # Python source code
│   ├── main.py           # Site generation entry point
│   ├── convert_block.py  # Block-level markdown parsing
│   ├── convert_inline.py # Inline markdown parsing
│   ├── htmlnode.py       # HTML node classes
│   ├── textnode.py       # Text node types
│   ├── test_*.py         # Unit tests
│   └── __pycache__/
├── template.html         # HTML template for all pages
├── build.sh              # Build script with base path
├── main.sh               # Quick build and serve
└── test.sh               # Run tests
```

## Usage

### Build the site

```bash
# Generate HTML to docs/ with root path
python3 src/main.py

# Generate with a base path (e.g., for GitHub Pages subdirectory)
python3 src/main.py "/site-gen/"
```

The generator will:
1. Copy all static files to `docs/`
2. Recursively convert all `.md` files in `content/` to `.html` in `docs/`
3. Substitute `{{ Title }}` and `{{ Content }}` in the template

### Run tests

```bash
python3 -m unittest discover -s src
```

### View locally

```bash
cd docs
python3 -m http.server 8888
```

Then open `http://localhost:8888` in your browser.

## Technical Details

### Architecture

The generator is built on three core concepts:

1. **TextNode**: Represents inline text with formatting (bold, italic, code, link, image)
2. **BlockNode**: Represents block-level elements (heading, paragraph, list, quote, code block)
3. **HTMLNode**: Renders text/block nodes into valid HTML with proper nesting and attributes

### Processing Pipeline

1. **Block Parsing**: Markdown is split by double newlines into blocks, then classified by type
2. **Inline Parsing**: Each block's content is parsed for inline formatting (bold, italic, etc.)
3. **HTML Generation**: Text and block nodes are converted to an HTML tree
4. **Rendering**: The tree is rendered to HTML strings and injected into the template

### Markdown Parsing Rules

- **Bold** requires `**text**` with no internal spaces
- **Italic** requires `_text_` with no internal spaces or uses word boundaries
- **Code blocks** must start with ` ``` ` on its own line and end with ` ``` `
- **Lists** require consistent `- ` or `1. ` prefixes on every line
- **Quotes** require `>` on every line
- **Ordered lists** must start at `1.` and increment by exactly 1

## Example Content

See `content/index.md` for a full example page with headings, paragraphs, lists, quotes, code blocks, links, and images.

## Testing

The project includes 95+ unit tests covering:
- Markdown-to-block conversion
- Block type detection
- Inline text parsing
- HTML node rendering
- Full document conversion

Run tests with:
```bash
python3 -m unittest discover -s src
```