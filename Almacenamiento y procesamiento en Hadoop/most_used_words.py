#!/usr/bin/python3

from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_PATTERN = re.compile(r"[\w']+")

class MRCommonWord(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.map_words,
                   combiner=self.combine_counts,
                   reducer=self.reduce_counts),
            MRStep(reducer=self.reduce_frequency)
        ]

    def map_words(self, _, line):
        for word in WORD_PATTERN.findall(line):
            yield (word.lower(), 1)

    def combine_counts(self, word, counts):
        yield (word, sum(counts))

    def reduce_counts(self, word, counts):
        yield None, (sum(counts), word)
        
    def reduce_frequency(self, _, word_counts):
        sorted_counts = sorted(word_counts, key=lambda x: x[0], reverse=True)
        yield None, list(sorted_counts[:10])

if __name__ == '__main__':
    MRCommonWord.run()
