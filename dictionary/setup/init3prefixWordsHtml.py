#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import shutil
import urllib
from variables import getDictWordsJsonDir
from variables import getPrefixWordsHtmlDir


if __name__ == '__main__':
  prefixWords = {}

  for dirpath, dirnames, filenames in os.walk(getDictWordsJsonDir()):
    for filename in filenames:
      word = filename.decode('utf-8')

      if word[0] in prefixWords:
        prefixWords[word[0]].append(word)
      else:
        prefixWords[word[0]] = [word]

  if os.path.exists(getPrefixWordsHtmlDir()):
    shutil.rmtree(getPrefixWordsHtmlDir())
    os.makedirs(getPrefixWordsHtmlDir())
  else:
    os.makedirs(getPrefixWordsHtmlDir())

  for firstLetter in prefixWords:
    legalNameOnGAE = urllib.quote(
                       ('%s.html' % firstLetter).encode('utf-8')
                     ).replace('%', 'Z')
    path = os.path.join(getPrefixWordsHtmlDir(), legalNameOnGAE)
    print(path)
    print('%s: %d' % (firstLetter, len(prefixWords[firstLetter])))
    with open(path, 'w') as f:
      for word in prefixWords[firstLetter]:
        string = u'<a href="%s/%s">%s</a>' % (firstLetter, word, word)
        f.write(string.encode('utf-8'))
