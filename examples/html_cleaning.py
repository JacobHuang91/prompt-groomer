"""Example: Cleaning HTML content."""

from prompt_groomer import Groomer
from prompt_groomer.ops import NormalizeWhitespace, StripHTML

# Create a pipeline for cleaning HTML
html_cleaner = Groomer().pipe(StripHTML()).pipe(NormalizeWhitespace())

# Example HTML content
html_content = """
<div class="content">
    <h1>Title</h1>
    <p>This is a <strong>paragraph</strong> with <em>formatting</em>.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</div>
"""

cleaned = html_cleaner.run(html_content)

print("Original HTML:")
print(html_content)
print("\nCleaned text:")
print(cleaned)
