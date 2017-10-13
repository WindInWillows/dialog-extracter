# -*- coding:utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

MODELDIR = 'C:\ltp-data-v3.3.1\ltp_data'
FILE_IN = 'data/in/rmdmy.txt'
FILE_OUT = 'data/out/rmdmy.out'
from pyltp import *

# 话语开始标志
DIALOG_FLAG = '：'

# 封装语言模型可大大减少判断说话者的耗时
class LanguageModel:
    def __init__(self):
        print '开始载入语言模型...'
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(MODELDIR, "cws.model"))
        self.postagger = Postagger()
        self.postagger.load(os.path.join(MODELDIR, "pos.model"))
        self.parser = Parser()
        self.parser.load(os.path.join(MODELDIR, "parser.model"))
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(MODELDIR, "ner.model"))
        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(MODELDIR, "srl"))
        self.cache = None
        print '语言模型载入成功'

    def isSpeaker(self, sentence, name):
        if self.cache != sentence:
            self.cache = sentence
            self.words = self.segmentor.segment(sentence)
            self.postags = self.postagger.postag(self.words)
            self.arcs = self.parser.parse(self.words, self.postags)
            self.netags = self.recognizer.recognize(self.words, self.postags)
            self.roles = self.labeller.label(self.words, self.postags, self.netags, self.arcs)

        for role in self.roles:
            for arg in role.arguments:
                if arg.name == 'A0' and self.words[arg.range.start] == name:
                    return True
        return False

# 提取有对话的句子并连接
def getDialogSentence(file):
    print '开始抽取有对话的句子...'
    text = []
    with open(file) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            lst = SentenceSplitter.split(line)

            pre = ''
            for l in lst:
                if DIALOG_FLAG not in l:
                    pre += l
                else:
                    if DIALOG_FLAG in pre:
                        text.append(pre)
                    pre = l
            if DIALOG_FLAG in pre:
                text.append(pre)
    print '抽取句子完成'
    return text

# 抽取人物对话
def extracter(file, names):
    lm = LanguageModel()
    text = getDialogSentence(file)
    lan = {}
    print '开始抽取人物对话...'
    for name in names:
        lan[name] = []
    for sen in text:
        for name in names:
            if lm.isSpeaker(sen.split(DIALOG_FLAG)[0], name):
                lan[name].append(sen)
    print '抽取人物对话成功'
    return lan

def storeResultMap(resMap, file):
    print '正在存储文件...'
    with open(file, 'w') as fout:
        for key in resMap:
            fout.write('\n%s:%i\n' % (key, len(resMap[key])))
            for sen in resMap[key]:
                fout.write('%s\n'%sen)
    print '存储文件成功'


def showResultMap(resMap):
    for key in resMap:
        print '\n%s:\n%i' % (key, len(resMap[key]))
        for sen in resMap[key]:
            print sen

if __name__ == '__main__':
    resMap = extracter(FILE_IN, ['侯亮平', '钟小艾', '祁同伟', '李达康', '沙瑞金', '陈海','陈岩石', '易学习', '赵德汉', '高小琴', '陆亦可', '赵东来'])
    storeResultMap(resMap, FILE_OUT)