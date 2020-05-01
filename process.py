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
        "test": {"source": [], "target": []},
    }
    splits = glob.glob(os.path.join(article_dir, "*.txt"))
    for split in tqdm(splits, desc="Loading Splits"):
        num_articles_skipped = 0

        with open(split, "r") as articles_info:
            # count the number of lines in the file
            try:
                print(
                    "Counting the number of lines for data integrity and accurate progress bar. Press CTRL+C to cancel line counting (not recommended)."
                )
                t0 = time()
                num_articles = sum(1 for line in articles_info)
                # reset pointer to the beginning of the file
                print("done in " + str(time() - t0))
            except KeyboardInterrupt:
                num_articles = None
                print("Skipping line counting...")
            articles_info.seek(0)

            for idx, article_info in enumerate(
                tqdm(articles_info, desc="Loading Articles", total=num_articles)
            ):
                article_info = json.loads(article_info)
                abstract_sents = article_info["abstract_text"]
                article_sents = article_info["article_text"]

                # must have at least three sentences in the article
                # there are some articles that have one sentence (probably an error during data collection)
                if len(article_sents) <= 3:
                    num_articles_skipped += 1
                    continue  # move to next article

                # must have at least two sentences in the abstract
                if len(abstract_sents) <= 2:
                    num_articles_skipped += 1
                    continue  # move to next article

                # remove the <S> and </S> tokens
                abstract_sents = [x[4:-4] for x in abstract_sents]

                # convert from lists of sentences to strings
                abstract_str = " ".join(abstract_sents).strip()
                article_str = " ".join(article_sents).strip()

                # remove newlines (pubmed dataset has newlines while arxiv probably does not)
                # each document is sentence-tokenized
                abstract = abstract_str.replace("\n", "")
                article = article_str.replace("\n", "")

                if "\n" in abstract or "\n" in article:
                    logger.warn(
                        "A newline character was found at index "
                        + str(idx)
                        + " in "
                        + str(split)
                        + ". Logging abstract and article. This indicates a problem in the data or this processing code."
                    )
                    logger.debug("Abstract: " + str(abstract_sents))
                    logger.debug("Article: " + str(article_sents))

                split_name = os.path.splitext(os.path.basename(split))[0]

                dataset[split_name]["source"].append(article)
                dataset[split_name]["target"].append(abstract)

            # if the number of articles were counted then make sure it equals the number of processed articles
            if num_articles:
                assert (
                    num_articles
                    == len(dataset[split_name]["source"]) + num_articles_skipped
                    == len(dataset[split_name]["target"]) + num_articles_skipped
                ), (
                    "The number of processed articles does not equal the number of input articles. num_articles is "
                    + str(num_articles)
                    + ", number of sources is "
                    + str(len(dataset[split_name]["source"]))
                    + ", and number of targets is "
                    + str(len(dataset[split_name]["target"]))
                )

    for split_name, current_split in tqdm(dataset.items(), desc="Split"):
        for source_or_target, data in current_split.items():
            with open(
                os.path.join(save_path, split_name + "." + source_or_target), "a"
            ) as f:
                for item in tqdm(
                    data, desc="Writing " + source_or_target + " Documents"
                ):
                    f.write("%s\n" % item)
                gc.collect()
    del dataset
    gc.collect()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python process.py <arxiv_articles_dir> <pubmed_articles_dir>")
        sys.exit()
    arxiv_articles_dir = sys.argv[1]
    pubmed_articles_dir = sys.argv[2]

    # The path where the articles are to be saved
    path = "arxiv-pubmed"
    if not os.path.exists(path):
        os.makedirs(path)

    write_to_bin(arxiv_articles_dir, path)
    write_to_bin(pubmed_articles_dir, path)
