from collections import Counter

class Indexer:
    def process(self,text):
        text = self.normalizetext(text)
        words = self.splittext(text)
        words = self.removestop_words(words) 
        stemmed_words = self.stemwords(words)
        return self._frequency(stemmed_words)

    def normalizetext(self,text):
        return text.lower().strip()
    
    def splittext(self,text):
        return text.split()
    
    def removestop_words(self,words):
        raise NotImplementedError 
    
    def stemwords(self,words):
        raise NotImplementedError
    
    def _frequency(self,words):
        return Counter(words)


class BasicIndexer(Indexer):
    _stop_words = {'he','she','is','and','or','the'}
    def removestop_words(self, words):
        return (
            word for word in words
            if word not in self._stop_words
        )
    
    def stemwords(self, words):
        return (
            (len(word)>3 and word.rstrip('aeiouy') or word
        )for word in words
        )
    
if __name__ =='__main__':
    indexer = BasicIndexer()
    indexer.process("Just like Johnny Flynn said\nThe breath I've taken and the one I must to go on")

