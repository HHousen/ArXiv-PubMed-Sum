# ArXiv-PubMed-Sum

[process.py](process.py) is a script to process the [ArXiv-PubMed dataset](https://github.com/armancohan/long-summarization). **ArXiv and PubMed** (Cohan et al., 2018) are two long document datasets of scientific publications
from [arXiv.org](http://arxiv.org/) (113k) and PubMed (215k). The task is to generate the abstract from the paper body. 

The script processes the data into 6 files based on dataset splits. For each of the dataset split files (`train.txt`, `val.txt` and `test.txt`), the articles are read from the arxiv and pubmed sections and written to text files `train.source`, `train.target`, `val.source`, `val.target`, and `test.source` and `test.target`. These will be placed in the newly created `arxiv-pubmed` directory.

The output can be used for [HHousen/TransformerExtSum](https://github.com/HHousen/TransformerExtSum) to perform extractive summarization.

Steps:

1. Download the data from [armancohan/long-summarization](https://github.com/armancohan/long-summarization) or with the following direct links: [PubMed](https://bit.ly/2VsKNvt) ([mirror](https://bit.ly/2VLPJuh)) and [ArXiv](https://bit.ly/2wWeVpp) ([mirror](https://bit.ly/2VPWnzs)).
2. Run the command `python process.py <arxiv_articles_dir> <pubmed_articles_dir>` (runtime: 5-10m).

Commands:

```
pip install gdown
gdown https://drive.google.com/uc?id=1lvsqvsFi3W-pE1SqNZI0s8NR9rC1tsja
gdown https://drive.google.com/uc?id=1b3rmCSIoh6VhD4HKWjI4HOW-cSwcwbeC
unzip pubmed-dataset.zip
unzip arxiv-dataset.zip
python process.py arxiv-dataset/ pubmed-dataset/
```