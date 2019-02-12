来宝人工智能：基于树莓派的语音对话机器人
=================

[![Build Status](https://travis-ci.org/jjwang/laibot-client.svg?branch=master)](https://travis-ci.org/jjwang/laibot-client) [![Python3](https://img.shields.io/badge/python-3-blue.svg
)](https://www.python.org)

![TJBot](http://115.28.128.30/tjbot.jpg)

如果你喜欢此项目，请给我打星。

## 1. 必读
- [演示视频](http://v.youku.com/v_show/id_XMzIzNDUyNjQ5Mg==.html?spm=a2h3j.8428770.3416059.1)
- [项目Wiki](https://github.com/jjwang/laibot-client/wiki)

## 2. 由来

来宝项目的由来是因为2017年智能音箱太火了！就智能音箱这个方向来说，众多巨头涌入的是一个2亿的小市场，小市场的由来是因为用户接受度不高（画外音：什么？天猫双十一卖了一百万台？OMG，我可什么都没说）。归根结底，就是现在的汉语普通话智能音箱方案用户体验不佳，说是智能、经常情况下是智障。如果方案在用户体验上没有任何优势，集成了再多的服务实际上用处并不大。

说了这么多，那么来宝想干嘛？其实很简单，来宝就是想试一下基于当前可用的开源软硬件和免费语音服务，能打造的语音助理最好能到什么样子？好吧，这就是来宝的由来！能做到什么程度，说实在的，我也不知道，走走看吧！来宝基于Jasper。

## 3. 规矩

- 确保通过单元测试。

        python3 -m unittest discover
- Python 代码需符合 PEP 8 编程规范，检查工具使用 flake8。

