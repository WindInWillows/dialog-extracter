# -*- coding:utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

MODELDIR = 'C:\ltp-data-v3.3.1\ltp_data'
FILE_IN = 'data/rmdmy.txt'
from pyltp import *

DIALOG_FLAG = '：'

class LanguageModel:
    def __init__(self):
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
        self.cached = None

    def isSpeaker(self, sentence, name):
        if self.cached != sentence:
            self.cached = sentence
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

def explore(name):
    count = 0
    with open(FILE_IN) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            if name not in line:
                continue
            count += 1
    print count

def getDialogSentence(file):
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
    return text

def extracter(file, names):
    # lines = []
    # res = []
    # pres = []
    lm = LanguageModel()
    text = getDialogSentence(file)
    lan = {}
    for name in names:
        lan[name] = []
    print len(text)
    for sen in text:
        for name in names:
            if lm.isSpeaker(sen.split(DIALOG_FLAG)[0], name):
                lan[name].append(sen)
    return lan

    # with open(file, 'r') as fin:
    #     while True:
    #         line = fin.readline()
    #         if not line:
    #             break
    #         if name not in line or DIALOG_FLAG not in line:
    #             continue
    #         lst = line.split('%s' % DIALOG_FLAG)
    #         pre = SentenceSplitter.split(lst[0])[-1]
    #         dialog = lst[1]
    #         if name not in pre or not lm.isSpeaker(pre, name):
    #             continue
    #         lines.append(line)
    #         pres.append(pre)
    #         res.append(dialog)
    #
    # com = ['%s：%s' % pd for pd in zip(pres, res)]
    #
    # with open(file.split('.')[0] + '.com', 'w') as com_file:
    #     for l in com:
    #         com_file.write('%s' % l)
    # with open(file.split('.')[0] + '.phase', 'w') as phase_file:
    #     for l in lines:
    #         phase_file.write('%s' % l)
    # with open(file.split('.')[0] + '.pre', 'w') as pre_file:
    #     for l in pres:
    #         pre_file.write('%s\n' % l)
    # with open(file.split('.')[0] + '.dialog', 'w') as res_file:
    #     for l in res:
    #         res_file.write(l)
    # return res

if __name__ == '__main__':
    # lst = extracter(FILE_IN, '侯亮平')
    # print len(lst)
    # explore('钟小艾')
    # lst = getDialogSentence(FILE_IN)
    # for i in lst:
    #     print i

    lan = extracter(FILE_IN, ['侯亮平', '钟小艾'])
    print lan