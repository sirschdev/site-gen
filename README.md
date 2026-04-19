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
