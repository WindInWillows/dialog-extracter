# 小说人物对话抽取

## 任务：
给定一篇小说，从中抽取一些给定人物所说的话，并尽可能优化准确率（是该人物说的，并且都是语言）与召回率（能提取出的人物语言在该人物实际在小说中所说的话中所占的比例）

## 工具：
python 2.7

HIT-SCIR: pyltp


## 解决方法：
1. 第一步：首先要断句，使用pyltp的SentenceSplitter即可完成断句的工作，然后根据对话标志（本篇小说是‘：’）将上一个人说的话连起来，这里可能会将剧情连上，但是为了保证足够的召回率，也只能牺牲一点准确率。
2. 第二部：根据pyltp的语言角色标注工具判断出谁是说话者，大部分情况下会是话语前句的主语。小说结构比较好的话就能保证准确率。