For the words I downloaded a list (original.txt) of 'frequent' used nouns from:
- https://www.desiquintans.com/nounlist

To further process it.
- All barrelled compound nouns are put in a filter list delta_compound.txt.
- Using aspell (aspell -d en_GB-ise) another filter list is created.
  - Some false positives have been removed.
- A Combined filter list is created and some words have been manually added.

The filter is used to remove the words from original.txt and put the remaining
in nouns.txt .