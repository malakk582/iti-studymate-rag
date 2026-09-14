# Dataset: Public-Domain Classic Literature

The project uses three real text documents downloaded from Project Gutenberg:

- [Alice's Adventures in Wonderland](https://www.gutenberg.org/ebooks/11)
- [Pride and Prejudice](https://www.gutenberg.org/ebooks/1342)
- [Frankenstein; or, the Modern Prometheus](https://www.gutenberg.org/ebooks/84)

The plain-text files are stored locally in `data/documents/`. Project Gutenberg identifies these US editions as public domain in the United States. Before redistributing the files in another jurisdiction, review the applicable local copyright rules and Project Gutenberg terms.

## Dataset inspection

The three files are text-extractable and contain approximately 25,000 lines and 1.3 MB in total. The ingestion code records the filename and chunk ID for every retrieved passage. Since these source files are plain text rather than PDFs, their page field is `null` and citations use filename plus chunk ID.

## Suggested evaluation questions

1. Who is Alice?
2. What happens when Alice follows the White Rabbit?
3. What is Elizabeth Bennet's first impression of Mr. Darcy?
4. Why does Mr. Darcy initially object to the relationship?
5. What motivates Victor Frankenstein's experiment?
6. How does the creature learn about human society?
7. What does the Queen of Hearts order during the trial?
8. Where does the Bennet family live?
9. What does the monster ask Victor to create?
10. What is RAG, and why does it help reduce hallucination?
