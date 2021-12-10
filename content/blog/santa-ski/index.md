---
title: "Santa Ski"
date: 2015-11-15
lastmod: 2021-12-10
resources:
- name: header
  src: images/header.png
---

This game was made in 48h, for a local [game jam](https://en.wikipedia.org/wiki/Game_jam) that I organised with friends when I still was in University (good times).

This game is a remake of a Microsoft classic: [SkiFree](https://en.wikipedia.org/wiki/SkiFree). The protagonist is supposed to be Santa Claus, in case you were wondering.

{{< video "videos/gameplay.mp4" >}}

I consider game jams great experiences for learning how to be pragmatical developers. Given the short time available one need to focus on implementing the features that matter and not the ones that could be solved by using a more complete media framework. Loading assets, audio and video access, are all problems that can be solved immediately by using a modern and mature framework and not something worth spending time on like I did for earlier game projects. You barely have the time to build the core features of whatever idea you come up with.

For this project I decided to use C++ with [SFML](https://en.wikipedia.org/wiki/Simple_and_Fast_Multimedia_Library) which provides access to graphics and input with very few lines of code.

I have drawn all the game art, and I am really happy how it has given the game a consistent look&feel, as opposed to downloading a bunch of random images from the internet and mixing them together.

Overall I am quite satisfied how productive this project has been compared to other ones where I decided to reinvent the wheel by building my own graphic framework from scratch. It is a testament to how building on top of well-established libraries saves time.

The source code is available on [GitHub](https://github.com/skilion/santa-ski) and it can be compiled on Linux.
