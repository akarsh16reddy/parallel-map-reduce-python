import time
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

DATA_PATH = (
    Path(__file__).parent
    / "googlebooks-eng-all-1gram-20120701-a"
    / "googlebooks-eng-all-1gram-20120701-a"
)

# (asyncio) PS C:\Akarsh\workspace\python-asyncio> python -m multi_processing.6_7_google_n_gram_basic
# 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 86618505/86618505 [01:19<00:00, 1084959.65it/s]
# 80.6545

if __name__ == "__main__":
    freqs = defaultdict(int)

    with DATA_PATH.open(encoding="utf-8") as f:
        lines = f.readlines()

        start = time.time()

        for line in tqdm(lines):
            data = line.split("\t")
            word = data[0]
            count = int(data[2])
            freqs[word] += count

        end = time.time()
        print(f"{end - start:.4f}")
