# 正则包
import re
# 自然语言处理包
import jieba
import jieba.analyse
import os.path
# html 包
import html
# 数据集处理包
from datasketch import MinHash

class MinHashSimilarity(object):
    """
    MinHash
    """
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  
        # 提取关键词
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    def main(self):
        # 去除停用词
        jieba.analyse.set_stop_words('stopwords.txt')
        # MinHash计算
        m1, m2 = MinHash(), MinHash()
        # 提取关键词
        s1 = self.extract_keyword(self.s1)
        s2 = self.extract_keyword(self.s2)

        for data in s1:
            m1.update(data.encode('utf8'))
        for data in s2:
            m2.update(data.encode('utf8'))
        return m1.jaccard(m2)

# 测试
if __name__ == '__main__':
    file1 = input("输入原文件：")
    file2 = input("输入要查重的文件：")
    with open(file1, 'r',encoding='utf-8') as x, open(file2, 'r',encoding='utf-8') as y:
        content_x = x.read()
        content_y = y.read()
        similarity = MinHashSimilarity(content_x, content_y)
        similarity = similarity.main()
        results = '('+file1+')'+ ' 跟 (' + file2 +') 相似度: %.2f%%' % (similarity*100)+'\n'
        file3 = open("result.txt","a",encoding='utf-8')
        file3.write(results)
        file3.close()
        path3 = os.path.abspath('result.txt')
        print("结果路径为："+path3)
