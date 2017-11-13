来宝：开源人工智能
=================

[![Build Status](https://travis-ci.org/jjwang/laibot.svg?branch=master)](https://travis-ci.org/jjwang/laibot)

## 这码农咋想的？

来宝项目的由来是因为2018年智能音箱太火了！当我在看基于淘宝可购买的硬件电路板以及免费语音服务如何构建智能音箱时，我找到了[japser-client](http://https://github.com/jasperproject/jasper-client)和[dingdang-robot](https://github.com/wzpan/dingdang-robot)这两个项目。Jasper完成了一个大概的框架，但是没有集成对应的汉语服务；Dingdang基于Jasper继续演进。不得不说，Dingdang开发的确实非常好，集成了很多的服务、编写了大量的文档，使得一个新手很容易入门。

但是，Dingdang并不是我想要的。就智能音箱这个方向来说，众多巨头涌入的是一个2亿的小市场，小市场的由来是因为用户接受度不高（画外音：什么？天猫双十一卖了一百万台？OMG，我可什么都没说）。归根结底，就是现在的汉语普通话智能音箱方案用户体验不佳，说是智能、经常情况下是智障。如果方案在用户体验上没有任何优势，集成了再多的服务实际上用处并不大。

说了这么多，那么来宝想干嘛？其实很简单，来宝就是想试一下基于当前可用的开源软硬件和免费语音服务，能打造的语音助理最好能到什么样子？Jasper和Dingdang从优化的角度来说还做的不够，这些是来宝所想做的。

好吧，这就是来宝的由来！能做到什么程度，说实在的，我也不知道，走走看吧！

## 项目的规矩

- 确保通过单元测试。

        python -m unittest discover
- Python 代码需符合 PEP 8 编程规范，检查工具使用 flake8。

