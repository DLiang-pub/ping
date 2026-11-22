---
license: cc-by-nc-4.0
language:
- en
tags:
- nanochat
- from-scratch
- historical
- time-capsule
---

# Ping

A small English-language model set on the last evening of 31 December 1999. Its base model was trained from scratch with nanochat on text published by that date, then post-trained with modern conversation data. It is intended for non-commercial experimentation and an openly imperfect historical chat demo.

**Release:** the frozen Ping checkpoint, its tokenizer and a chat script are in the [Hugging Face repository](https://huggingface.co/onlatentstates/ping). The demo is at [ping1999.com](https://www.ping1999.com) until the end of 31 December 2026, Singapore time.

Write-up and charts: [DLiang-pub/ping](https://github.com/DLiang-pub/ping) · Demo: [ping1999.com](https://www.ping1999.com)

## Model details

| Field | Value |
|---|---|
| Architecture | nanochat d32; 32 layers, width 2,048, value embeddings on 16 layers, windowed attention |
| Parameters | Approximately 1.68 billion in the network; 2,818,575,450 in total with its embedding lookup tables |
| Tokenizer | Project-trained, 32,768 tokens |
| Model context | 4,096 tokens |
| Base training | 9,600 steps; 20.1 billion training tokens |
| Base publication cutoff | 31 December 1999 |
| Final chat pass | 113,634 rows; 559 steps |
| Training hardware | GPUs rented from RunPod, in its US data centres: base about 33 hours on 4× H100; chat stages 31 minutes on 4× H100 and 13 minutes on 1× H200 |
| Frozen checkpoint | 18 November 2026; step 559 |
| Runtime verified | Public nanochat at commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; clean-room load on 21 November 2026; the published files checked again on 22 November 2026 |

The base model started from random weights. It is not a fine-tune of the stock nanochat checkpoint.

## Training data and post-training

The base model’s corpus came from about 70 sources: historical books, newspapers, Usenet posts, government and parliamentary records, UN speeches, science, reference material, code and documentation. Dates refer to the extracted text, not download dates. Modern front matter was removed; unknown dates were excluded. The corpus holds about 14 billion tokens of distinct text; scarcer and more conversational material was read more than once and the largest collections were sampled, giving the 20.1 billion training tokens.

| Kind of text | Share of the training text |
|---|---:|
| Usenet discussion | 23.2% |
| Government and parliamentary records | 23.1% |
| Books and language corpora | 17.8% |
| Science and medicine | 12.0% |
| Newspapers | 10.4% |
| Reference works and UN records | 4.4% |
| Patents | 3.0% |
| Code and documentation | 2.0% |
| Verse, case law and geological surveys | 4.1% |

Post-training used modern text in two stages:

1. SmolTalk conversations screened for anachronisms, identity lessons, maths and multiple-choice exercises. Some modern technical knowledge was retained.
2. A final pass combining custom Ping conversations, screened SmolTalk and exercises including GSM8K, MMLU and ARC. Qwen3.8-Flash-Next wrote the custom examples from fact cards and pre-2000 material, followed by filtering. The exercises used MMLU’s auxiliary_train split and the training splits of GSM8K and ARC; rows found to overlap the benchmarks’ test questions were removed.

The 1999 boundary applies to the base model, not all training text or every generated answer. Modern knowledge can still appear. No text written by Claude was used to train Ping: Claude wrote the project’s code and the lesson writer’s instructions, and ran the evaluations; Qwen wrote the custom training conversations. Neither the corpus nor the private lesson files are redistributed. Demo visitors’ chats are never training text.

See [the project README](https://github.com/DLiang-pub/ping/blob/main/README.md) for the grouped source table and training account. [Source credits](sources.md).

## Evaluation

### General benchmarks

| Measurement | Base model | Ping | Comparator |
|---|---:|---:|---|
| CORE | 0.2437 | 0.246632 | GPT-2 Large 0.2165; GPT-2 XL 0.2541; stock nanochat d32 base 0.3168, author-published |
| ARC-Easy, likelihood | 56.7% | 59.6% | GPT-2 XL 57.6% |
| ARC-Challenge, likelihood | 30.6% | 33.8% | GPT-2 XL 28.7% |
| MMLU, likelihood | 30.0% | 30.5% | GPT-2 XL 30.3% |
| ARC-Easy, chat | — | 57.3% | Stock nanochat d32 chat 67.7% |
| ARC-Challenge, chat | — | 43.1% | Stock nanochat d32 chat 49.7% |
| MMLU, chat | — | 37.2% | Stock nanochat d32 chat 40.4% |
| GSM8K, chat | — | 10.6% | Stock nanochat d32 chat 12.4% |

Except for stock nanochat’s published CORE, the comparisons above were measured by the project, on the datasets’ test splits. CORE is the DCLM benchmark’s score over 22 tasks, as nanochat computes it. Stock nanochat’s base is not public and was not measured here. Stock nanochat was not measured on the likelihood ARC/MMLU rows. As a check on the harness: nanochat’s own reference CORE for GPT-2 XL is 0.257, and its author’s published chat scores for stock d32 (68.0%, 49.9%, 40.5%, 12.7%) are within half a point of the figures measured here.

The base model is the fairer GPT-2 comparison: Ping subsequently received multiple-choice practice. Stock nanochat is the stronger general conversationalist: it leads every chat-format row, and on the 70 questions of the dated UN test below its replies averaged 44 words to Ping's 22. Likelihood and chat results use different scoring procedures. Differences in corpus, compute, architecture and post-training prevent these comparisons from isolating the effect of the historical cutoff.

### UN evaluations

| Test | Ping | Stock nanochat d32 | Scope |
|---|---:|---:|---|
| General pre-2000 UN knowledge | 45/60 | 47/60 | Inconclusive under the predeclared rule |
| UN as of December 1999, date supplied to both, supported subset | 13/25 | 1/25 | Custom historical test built from Ping’s reading |
| Held-out 1990s UN speeches, bits per byte; lower is better | Base model 0.620; chat model 0.752 | Chat model 0.712 | Base model leads; released chat model trails stock chat |

Both extra tests were built from Ping’s own reading. Specifications were fixed before the evaluated models answered, after Ping was trained; the 287 speech passages were held out of all Ping training. They are not neutral benchmarks or a controlled test of the corpus mix alone.

The dated test’s 25 headline facts are supported by Ping’s 1997–1999 UN records. Its full set contains 35 facts, of which 22 are covered by Ping’s chat lessons. Ping missed 12 of the headline 25. The sampled pass gave 10/25 versus 2/25. AI marking concealed model names, but the time period often revealed the model.

The broader UN test had one blind AI reader and 15 uncertain primary verdicts, yielding possible scores of 43–46 for Ping and 42–54 for stock. Its sampled pass, 41 versus 39, was also inconclusive. No general UN-knowledge advantage is claimed.

### Conversation and reliability

| Measurement | Result |
|---|---:|
| Taught facts recalled, model alone | 487/630 |
| Unknown names not answered as known, development quiz | 62/70 |
| Untaught material correct without unsupported additions, through the page | 78/256 |
| Ordinary 1999 questions correct, outside lesson coverage | 12/52 |
| All visitor requirements retained in listening conversations | 8/32 |
| Development arithmetic turns correct, with the page’s calculator notes | 25/44; target 30 |
| Identity failures under deliberate pressure | 3/13 conversations |
| Post-1999 knowledge leaks in launch rehearsal | 0/208 turns |
| Period slips under technical probing | 13/36 conversations |

The conversation sets were frozen before the final lessons they tested were written. Most qualitative scores are AI-agent judgements, not human user-study results. The different denominators reflect different tests; the rehearsal’s zero leaks does not override failures under technical probing. In the general public conversation set, 23/127 replies contained a false statement.

## Uses, risks and safeguards

Intended use: non-commercial experimentation, historical conversation and research on a small model with a dated base corpus. Ping is unreliable for factual decisions, especially about real people, and is unsuitable for medical or other consequential advice. It can invent biographies, endorse false premises and produce hateful or dangerous replies.

**The weights and local chat wrapper do not include the demo’s external safeguards.** The hosted page supplies a calculator, a spelling hint, moderation and a rule-based guard. The guard gives fixed replies without asking Ping for certain accusations about people, medical emergencies/doses, requests to praise violence or insult groups, and selected sovereignty questions asking who is right. It can also block legitimate historical questions.

In a stress test of 119 prompts asked three times, two AI readers both marked **111/357 replies harmful through the moderated page before the guard**. The 21 November guarded-page repeat recorded **26/357**, with 213 turns answered by fixed lines. Neither number measures bare weights or ordinary visitor incidence. Corrections and a narrower sovereignty rule followed; the latest revision has not had the full test replayed with readers. The 26/357 count belongs to the tested 21 November configuration.

## Copying test

The exact release weights, verified by hash, continued 656 fifty-word source openings, including 550 from restricted sources. Each was tried as raw text and a chat continuation request, giving 1,312 replies of up to 120 tokens. Matching was measured against the 400 source words following each opening.

| Source | Passages | Longest matching word run, raw | Chat |
|---|---:|---:|---:|
| Institutional Books | 180 | 25 | 9 |
| Encyclopedias from 1999 | 102 | 9 | 7 |
| British National Corpus | 102 | 5 | 8 |
| COCA | 100 | 5 | 5 |
| Usenet | 75 | 5 | 8 |
| All sources, including other sampled collections | 656 | 25 | 23 |

No continuation exceeded the project’s more-than-50-word threshold. The longest match was a 25-word contents-list passage from an 1854 Hume volume; the 23-word match was US government text. This sample does not prove no memorisation. It did not cover demo-temperature sampling, other prompt lengths or highly repeated passages. No source passage is reproduced here.

## How to run

The files use nanochat's checkpoint layout, not the Transformers `AutoModel` format. The verified route is a CUDA GPU and the pinned nanochat checkout below. Allow **at least 24 GB of free GPU memory**: the load peaked at 21 to 22 GiB, because nanochat's loader briefly holds the model twice. It has also run on a 16 GB Apple Silicon Mac mini, more slowly; that route and smaller graphics cards were not part of the release check.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first if it is not already available, then download the complete snapshot:

```bash
uv tool install huggingface_hub
hf download onlatentstates/ping --revision frozen-2026-11-18 --local-dir ./ping-release
python3 ./ping-release/verify_release.py

export NANOCHAT_BASE_DIR="$(cd ./ping-release && pwd)"
git clone https://github.com/karpathy/nanochat
cd nanochat
git checkout 92d63d4e8bb4df75c3b71618f31ddde2378b2bcd
uv sync --extra gpu
uv run python "$NANOCHAT_BASE_DIR/ping_chat.py" --check --device-type cuda
uv run python "$NANOCHAT_BASE_DIR/ping_chat.py" --device-type cuda
```

`NANOCHAT_BASE_DIR` must be an absolute path to the downloaded release. Run the wrapper from the nanochat checkout, as above. Keep the snapshot's layout intact:

```text
ping-release/
  README.md
  sources.md
  LICENSE
  LICENSE-CODE
  ping_chat.py
  verify_release.py
  release-checkpoint.json
  checksums.sha256
  tokenizer/
    tokenizer.pkl
    token_bytes.pt
  chatsft_checkpoints/ping/
    model_000559.pt
    meta_000559.json
```

`verify_release.py` checks the release files before model loading. The wrapper's `--check` separately verifies the weights and metadata hashes, loads the checkpoint and runs three fixed prompts. The supplied wrapper adds `[1999-12-31] Ping` and defaults to temperature 0.6, top-k 50, a 320-token reply cap and a 3,500-token window including the reply. Type `new` to reset or `quit` to exit. The upstream CLI loads the model but omits the date/persona preamble.

This wrapper runs the bare model. It does **not** provide the hosted demo's moderation, rule-based guard, calculator or spelling hint. Behaviour can therefore differ from the through-the-page evaluations above.

| File | SHA-256 |
|---|---|
| `model_000559.pt` (8,992,693,942 bytes) | `3a463f98b9544f009558219a052567800f52c9167e6ff7b993710416d8f016d3` |
| `meta_000559.json` | `4ed8c86ac51e0538b5c6d50c4846467fce6de976650b4cfddc8d739c319c9833` |

## Licence and attribution

The weights are licensed under **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)**: non-commercial sharing and adaptation are permitted with attribution, a licence link and an indication of changes. See the `LICENSE` file in the [Hugging Face repository](https://huggingface.co/onlatentstates/ping/blob/main/LICENSE) and the linked legal code for the terms.

The accompanying code is **MIT licensed**. Data sources have separate terms; neither licence grants rights in the underlying texts. The corpus and private lesson files are not distributed. Exact reproduction requires independent access to restricted sources.

Historical sources include Institutional Books, COCA, BNC, encyclopedias from 1999, Usenet, UN and parliamentary records, newspapers and scientific literature. Usenet posts remain their authors’ copyright; proprietary reference text is not redistributed. No blanket open-data claim is made. [Source credits](sources.md).

- **COCA:** The Corpus of Contemporary American English (Mark Davies), 1990–1999 texts, full-text data from https://www.corpusdata.org. About 3.8% of the base model's training text.
- **Institutional Books:** Institutional Books provided by the Institutional Data Initiative with source material contributed by Harvard Library, available at https://institutional.org/institutional-books. About 9.6% of the base model's training text.
- **British National Corpus:** [BNC source page](https://www.natcorp.ox.ac.uk/), under the applicable BNC User Licence.
- **UN records:** General Debate Corpus (Jankin, Baturo and Dasandi); Security Council records (Sakamoto and Matsuoka). [Source credits](sources.md).

Thanks to Andrej Karpathy for nanochat; Qwen3.8-Flash-Next for the custom lessons; the creators of SmolTalk, GSM8K, MMLU and ARC; and Mark Davies of COCA and the Institutional Data Initiative, whose collections gave Ping most of its books and its widest sample of 1990s American English. Claude assisted with implementation and evaluation.


## Hosted demo privacy

The demo is planned to close at the end of 31 December 2026, Singapore time. Chats are recorded for the owner’s review without the visitor’s address and deleted 90 days after closure. **Visitors’ chats are never used as training text.** No account is required; visitors should avoid personal information. This describes the project’s demo, not deployments by people downloading the weights.
