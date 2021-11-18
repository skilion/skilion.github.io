---
title: "Santa Ski"
date: 2015-11-15
lastmod: 2021-11-07
resources:
- name: header
  src: images/header.png
tags:
  - portfolio
---

This game was made in 48h, for a local [game jam](https://en.wikipedia.org/wiki/Game_jam) that I organised with friends when I still was in University (good times).

This game is a remake of a Microsoft classic: [SkiFree](https://en.wikipedia.org/wiki/SkiFree). The protagonist is supposed to be Santa Claus, in case you were wondering.

{{< video "videos/gameplay.mp4" >}}

I consider game jams great experiences for learning to be efficient programmers. Given the short time available one can not waste time on technicalities such as which language to use, which IDE, which framework, etc. You barely have the time to build the core features of whatever idea you come up with.

So for this project I decided to use C++ as I knew it has many good multimedia framework which provide graphics and input access with minimum code required. I ended up using [SFML](https://en.wikipedia.org/wiki/Simple_and_Fast_Multimedia_Library).

I have drawn all the game art, and I am really happy how it has given the game a consistent look&feel, as opposed to downloading a bunch of random images from the internet and mixing them together. I am not claiming it looks professional but at least it doesn't look like Frankenstein's monster.

Overall I am quite satisfied how productive this project has been compared to other ones where I decided to reinvent the wheel by building my own graphic framework from scratch. It is a testament to how building on top of well-established libraries saves time.

The source code is available on [GitHub](https://github.com/skilion/santa-ski) and it can be readily compiled on Linux.