import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


def read_tsv_file(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df


def count_quotes_by_author(df, author_name):
    quote_count = df[df['Author'] == author_name].shape[0]
    return quote_count


def find_longest_quote_author(df):
    df['Quote_Word_Count'] = df['Quote'].apply(lambda x: len(str(x).split()))
    index_of_longest_quote = df['Quote_Word_Count'].idxmax()
    author_with_longest_quote = df.loc[index_of_longest_quote, 'Author']
    longest_quote = df.loc[index_of_longest_quote, 'Quote']
    return author_with_longest_quote, longest_quote


def find_authors_with_word_in_quote(df, word):
    df_with_word = df[df['Quote'].str.contains(fr'\b{word}\b', case=False, na=False)]
    authors_with_word = df_with_word['Author'].unique()
    return authors_with_word


def analyze_word_frequencies(df, top_n=10, bottom_n=10):
    quotes = df['Quote']
    words = []

    for quote in quotes:
        tokens = word_tokenize(quote)
        words.extend(tokens)

    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    word_counts = Counter(words)

    most_common_words = word_counts.most_common(top_n)
    least_common_words = word_counts.most_common()[-bottom_n:]

    return most_common_words, least_common_words


if __name__ == "__main__":
    file_path = 'quotes.tsv'
    df = read_tsv_file(file_path)

    # Task 1: Count quotes by a specific author
    author_name = 'Alexandre Dumas'
    quote_count = count_quotes_by_author(df, author_name)
    print(f"Number of quotes from '{author_name}': {quote_count}")

    # Task 2: Find the author with the longest quote
    author_with_longest_quote, longest_quote = find_longest_quote_author(df)
    print(f"Author with the longest quote is '{author_with_longest_quote}' with {len(longest_quote.split())} words.")
    print("Longest Quote:")
    print(longest_quote)

    # Task 3: Find authors with a specific word in their quotes
    word_to_search = 'one'
    authors_with_word = find_authors_with_word_in_quote(df, word_to_search)
    print(f"Author(s) with a quote containing the word '{word_to_search}': {', '.join(authors_with_word)}")

    # Task 4: Analyze word frequencies
    top_n = 10  # Number of top words to find
    bottom_n = 10  # Number of bottom words to find
    most_common_words, least_common_words = analyze_word_frequencies(df, top_n, bottom_n)

    print("Most frequent words:")
    for word, count in most_common_words:
        print(f"{word}: {count}")

    print("\nLeast frequent words:")
    for word, count in least_common_words:
        print(f"{word}: {count}")
