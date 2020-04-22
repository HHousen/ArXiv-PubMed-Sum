import os
import sys
import gc
import glob
import json
from time import time
from tqdm import tqdm

def write_to_bin(article_dir, save_path):
    dataset = {
        "train": {"source": [], "target": []},
        "val": {"source": [], "target": []},
        "test": {"source": [], "target": []}
    }
    splits = glob.glob(os.path.join(article_dir, "*.txt"))
    for split in tqdm(splits, desc="Loading Splits"):
        with open(split, "r") as articles_info:
            # count the number of lines in the file
            try:
                print("Counting the number of lines for accurate progress bar. Press CTRL+C to cancel line counting.")
                t0 = time()
                num_articles = sum(1 for line in articles_info)
                # reset pointer to the beginning of the file
                print("done in " + str(time() - t0))
            except KeyboardInterrupt:
                num_articles = None
                print("Skipping line counting...")
            articles_info.seek(0)

            for article_info in tqdm(articles_info, desc="Loading Articles", total=num_articles):
                article_info = json.loads(article_info)
                abstract_sents = article_info["abstract_text"]
                article_sents = article_info["article_text"]

                # convert from lists of sentences to strings
                abstract = " ".join(abstract_sents).strip()
                article = " ".join(article_sents).strip()

                split_name = os.path.splitext(os.path.basename(split))[0]

                dataset[split_name]["source"].append(article)
                dataset[split_name]["target"].append(abstract)

    for split_name, current_split in tqdm(dataset.items(), desc="Split"):
        for source_or_target, data in current_split.items():
            with open(os.path.join(save_path, split_name+"."+source_or_target), 'a') as f:
                for item in tqdm(data, desc="Writing " + source_or_target + " Documents"):
                    f.write("%s\n" % item)
                gc.collect()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python process.py <arxiv_articles_dir> <pubmed_articles_dir>")
        sys.exit()
    arxiv_articles_dir = sys.argv[1]
    pubmed_articles_dir = sys.argv[2]

    # The path where the articles are to be saved
    path = "arxiv-pubmed"
    if not os.path.exists(path): os.makedirs(path)

    write_to_bin(arxiv_articles_dir, path)
    write_to_bin(pubmed_articles_dir, path)