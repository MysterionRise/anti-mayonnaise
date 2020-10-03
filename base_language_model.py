# Before starting the task please read thoroughly these chapters of Speech and Language Processing by Daniel Jurafsky & James H. Martin:
#
# • N-gram language models: https://web.stanford.edu/~jurafsky/slp3/3.pdf
#
# • Neural language models: https://web.stanford.edu/~jurafsky/slp3/7.pdf
#
# In this task you will be asked to implement the models described there.
#
# Build a text generator based on n-gram language model and neural language model.
#
# Find a corpus (e.g. http://cs.stanford.edu/people/karpathy/char-rnn/shakespeare_input.txt ), but you are free to use anything else of your interest
# Preprocess it if necessary (we suggest using nltk for that)
# Build an n-gram model
# Try out different values of n, calculate perplexity on a held-out set
# Build a simple neural network model for text generation (start from a feed-forward net for example). We suggest using tensorflow + keras for this task
# Criteria:
#
# Data is split into train / validation / test, motivation for the split method is given
# N-gram model is implemented a. Unknown words are handled b. Add-k Smoothing is implemented
# Neural network for text generation is implemented
# Perplexity is calculated for both models
# Examples of texts generated with different models are present and compared
# Optional: Try both character-based and word-based approaches.
from typing import List


class BaseLM:

    def __init__(self, n: int, vocab: List = None):
        """Language model constructor
        n -- n-gram size
        vocab -- optional fixed vocabulary for the model
        """
        self.n = n
        self.vocab = vocab
        self.ngrams = {}

    def prob(self, word: str, context=None):
        """This method returns probability of a word with given context: P(w_t | w_{t - 1}...w_{t - n + 1})

        For example:
        >>> lm.prob('hello', context=('world',))
        0.99988
        """
        context_stats = self.ngrams.get(' '.join(context), {})
        total = len(context_stats)
        print(context_stats)
        print(word)
        count = context_stats.get(word, 0)
        return count / total

    def generate_text(self, text_length: int):
        """This method generates random text of length

        For example
        >>> lm.generate_text(2)
        hello world

        """
        raise NotImplementedError

    def update(self, sequence_of_tokens: List[str]):
        """This method learns probabiities based on given sequence of tokens

        sequence_of_tokens -- iterable of tokens

        For example
        >>> lm.update(['hello', 'world'])
        """
        for i in range(len(sequence_of_tokens) - self.n):
            seq = ' '.join(sequence_of_tokens[i:i + self.n])
            # print(seq)
            if seq not in self.ngrams.keys():
                self.ngrams[seq] = {}
            token = sequence_of_tokens[i + self.n]
            self.ngrams[seq][token] = self.ngrams[seq].get(token, 0) + 1

    def perplexity(self, sequence_of_tokens: List[str]):
        """This method returns perplexity for a given sequence of tokens

        sequence_of_tokens -- iterable of tokens
        """
        mul = 1.0
        sequence_of_tokens.append('</s>')
        for i in range(0, len(sequence_of_tokens) - self.n):
            selected = sequence_of_tokens[i:i + self.n + 1]
            mul = mul * (1.0 / self.prob(selected[self.n], context=selected[:self.n]))
            print()
        return mul