"""
Example: Precise Token Counting with Optional Tiktoken

Demonstrates the optional tiktoken dependency for precise token counting.

Installation:
- Default (lightweight): pip install llm-prompt-refiner
- Precise mode: pip install llm-prompt-refiner[token]
"""

from prompt_refiner import ContextPacker, CountTokens, PRIORITY_HIGH, PRIORITY_SYSTEM

print("=" * 70)
print("Token Counting Modes")
print("=" * 70)

# Example 1: CountTokens - Check which mode is active
print("\n1. CountTokens - Detection of tiktoken")
print("-" * 70)

counter = CountTokens(model="gpt-4")
print(f"Precise mode enabled: {counter.is_precise}")
print(f"Using tiktoken: {'Yes ✓' if counter.is_precise else 'No (estimation mode)'}")

text = "The quick brown fox jumps over the lazy dog"
counter.process(text)
stats = counter.get_stats()
print(f"\nText: '{text}'")
print(f"Token count: {stats['tokens']}")
print(f"Mode: {'Precise (tiktoken)' if counter.is_precise else 'Estimation (chars/4)'}")

# Example 2: ContextPacker - Safety buffer in estimation mode
print("\n\n2. ContextPacker - Safety Buffer")
print("-" * 70)
print("Creating ContextPacker with max_tokens=100...")
print()

packer = ContextPacker(max_tokens=100, model="gpt-4")

print(f"\nPacker settings:")
print(f"  Raw max tokens: {packer.raw_max_tokens}")
print(f"  Effective max tokens: {packer.effective_max_tokens}")
print(f"  Safety buffer: {packer.raw_max_tokens - packer.effective_max_tokens} tokens")

# Example 3: Comparison between modes
print("\n\n3. Estimation vs Precise Mode")
print("-" * 70)

texts = [
    "Hello world!",
    "This is a longer sentence with more words.",
    "UTF-8: 你好世界 (Chinese characters)",
    "Code: def hello(): return 'world'",
]

counter_est = CountTokens(model="gpt-4")

print(f"\nMode: {'Precise' if counter_est.is_precise else 'Estimation'}")
print(f"\n{'Text':<50} {'Tokens':>10}")
print("-" * 62)

for text in texts:
    counter_est.process(text)
    stats = counter_est.get_stats()
    print(f"{text[:47]+'...' if len(text) > 50 else text:<50} {stats['tokens']:>10}")

# Example 4: Why the safety buffer matters
print("\n\n4. Why the 10% Safety Buffer Matters")
print("-" * 70)
print("""
In estimation mode (without tiktoken), token counting uses the approximation:
  1 token ≈ 4 characters

However, this can be inaccurate for:
- Non-English text (Chinese, Arabic, etc.)
- Special characters and emojis
- Code with lots of punctuation
- Numbers and dates

The 10% safety buffer (90% effective capacity) helps prevent context overflow
by being conservative with the budget.

Example:
  max_tokens=1000 (requested)
  → effective_max_tokens=900 (actual limit in estimation mode)
  → 100 token buffer to account for estimation errors

When you install tiktoken, the buffer is removed:
  max_tokens=1000 (requested)
  → effective_max_tokens=1000 (actual limit in precise mode)
  → 0 token buffer (no estimation error)
""")

# Example 5: Installation instructions
print("\n5. How to Enable Precise Mode")
print("-" * 70)
print("""
To enable precise token counting with tiktoken:

    pip install llm-prompt-refiner[token]

This installs tiktoken as an optional dependency.

Benefits of precise mode:
✓ Accurate token counts (no approximation)
✓ Full token budget utilization (no 10% safety buffer)
✓ Better handling of non-English text
✓ More predictable context management

When to use estimation mode:
✓ Lightweight deployments
✓ Performance-critical applications
✓ Development/testing environments
✓ When approximate counts are sufficient
""")

print("=" * 70)
print("Example complete!")
print("=" * 70)
