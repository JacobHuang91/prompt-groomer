# Prompt Groomer Benchmarks

This directory contains different benchmarking approaches to validate the cost-effectiveness of prompt-groomer.

## 📊 Available Benchmarks

### [`custom/`](custom/) - Custom A/B Testing

A custom A/B testing approach that compares raw vs groomed prompts:
- Tests 3 grooming strategies (minimal, standard, aggressive)
- Uses 30 curated test cases (SQuAD + RAG scenarios)
- Measures token reduction and response quality
- Quality evaluation via cosine similarity + LLM-as-a-judge

**Cost**: ~$2-5 per full run (using gpt-4o-mini)

**When to use**: Quick validation, proving concept, establishing baseline metrics

[→ See custom benchmark documentation](custom/README.md)

---

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   uv pip install -e ".[benchmark]"
   ```

2. **Set up API key**:
   ```bash
   cd benchmark/custom
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Run a benchmark**:
   ```bash
   cd custom
   python benchmark.py
   ```

## 📈 Choosing a Benchmark

| Benchmark | Speed | Cost | Accuracy | Best For |
|-----------|-------|------|----------|----------|
| **custom** | Fast | Low | Good | Quick validation, CI/CD |
| **promptfoo** | - | - | - | *(coming soon)* |
| **ragas** | - | - | - | *(coming soon)* |

## 🤝 Contributing

Have ideas for new benchmarking approaches? Open an issue or PR!

Potential future benchmarks:
- Industry-standard benchmarks (MMLU, HellaSwag, etc.)
- Production traffic replay
- Multi-model comparison
- Cost/latency optimization analysis
