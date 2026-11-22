"""Chat with Ping as its demo serves it: nanochat's own engine, Ping's first line after <|bos|>, the demo's sampling.

Run it from a checkout of https://github.com/karpathy/nanochat at commit 92d63d4, with NANOCHAT_BASE_DIR set to this folder,
which is laid out as nanochat expects (chatsft_checkpoints/ping/ and tokenizer/):

    git clone https://github.com/karpathy/nanochat && cd nanochat && git checkout 92d63d4 && uv sync --extra gpu
    export NANOCHAT_BASE_DIR=/path/to/this/folder
    uv run python $NANOCHAT_BASE_DIR/ping_chat.py                              # a conversation
    uv run python $NANOCHAT_BASE_DIR/ping_chat.py -p "What's the date today?"  # one reply
    uv run python $NANOCHAT_BASE_DIR/ping_chat.py --check                      # the files' sha256 and three fixed prompts, greedy

nanochat's own `python -m scripts.chat_cli -g ping` also loads these weights; it leaves out Ping's first line, which
every lesson Ping learned from began with, so Ping is less itself there.

The weights alone carry no moderation filter, no calculator note and no spell-check hint: the demo page adds those.
Ping is often wrong and agrees with what it is told. See the model card.
"""
import argparse
import hashlib
import os
import sys

sys.path.insert(0, os.getcwd())         # run from the nanochat checkout: python puts this file's folder on the path, not the checkout
try:
    from nanochat.checkpoint_manager import load_model
    from nanochat.common import autodetect_device_type, compute_init, get_base_dir
    from nanochat.engine import Engine
except ModuleNotFoundError as e:
    if e.name != "nanochat":
        raise
    sys.exit("ping_chat.py: no nanochat here. Run it from a checkout of https://github.com/karpathy/nanochat at commit 92d63d4 "
             "(cd nanochat first; see the top of this file).")

TAG, STEP = "ping", 559
PREAMBLE = "[1999-12-31] Ping"          # the line after <|bos|> in every lesson and in the demo
WINDOW, MAX_TOKENS = 3500, 320          # the demo's: the tokens Ping sees with its reply, and a reply's cap
SHA256 = {"chatsft_checkpoints/ping/model_000559.pt": "3a463f98b9544f009558219a052567800f52c9167e6ff7b993710416d8f016d3",
          "chatsft_checkpoints/ping/meta_000559.json": "4ed8c86ac51e0538b5c6d50c4846467fce6de976650b4cfddc8d739c319c9833"}
CHECK = ["What's the date today?", "Who are you?", "What is the capital of France?"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


class Ping:
    def __init__(self, device_type=""):
        device_type = device_type or autodetect_device_type()
        _, _, _, _, device = compute_init(device_type)
        model, self.tok, self.meta = load_model("sft", device, phase="eval", model_tag=TAG, step=STEP)
        self.engine = Engine(model, self.tok)
        t = self.tok
        self.bos = t.get_bos_token_id()
        self.user_start, self.user_end = t.encode_special("<|user_start|>"), t.encode_special("<|user_end|>")
        self.assistant_start, self.assistant_end = t.encode_special("<|assistant_start|>"), t.encode_special("<|assistant_end|>")
        self.head = [self.bos, *t.encode(PREAMBLE + "\n")]

    def prompt(self, history, user, max_tokens):
        """The newest whole turns that fit the window with the reply, after Ping's first line."""
        last = [self.user_start, *self.tok.encode(user), self.user_end, self.assistant_start]
        budget = WINDOW - max_tokens - len(self.head) - len(last)
        kept = []
        for u, r in reversed(history):
            turn = [self.user_start, *u, self.user_end, self.assistant_start, *r, self.assistant_end]
            if len(turn) > budget:
                break
            kept.insert(0, turn)
            budget -= len(turn)
        return self.head + [x for turn in kept for x in turn] + last

    def reply(self, history, user, temperature=0.6, top_k=50, max_tokens=MAX_TOKENS, seed=0):
        tokens = self.prompt(history, user, max_tokens)
        rows, _ = self.engine.generate_batch(tokens, num_samples=1, max_tokens=max_tokens, temperature=temperature,
                                             top_k=top_k, seed=seed)
        out = rows[0][len(tokens):]
        history.append((self.tok.encode(user), out))
        return self.tok.decode(out).replace("<|assistant_end|>", "").strip()


def main():
    ap = argparse.ArgumentParser(description="Chat with Ping")
    ap.add_argument("-p", "--prompt", default="", help="one message, one reply")
    ap.add_argument("-t", "--temperature", type=float, default=0.6)
    ap.add_argument("-k", "--top-k", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device-type", default="", choices=["", "cuda", "cpu", "mps"])
    ap.add_argument("--check", action="store_true", help="the files' sha256, then three fixed prompts decoded greedily")
    args = ap.parse_args()
    if args.check:
        base, bad = get_base_dir(), 0
        for rel, want in SHA256.items():
            got = sha256(os.path.join(base, rel))
            print(("ok       " if got == want else "DIFFERENT") + f" {rel} {got}")
            bad += got != want
        if bad:
            sys.exit("the files are not the release's")
    ping = Ping(args.device_type)
    if args.check:
        print(f"loaded: step {ping.meta.get('step')}, {ping.meta['model_config']}")
        for i, q in enumerate(CHECK):
            print(f"CHECK {i + 1} | {q} | {ping.reply([], q, temperature=0.0, top_k=1, max_tokens=64, seed=i)}")
        return
    if args.prompt:
        print(ping.reply([], args.prompt, args.temperature, args.top_k, seed=args.seed))
        return
    print("It is 31 December 1999. Type a message; 'new' starts a fresh chat, 'quit' ends.")
    history, n = [], 0
    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in ("quit", "exit"):
            break
        if user.lower() == "new":
            history = []
            continue
        if user:
            n += 1
            print("Ping:", ping.reply(history, user, args.temperature, args.top_k, seed=args.seed + n))


if __name__ == "__main__":
    main()
