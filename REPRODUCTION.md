
# FTEC5660 Reproducibility Study

## Project

**LLM-as-a-Verifier: A General-Purpose Verification Framework**

Original repository:
https://github.com/llm-as-a-verifier/llm-as-a-verifier

Original paper:
https://arxiv.org/abs/2607.05391

This project reproduces a subset of the Terminal-Bench 2.1 evaluation using DeepSeek and studies the effect of reducing the number of repeated verifications.

## 1. Environment

- Platform: macOS (Apple Silicon M5)
- Python: 3.11.16
- LLM Provider: DeepSeek API
- Original repository commit: `90e8fc215606447d6d31e9e24bff7200fb0c0994`
- Benchmark: Terminal-Bench 2.1
- Agent trajectories: mini-swe-agent / DeepSeek V4 Flash

The verification API uses the currently available DeepSeek Flash model. Since the model version may differ from the original experiments, exact numerical reproduction is not guaranteed.

## 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/liuhanpu-lyrid/llm-as-a-verifier.git
cd llm-as-a-verifier

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -e .
```

Configure `DEEPSEEK_API_KEY` in a local `.env` file.

Do not commit API keys or other credentials.

## 3. Dataset

We used a fixed subset of 20 tasks from Terminal-Bench 2.1.

The subset was selected using random seed 5660.

To regenerate the subset:

```bash
python scripts/make_subset.py
```

Each selected task contains five recorded agent trajectories. We used the first three trials per task for Best-of-3 evaluation.

Dataset composition:

- Total tasks: 20
- All-pass tasks: 16
- All-fail tasks: 1
- Swing tasks: 3

Swing tasks contain both successful and unsuccessful candidate trajectories.

## 4. Experimental Design

We compared two configurations:

| Parameter | Baseline | Modified |
|---|---|---|
| Repeated evaluations (K) | 2 | 1 |
| Pivot count | 2 | 2 |
| Number of trials | 3 | 3 |
| Random seed | 0 | 0 |
| Evaluation criteria | 3 | 3 |
| Max workers | 2 | 2 |

The evaluation criteria were:

- Specification
- Output Match
- Error Signals

The only experimental parameter changed was the number of repeated verifications, K.

## 5. Reproduction Commands

Baseline (K=2):

```bash
python scripts/run.py terminal_bench_2.1_subset20_k2 \
  --n-trials 3 \
  --n-evaluations 2 \
  --pivots 2 \
  --seed 0 \
  --max-workers 2
```

Modified (K=1):

```bash
python scripts/run.py terminal_bench_2.1_subset20_k1 \
  --n-trials 3 \
  --n-evaluations 1 \
  --pivots 2 \
  --seed 0 \
  --max-workers 2
```

Both configurations use separate local score caches and result files.

## 6. Results

| Metric | Baseline K=2 | Modified K=1 |
|---|---:|---:|
| Pass@1 | 88.3% | 88.3% |
| Verifier Accuracy | 95.0% | 95.0% |
| Oracle (Best-of-3) | 95.0% | 95.0% |
| API Calls | 84 | 42 |
| Input Tokens | 11,661,898 | 5,830,949 |
| Output Tokens | 383,451 | 156,172 |
| Total Tokens | 12,045,349 | 5,987,121 |
| Execution Time | 21m 27s | 9m 25s |
| Errors | 0 | 0 |

Reducing K from 2 to 1 resulted in:

- No observed change in selection accuracy.
- 50.0% fewer API calls.
- 50.3% lower total token consumption.
- 56.1% shorter execution time.

## 7. Normalized Cost Comparison

Actual API charges depend on server-side caching.

The measured input cache hit rates were:

- Baseline: 85.0%
- Modified: 99.9%

To compare costs under consistent assumptions, we estimated the cost of both runs using the same DeepSeek Flash off-peak prices and treating all input tokens as uncached.

- Input: $0.15 per million tokens
- Output: $0.60 per million tokens

Estimated normalized costs:

- Baseline: $1.979
- Modified: $0.968
- Reduction: 51.1%

These are theoretical standardized estimates, not actual API charges.

## 8. Limitations

Only 3 of the 20 selected tasks were swing tasks, limiting the statistical strength of the accuracy comparison.

The unchanged accuracy does not establish that reducing K will preserve performance on larger or more difficult datasets.

The verification model may also differ from the model used in the original reported experiments.

Server-side caching and runtime conditions can affect measured latency and actual API charges.

## 9. Conclusion

On the evaluated subset, reducing the number of verification repetitions from two to one maintained the same 95.0% selection accuracy while reducing API calls by 50.0% and total token usage by 50.3%.

The result suggests that repeated verification may be reduced in some settings without an observed loss of accuracy. However, a larger and more diverse evaluation is necessary to establish whether this finding generalizes.

## 10. Experimental Logs

The original outputs are available in:

- `reproduction_logs/subset20_baseline_k2.txt`
- `reproduction_logs/subset20_modified_k1.txt`
