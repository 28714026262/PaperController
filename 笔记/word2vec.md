<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-10-27 20:47:46
 * @LastEditTime: 2022-11-28 11:36:38
 * @LastEditors: Suez_kip
 * @Description: 
-->
# word2vec

## 文本表示

1. Skip-gram模型：从大量非结构化文本数据中学习单词的高质量矢量表示；  
通过中心词来推断上下文一定窗口内的单词，对独热码生成嵌入词向量；  
![图 4](../images/f3214d61d6d1123f3319afb9a218658d18f5905b2033e46c010f38a538e4a26a.png)  
![图 6](../images/8e396dabd5689e8782b15700db2f7c8c249b622f26ac553153e5992f1570bb4b.png)  
其中模式中的许多可以表示为线性翻译：vec(“Madrid”) - vec(“Spain”) + vec(“France”) is closer to vec(“Paris”)  
相对词汇自然组合得出地含义更有意义如“波士顿”和“环球报”的组合含义；  

1. N-gram模型：进行大小为N的滑动窗口操作，形成了长度是N的字节片段gram序列。常用二元和三元gram模型；
N-gram模型是基于统计的概率预测，以二元模型为例：  
![图 2](../images/ddc201a22f9f543c600958c497d6753ce977266b21ff1e15a444968946e0806d.png)  
根据一个语料库中的参数统计分析，得到相应的概率：  
![图 3](../images/5c2f9e59ab18bd4f665f99464044b3102e1170414a279124d92d00caf59b6792.png)  
进一步可以求出一个相应的句子所对应的概率（通过链式法则），来研究这句句子在语料库中的存在概率；  

1. 递归自动编码器，受益于短语向量而非单词向量，单词->短语模型扩展更为简单；  
数据驱动获取大量短语，视之为单独标记

本文有基于skip-gram的扩展；对频繁单词进行二次采样->速度提高、稀有词汇准确性提高；
本文提出一种简化的噪声对比估计（NCE）变体，训练skip-gram，相对分层softmax更快更好地表示；
本文提出了一组包含单词和短语的类比推理任务，例子如下：  
vec（“蒙特利尔加拿大人”）-vec（蒙特利尔”）+vec（多伦多”）接近vec（”多伦多枫叶”）则为正确；  

本文发现Skip-gram模型符合一定的数学运算能力；

word2vec基本架构是由CBOW+Skip-gram组成的;

### CBOW（连续词袋模型）context->words next

- CBOW simple  
词袋
![图 1](../images/2fa58824c9385a4b95b986bfb2866812e7127b0e128cddd632772a02324f4357.png)  
连续词袋，用多个上下文去训练一个词；  
tips:

1. 输入层x可作为选择矩阵（其中的值均为0或1）；
2. 目标函数为：
![图 2](../images/8a557a07ce42d0ebecc344942fd0de92ead30bfd760ef320d80894db7230c8fb.png)  
并转化为  
![图 3](../images/7c08f4ff7b5548f5af4cc3a43cbf2167349f75c9dc79617f179f60840847926f.png)  

- CBOW multiple2multiple
![图 5](../images/4b17a3db995ce5eac634e763d13f40dd3b23132a3abdd41e3f5c26232e6b79fc.png)  

## word2vec提出的加速训练方法

### Hierarchical softmax 层次softmax

- CBOW based on Hierarchical softmax:
![图 9](../images/9a6edbcab25aacf3a0e0be2e630ab7d7172e7cd16bef807634dcc02f631044a0.png)  
输入：2c个词向量  
投影：累加  
⭐输出：Huffman Tree  
此处认为设定0为正类，1为负类，即将节点作为二分类器（sigmod）
  
基于以上概率函数可以总结为：
![图 11](../images/4aacf544596a5b7ea04cee1291025606046ec58c3847bab5c0298bebb60993c6.png)  

带入CBOW的目标函数可得下式，并可进一步获得梯度更新：
![图 12](../images/49bf61511c454d39a0bdad3b1c5b97f0c14f45f7fa217143af56988bc714d73c.png)  

- Skip-gram based on Hierarchical softmax:
结构与CBOW on HS相似
![图 13](../images/9531cc7e4c004c48c7b7c0ba748ab4a42cff5ece04e7a06a8b3873e8d6423019.png)  

### Negative Sampling 基于负采样的CBOW、skipgram

#### 负采样

参考博客<https://zhuanlan.zhihu.com/p/39684349>

采样的本质：每次让一个训练样本只更新部分权重，其他权重全部固定；减少计算量；（一定程度上还可以增加随机性）  
```随机选择一小部分的negative words（比如选5个negative words）来更新对应的权重。我们也会对我们的“positive” word进行权重更新;在论文中，作者指出指出对于小规模数据集，选择5-20个negative words会比较好，对于大规模数据集可以仅选择2-5个negative words。```  

一元模型分布（unigram distribution）”来选择“negative words”。
![图 15](../images/0e5b7911edea5ceab0e525168d5977917ff349ec78366f3c2968131f2cfb9b9b.png)  
![图 16](../images/77c06f7e608d30df1cb673c3aa30f28f7ff6086b89e5a6a265edc7e013fdd09e.png)  

![图 14](../images/5e0a7abbaf37f08ae5beeec580ed112d8be09db22ae2b31dd72c852402ba5d12.png)  

# Doc2Vec

word2vec的词嵌入很优秀，但其拼接后表达长句子仍然表现力很差；在word2vec的词向量基础上，能更好地表达句子的语义信息；  

一种无监督算法，能从变长的文本（例如：句子、段落或文档）中学习得到固定长度的特征表示， 它有两种训练方式：

## 分布记忆的段落向量（Distributed Memory Model of Paragraph Vectors , PV-DM）->CBOW模型；
![picture 1](../images/846a5d76e90a42094476c215d76b1fcb447b345bc56db2a2afd7e7f86a7e51af.png)  

每一句话用唯一的向量来表示，用矩阵D的某一列来表示；  
每一个词也用唯一的向量来表示，用矩阵W的某一列来表示；
每次从一句话中滑动采样固定长度的词，取其中一个词作预测词，其他的作为输入词。输入词对应的词向量和本句话对应的句子向量作为输入层的输入，相加求平均或者累加构成一个新的向量，进而使用这个向量预测此次窗口内的预测词。

其实只是增加了一个用于外置记忆和调控的句vector

## 分布词袋版本的段落向量（Distributed Bag of Words version of Paragraph Vector，PV-DBOW）->Skip-gram模型。

另外一种训练方法是忽略输入的上下文，让模型去预测段落中的随机一个单词。就是在每次迭代的时候，从文本中采样得到一个窗口，再从这个窗口中随机采样一个单词作为预测任务，让模型去预测，输入就是段落向量。
