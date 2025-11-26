"""Example: Different truncation strategies."""

from prompt_groomer import Groomer
from prompt_groomer.ops import TruncateTokens

# Sample long text
long_text = "The quick brown fox jumps over the lazy dog while exploring the vast wilderness"

print("Original text:")
print(long_text)
print(f"Word count: {len(long_text.split())}")
print()

# Strategy 1: Keep start (truncate end)
groomer_end = Groomer().pipe(TruncateTokens(max_tokens=8, strategy="end"))
result_end = groomer_end.run(long_text)
print("Strategy 'end' (keep start):")
print(result_end)
print()

# Strategy 2: Keep end (truncate start)
groomer_start = Groomer().pipe(TruncateTokens(max_tokens=8, strategy="start"))
result_start = groomer_start.run(long_text)
print("Strategy 'start' (keep end):")
print(result_start)
print()

# Strategy 3: Keep both ends (truncate middle)
groomer_middle = Groomer().pipe(TruncateTokens(max_tokens=8, strategy="middle"))
result_middle = groomer_middle.run(long_text)
print("Strategy 'middle' (keep start and end):")
print(result_middle)
