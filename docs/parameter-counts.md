# Parameter counts used in the write-up and charts

The write-up and the charts give each model's parameters **without embedding lookup tables**: the tables a model reads by index (token and value embeddings), as opposed to the matrices it multiplies by. This is the count that tracks the computation a model does, and the one that makes Ping and stock nanochat comparable: they are the same 32-layer, 2,048-wide network.

| Model | Without lookup tables | Lookup tables | Total | Chart label |
|---|---:|---:|---:|---:|
| Ping, base and chat | 1,677,724,762 | 1,140,850,688 | 2,818,575,450 | 1.68B |
| Stock nanochat d32 | 1,744,830,464 | 134,217,728 | 1,879,048,192 | 1.74B |
| GPT-2 XL | 1,557,611,200 | shared with its output layer | 1,557,611,200 | 1.56B |
| GPT-2 Large | 774,030,080 | shared with its output layer | 774,030,080 | 774M |

**Ping.** The total comes from the release configuration; the checkpoint is identified in [the release manifest](release-checkpoint.json). Its lookup tables are the token embedding (32,768 × 2,048) and a value-embedding table of the same size on 16 of its 32 layers, which the version of nanochat it was trained with adds. The 1.68B figure is the 32 transformer blocks and the output layer.

**Stock nanochat d32.** The total is reported in [Karpathy's original d32 training run](https://github.com/karpathy/nanochat/discussions/8). Its one lookup table is the token embedding (65,536 × 2,048). The comparator is [karpathy/nanochat-d32](https://huggingface.co/karpathy/nanochat-d32), revision `016dba034c9c0ca9033ad1bc721bceff54680600`, step 650. Its published CORE figure is for the author's base; the locally evaluated model is the chat checkpoint.

**GPT-2.** Totals are calculated from the [Large configuration](https://huggingface.co/openai-community/gpt2-large/blob/main/config.json), [XL configuration](https://huggingface.co/openai-community/gpt2-xl/blob/main/config.json) and [OpenAI's implementation](https://github.com/openai/gpt-2/blob/master/src/model.py). GPT-2's token table is also its output layer, so it is counted once and stays in the figure; its small position table (1.3M and 1.6M) is included too.

Parameter count is not a control for architecture, training text, compute or post-training. Those differ between the models.
