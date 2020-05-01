import os
import sys
import glob
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["figure.figsize"] = (5.5, 4.25)
plt.rcParams["font.size"] = 9


def graph(article_dir, save_path, title=""):
    splits = glob.glob(os.path.join(article_dir, "*.txt"))
    for idx, split in tqdm(enumerate(splits), desc="Loading Splits", total=len(splits)):
        split_name = os.path.splitext(os.path.basename(split))[0]
        title_split = title + "-" + split_name

        num_article_sents = []
        num_abstract_sents = []

        with open(split, "r") as articles_info:
            for line in tqdm(articles_info, desc="Counting Sentences"):
                line = json.loads(line)
                current_num_article_sents = len(line["article_text"])
                current_num_abstract_sents = len(line["abstract_text"])
                num_article_sents.append(current_num_article_sents)
                num_abstract_sents.append(current_num_abstract_sents)

        avg_num_article_sents = sum(num_article_sents) / len(num_article_sents)
        avg_num_abstract_sents = sum(num_abstract_sents) / len(num_abstract_sents)
        print(
            title_split
            + "> Average Number of Sentences per Article: "
            + str(round(avg_num_article_sents, 2))
        )
        print(
            title_split
            + "> Average Number of Sentences per Abstract: "
            + str(round(avg_num_abstract_sents, 2))
        )

        sns.distplot(num_article_sents, kde=False)
        plt.title(title_split + " / Article Sentence Distribution")
        plt.xlabel("Sentence Count")
        plt.ylabel("Number of Articles")
        plt.savefig(os.path.join(save_path, title_split + "-article_sents.png",))
        plt.clf()

        sns.distplot(num_abstract_sents, kde=False)
        plt.title(title_split + " / Abstract Sentence Distribution")
        plt.xlabel("Sentence Count")
        plt.ylabel("Number of Abstracts")
        plt.savefig(os.path.join(save_path, title_split + "-abstract_sents.png",))
        plt.clf()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python graphs.py <arxiv_articles_dir> <pubmed_articles_dir>")
        sys.exit()
    arxiv_articles_dir = sys.argv[1]
    pubmed_articles_dir = sys.argv[2]

    # The path where the graphs are to be saved
    path = "graphs"
    if not os.path.exists(path):
        os.makedirs(path)

    graph(arxiv_articles_dir, path, title="arXiv")
    graph(pubmed_articles_dir, path, title="PubMed")
