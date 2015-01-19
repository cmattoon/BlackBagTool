from math import sqrt
from collections import Counter


def cosine_similarity(list_A, list_B):
    """Calculates cosine similiarity between two lists.
    Lists are treated as sets, so duplicates don't count.
    """
    ctrA = Counter(list_A)
    ctrB = Counter(list_B)
    terms = set(ctrA).union(ctrB)
    dotprod = sum(ctrA.get(k, 0) * ctrB.get(k, 0) for k in terms)
    magA = sqrt(sum(ctrA.get(k, 0)**2 for k in terms))
    magB = sqrt(sum(ctrB.get(k, 0)**2 for k in terms))
    return dotprod / float(magA * magB)

    
