#
# Extension to the Python Imaging Library: ImageDraw.textwrap
#
# Copyright (c) 2011 Szymon Jakubczak szym@szym.net
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 

import re
import ImageDraw

def _textwrap(self, xy, text, width, linespace=1.0, fill=None, font=None):
  """ Draw text at xy, wrapping it at width pixels.
      linespace is a multiplicative factor of font height determining line stretch.
  """
  
  # text up into word-wrappable chunks.  E.g.
  #   "Hello there -- you goof-ball, use the -b option!"
  # splits into
  #   Hello/ /there/ /--/ /you/ /goof-/ball,/ /use/ /the/ /-b/ /option!
  wordsep_re = re.compile(
  r'(\s+|'                                  # any whitespace
  r'[^\s\w]*\w+[^0-9\W]-(?=\w+[^0-9\W])|'   # hyphenated words
  r'(?<=[\w\!\"\'\&\.\,\?])-{2,}(?=\w))')   # em-dash
  # wordsep_re_uni = re.compile(self.wordsep_re.pattern, re.U)

  def just_whitespace(val):
    return not (val is None or len(val.strip()) == 0)

  chunks = wordsep_re.split(text)
  chunks = filter(just_whitespace, chunks)

  if font is None:
    font = self.getfont()
  
  def size(left, right):
    fragment = ' '.join(chunks[left:right])
    return font.getsize(fragment), fragment

  def search(left, right):
    # find break point so that the line fits the width
    (w, h), _ = size(left, right)
    if (w <= width):
      return right
    
    lo = left
    hi = right
    while lo + 1 < hi:
      md = (lo + hi) / 2
      (w, h), _ = size(left, md)
      if w > width:
        # too high
        hi = md
      elif w < width:
        # too low
        lo = md
      else:
        return md
    return lo

  left = 0
  right = len(chunks)
  (x,y) = xy
  
  while right > left:
    newbreak = search(left, right)
    if newbreak == left:
      # This sucks, we'll overflow the width.
      newbreak = left + 1
    (w, h), fragment = size(left, newbreak)
    left = newbreak
    self.text((x, y), fragment, fill=fill, font=font)
    y+= int(h * linespace)

# Install the new method.
ImageDraw.ImageDraw.textwrap = _textwrap
   
