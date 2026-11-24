# Source credits and supporting datasets

The [project README](https://github.com/DLiang-pub/ping/blob/main/README.md) describes the historical source groups and selected dates. This page records selected credits and links; it is not a redistribution of the corpus or a claim that all source material has the same licence.

## Historical sources

- **COCA:** The [Corpus of Contemporary American English](https://www.english-corpora.org/coca/) (Mark Davies): its 1990–1999 texts in the five original genres (transcripts of television and radio programmes, fiction, magazines, newspapers and academic journals), from the full-text data at [corpusdata.org](https://www.corpusdata.org). The later television and film subtitle, blog and web genres were not used. About 3.8% of the base model's training text, a little under 1% from each genre, and its widest sample of how American English was spoken and written in the 1990s.
- **Institutional Books provided by the Institutional Data Initiative with source material contributed by Harvard Library, available at https://institutional.org/institutional-books.** About 9.6% of the base model's training text, and more than half of its books.
- **British National Corpus:** [Oxford's BNC project](https://www.natcorp.ox.ac.uk/), used under the applicable BNC User Licence.
- **UN General Debate Corpus:** Jankin, Baturo and Dasandi; [data](https://doi.org/10.7910/DVN/0TJX8Y). Selected speeches cover 1946–1999.
- **UN Security Council records:** Sakamoto and Matsuoka. Selected records cover 1946–1999; see the [UN Digital Library](https://digitallibrary.un.org/).
- **Encyclopedias from 1999:** selected text; source text is not distributed.
- **Usenet:** period discussions; posts remain the copyright of their authors.
- **National Library Singapore Digitised Newspapers:** headlines and opening lines of articles from old Singapore titles, from the [collection on data.gov.sg](https://data.gov.sg/collections/1478/view).
- Other historical collections include Project Gutenberg, American Stories, Hansard, Oireachtas, US government publications, PubMed, PubMed Central, arXiv, NASA, USGS, patent text, Britannica and Singapore and Malaya collections, as grouped in the README.

## Chat and evaluation materials

Licence labels below were checked on the linked project pages on 22 November 2026. They describe those resources, not the licence of Ping's weights.

| Resource | Role | Project's licence information |
|---|---|---|
| [nanochat](https://github.com/karpathy/nanochat) | Training framework and stock comparison | See upstream licence |
| [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | Writer of custom conversation lessons | Qwen Community Licence 1.0 |
| [Qwen3Guard-Stream-4B](https://huggingface.co/Qwen/Qwen3Guard-Stream-4B) | Hosted demo moderation | Apache 2.0 |
| [SmolTalk](https://huggingface.co/datasets/HuggingFaceTB/smoltalk) | Screened conversation examples | New component datasets Apache 2.0; pre-existing components retain their original licences |
| [MMLU](https://huggingface.co/datasets/cais/mmlu) | Multiple-choice exercises and evaluation | MIT |
| [GSM8K](https://huggingface.co/datasets/openai/gsm8k) | Maths exercises and evaluation | MIT |
| [ARC](https://huggingface.co/datasets/allenai/ai2_arc) | Multiple-choice exercises and evaluation | CC BY-SA 4.0 |

Claude assisted with implementation and evaluation, and no text it wrote was used to train Ping; Qwen wrote the custom training conversations. Visitors' demo chats are never used as training text.
