"""Example usage of prompt-groomer."""

from prompt_groomer import Groomer
from prompt_groomer.ops import NormalizeWhitespace, StripHTML, TruncateTokens

# Define a cleaning pipeline
groomer = (
    Groomer()
    .pipe(StripHTML())
    .pipe(NormalizeWhitespace())
    .pipe(TruncateTokens(max_tokens=1000, strategy="middle"))
)

raw_input = "<div>  User input with <b>lots</b> of   spaces... </div>"

# Execute
clean_prompt = groomer.run(raw_input)

print("Raw input:")
print(raw_input)
print("\nCleaned output:")
print(clean_prompt)
