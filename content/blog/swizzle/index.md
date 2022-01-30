---
title: "Swizzle"
date: 2013-01-27
lastmod: 2021-11-04
resources:
- name: header
  src: images/header.png
---

In 2013, all my friends were playing [Ruzzle](https://en.wikipedia.org/wiki/Ruzzle) on their smartphones. However I only had a [dumbphone](https://en.wiktionary.org/wiki/dumbphone) so I could not join in the fun.

I was fascinated by how addicting the game was, given its simplicity, and I started thinkering how I could replicate it.

{{< video "videos/gameplay.mp4" >}}

The game is written in [D](https://dlang.org/) because at the time I was looking to replace C++ for making games. The more I used C++ the more I found myself spending time avoiding bad patterns and the growing complexity of the language with each major release.

For this project I did not want to use any off the shelf multimedia framework because I wanted to challenge myself and going as low level as possible. So I ended up having to deal with a lot of interfaces in order to use C libraries such as OpenGL, FreeType, and libpng. It turned out to be a huge amount of work so I reduced the scope and only made it work for Windows and not Linux.

After spending much of my time making interfaces for the C libraries, the game logic to re-implement Ruzzle turned out to be a tiny work in comparison.

The game logic is all contained in one class: [WordTable](https://github.com/skilion/swizzle/blob/master/word_table.d). And the most interesting functions are two.

[WordTable.reset()](https://github.com/skilion/swizzle/blob/a2e788be864b15880b18407250bdb9009a3f5e95/word_table.d#L33). This function prepares the game board by placing the letters. It starts by taking a random word and placing its letters close to each other in the board. Then this process is repeated until there is no more space left. This algorithm ensures that any game has valid words to be discovered. A simpler approach, where letters are placed randomly in the board could lead to corner cases where no words are available in a game.

[WordTable.findPossibleWords()](https://github.com/skilion/swizzle/blob/a2e788be864b15880b18407250bdb9009a3f5e95/word_table.d#L128). This function finds all available words in the game board. It uses a recursive algorithm that tries to match each word in the word list by trying each neighbor letter at the current position.

{{< video "videos/end.mp4" >}}

The source code is available on [GitHub](https://github.com/skilion/swizzle) and it can be readily compiled on Windows using Visual D. Pre-compiled binaries are also available.