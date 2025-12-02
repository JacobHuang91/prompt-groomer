"""
TextPacker Demo - Text Completion APIs

Shows how to use TextPacker for base models and completion endpoints.
Demonstrates token optimization through HTML cleaning and MARKDOWN formatting.
"""

from dotenv import load_dotenv
from openai import OpenAI

from prompt_refiner import (
    ROLE_ASSISTANT,
    ROLE_CONTEXT,
    ROLE_QUERY,
    ROLE_SYSTEM,
    ROLE_USER,
    NormalizeWhitespace,
    StripHTML,
    TextFormat,
    TextPacker,
)

# Load environment variables from .env file
load_dotenv()


def main():
    # RAG documents with messy HTML and excessive whitespace (common in web scraping)
    doc_html = """
    <div class="doc">
        <h2>TextPacker   Overview</h2>
        <p>TextPacker   is   optimized   for   text   completion   APIs.
        It   supports   multiple   formatting   strategies   to   prevent
        instruction   drifting   in   base   models.</p>

        <script>analytics.track();</script>
        <style>.sidebar { display: none; }</style>
        <nav><ul><li>Home</li></ul></nav>
    </div>
    """

    # Initialize packer with MARKDOWN format and automatic token savings tracking
    packer = TextPacker(
        text_format=TextFormat.MARKDOWN,
        separator="\n\n",
        model="gpt-3.5-turbo-instruct",
        track_savings=True,
    )

    # Add system instructions
    packer.add(
        "You are a QA assistant. Answer questions based on the provided context.",
        role=ROLE_SYSTEM,
    )

    # Add RAG documents with automatic cleaning pipeline
    packer.add(doc_html, role=ROLE_CONTEXT, refine_with=[StripHTML(), NormalizeWhitespace()])
    packer.add(
        "The library includes 5 modules: Cleaner, Compressor, Scrubber, Analyzer, and Packer.",
        role=ROLE_CONTEXT,
    )

    # Add conversation history
    history = [
        {"role": ROLE_USER, "content": "What is prompt-refiner?"},
        {"role": ROLE_ASSISTANT, "content": "It's a Python library for optimizing LLM inputs."},
        {"role": ROLE_USER, "content": "Does it reduce costs?"},
        {"role": ROLE_ASSISTANT, "content": "Yes, by removing unnecessary tokens it can save 10-20% on API costs."},
    ]
    packer.add_messages(history)

    # Add current query
    packer.add("What is TextPacker and how does it work?", role=ROLE_QUERY)

    # Pack into text format with priority-based selection
    prompt = packer.pack()

    # Get automatic token savings
    savings = packer.get_token_savings()

    if savings:
        print("Token Optimization (automatic tracking):")
        print(f"  Before: {savings['original_tokens']} tokens")
        print(f"  After:  {savings['refined_tokens']} tokens")
        print(f"  Saved:  {savings['saved_tokens']} tokens ({savings['saving_percent']})")
        print()

    print(f"Context Management:")
    print(f"  Packed {len(packer.get_items())} items")
    print()

    print("Formatted Prompt:")
    print("-" * 80)
    print(prompt)
    print("-" * 80 + "\n")

    # Call OpenAI Completions API
    client = OpenAI()
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=256,
        temperature=0.7,
    )

    print("Response:")
    print(response.choices[0].text)


if __name__ == "__main__":
    main()
