from chunkit import Chunker
from newspaper import Article


def news_paper_extraction(url):
    article = Article(url)
    article.download()
    article.parse()

    return article.text


def url_to_chunks(url):
    try:
        print("------in-newspaper")
        url_content = news_paper_extraction(url)
    except:
        print("-----in-chunker")
        chunker = Chunker()
        chunk_urls = chunker.process(url)

        url_content = ""
        for url in chunk_urls:
            if url["success"]:
                for chunk in url["chunks"]:
                    url_content += chunk

    return url_content


if __name__ == "__main__":
    urls = [
        "https://www.financialexpress.com/market/ms-dhonis-bad-luck-in-equity-after-gensol-engineering-sebi-clampdown-3812256/"
    ]
    for url in urls:
        print(url_to_chunks(url))
