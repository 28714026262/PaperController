<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-11-06 09:18:11
 * @LastEditTime: 2022-11-30 20:05:53
 * @LastEditors: Suez_kip
 * @Description: 
-->
# 漏洞挖掘中的图的使用

## AST

![图 1](../images/0003d529b121d7f72cee15acaf7a8de8b967f2aa23443c8c298b51ee9cd8ba31.png)  

抽象语法树特点：

- 无论是LL(1)文法，还是LR(1)等方法，都要求在语法分析构造出相同的语法树。即使是前端采用了不同的文法，都只需要改变前端代码，而不用连累到后端。
- 在构造语法树时，不依赖于语言的细节。

简单流程：

1. 词法分析，scanner。对每一个代码中的单词进行分析，并得出其性质；->数组
2. 语法分析，解析器；数组->语法树（AST会删除其中没有必要的token，如不完整的括号，这与CST（具体语法树）对应）；例babel

[2021论文](../AI漏洞挖掘/Graph/Combining_Graph-Based_Learning_With_Automated_Data_Collection_for_Code_Vulnerability_Detection.pdf)  
丰富AST，增加分支8个，特定适配不同的特殊漏洞类型，来解决一些传统方案无法挖掘的漏洞；
序列化模型的问题：误识别部分漏洞类型，代码拼接会出现问题，有可能逻辑上不一定有连续执行的可能性；
MRAKING待看

案例论文Cross-Project T ransfer Representation Learning for Vulnerable Function Discovery  
[论文链接](./../AI漏洞挖掘/Graph/Cross-Project_Transfer_Representation_Learning_for_Vulnerable_Function_Discovery.pdf)
功能级漏洞发现框架，论文设计架构：

- 使用解析器CodeSensor（岛语法）,获取无需库的AST；  
[岛语法](../AI漏洞挖掘/other/Generating_robust_parsers_using_island_grammars.pdf)：包含自由部分（剩余部分）和详细部分（结构），对原有上下文无关语法G，是G的扩展，能识别G无法识别的句子；G复杂度更高；由广义LR解析支持；
- 通过使用深度有限遍历，以串行形式获得AST；关键词的数字映射；填充与截断保证定长向量（实验中为1000个元素）；对向量的元素使用词袋和word2vec，并使用主成分分析（PCA）将嵌入投影到二维；
- Word2vec[13]嵌入的双向长短期记忆（Bi-LSTM）[7]递归神经网络；  
![图 1](../images/09333d7b4476d8f50d40249980e86356bca8069bef733e7a8456e838c55d5955.png)  
- 对小样本参数，将数据馈送到预训练的网络以学习表示的子集；
- ![图 2](../images/f38bb14dcd3621852567d59c64e304392bf731b25d860352c36189a0357b5a1f.png)  

### FIRR功率减少率

检查所需功能数量减少与随机功能数量之比；
$FIRR_{AST2CM}=1-\frac{N_{total}*recall_{CM}}{N_{total}*recall_{AST}}$

## 控制流与数据流

### CFG、CDG

cfg 控制流图->cdg 控制依赖图（由FDT前向支配树产生）：  
![图 3](../images/d0e50bfeb09e3ff1a99cb6a8574ee889845f28497135b40c98e1143fc5a36c0b.png)  

![图 7](../images/2deb881fdf0b51739e64f003625b0179a39ef034aa42cda5eddb17e1acade40e.png)  

![图 4](../images/34bdd133ec568fb6b7fc9291e0a94d593645ca442511f083cee853b9f296f517.png)  

所有从函数出口到S2的路径都一定会经过S5；比如S1 -> C1 和 C1 -> S1 互相抵消。不过这还剩一个问题，就是像 C1 -> S3 这种依赖是怎么产生的？

ACFG 源自于Genius项目见下文

### DFG、DDG

变量使用的依赖，eazy，pass

### PDG，SDG

![图 3](../images/19f6fe8d79f344c404a7143e2561e4101762fa0feea4b71688363caa6ffb4036.png)  
  
PDG是有向图，其中节点（或顶点）表示语句或控制谓词，弧（或有向边）表示两个节点之间的数据或控制依赖关系。
SDG可以通过主叫-被叫关系从PDG导出。

### NCS

即源代码各个单词的顺序出现；

论文举例：[Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics via Graph Neural Networks](../AI漏洞挖掘/Graph/NeurIPS-2019-devign-effective-vulnerability-identification-by-learning-comprehensive-program-semantics-via-graph-neural-networks-Paper.pdf)

工作流程：

1. 提取代码的AST、CFG、DFG、NCS，每个节点由代码+节点组成，分别使用word2vec进行编码再结合作为节点；
2. 通过邻接矩阵来对邻接节点的信息进行聚合，将聚合节点和当前节点一起经过GRU网络得到下一时刻的当前节点。以此类推，经过T时刻，生成所有节点的最终的节点表征；（就剩了个邻接矩阵，初始为{0，1}，之前获取的那些信息不用了？）
3. 不使用节点特征线性的输入到MLP中然后通过softmax分类的一般方案，本文使用Conv进行训练一维卷积和dense层来对节点特征进行提取从而实现图级别的分类

## 图嵌入

<https://zhuanlan.zhihu.com/p/62629465>

图分析的目的包括四种： ( a )节点分类，( b )链接预测，( c )聚类，( d )可视化
嵌入的思想是在向量空间中保持连接的节点彼此靠近。拉普拉斯特征映射（Laplacian Eigenmaps）和局部线性嵌入（Locally Linear Embedding ，LLE）
自2010年以来，关于图嵌入的研究已经转移到解决网络稀疏性的可伸缩图嵌入技术上。
保持一阶二阶网络邻近度

目前研究的难点和目标：  

- *属性选择*  节点的“良好”向量表示应保留图的结构和单个节点之间的连接。第一个挑战是选择嵌入应该保留的图形属性。考虑到图中所定义的距离度量和属性过多，这种选择可能很困难，性能可能取决于实际的应用场景。
- *可扩展性*  大多数真实网络都很大，包含大量节点和边。嵌入方法应具有可扩展性，能够处理大型图。定义一个可扩展的模型具有挑战性，尤其是当该模型旨在保持网络的全局属性时。
- *嵌入的维数*  实际嵌入时很难找到表示的最佳维数。例如，较高的维数可能会提高重建精度，但具有较高的时间和空间复杂性。较低的维度虽然时间、空间复杂度低，但无疑会损失很多图中原有的信息。

大体上可以将这些嵌入方法分为三大类：

- 基于因子分解的方法
- 基于随机游走的方法(源于word2vec)
    首先选择某一特定点为起始点，做随机游走得到点的序列，然后将这个得到的序列视为句子，用word2vec来学习，得到该点的表示向量。
  - deepwalk，使用RandomWalk一种可重复访问已访问节点的深度优先遍历算法；每个节点开始分别遍历，直到访问序列长度满足预设条件。使用skip-gram model进行向量学习，使用Hierarchical Softmax来做超大规模分类的分类器；
  - node2vec
- 基于深度学习的方法
- LINE
  PAPER SOURCE：ang J , Qu M , Wang M , et al. LINE: Large-scale information network embedding[J]. 24th International Conference on World Wide Web, WWW 2015, 2015.

## 激活函数

1，相比Sigmoid/tanh函数，使用梯度下降（GD）法时，收敛速度更快

2，相比Sigmoid/tanh函数，Relu只需要一个门限值，即可以得到激活值，计算速度更快

缺点是：

Relu的输入值为负的时候，输出始终为0，其一阶导数也始终为0，这样会导致神经元不能更新参数，称为“Dead Neuron”。

为了解决Relu函数这个缺点，在Relu函数的负半区间引入一个泄露（Leaky）值，所以称为Leaky Relu函数；

$$
LeaekyReLU(x) =
\begin{cases}
x, & x\gt 0 \\
ax, & x\le 0
\end{cases}
$$

## 聚类

使用聚类算法：频谱聚类算法
[谱聚类的相关知识](https://www.cnblogs.com/pinard/p/6221564.html)

### K-means聚类算法介绍

[K-means聚类算法](https://www.cnblogs.com/pinard/p/6164214.html)  

![图 10](../images/9a750b0e6c05358cd103a6e1bd3e40c978bbbdb0062e176f63715c04059d8e44.png)  

简单介绍：  

``` 上图a表达了初始的数据集，假设k=2。
  在图b中，我们随机选择了两个k类所对应的类别质心，即图中的红色质心和蓝色质心，
  然后分别求样本中所有点到这两个质心的距离，并标记每个样本的类别为和该样本距离最小的质心的类别，如图c所示，
  经过计算样本和红色质心和蓝色质心的距离，我们得到了所有样本点的第一轮迭代后的类别。
  此时我们对我们当前标记为红色和蓝色的点分别求其新的质心，如图4所示，
  新的红色质心和蓝色质心的位置已经发生了变动。
  图e和图f重复了我们在图c和图d的过程，即将所有点的类别标记为距离最近的质心的类别并求新的质心。
  最终我们得到的两个类别如图f。
```

- ***传统K-means算法流程***  
  1. 经验确定k值；
  2. 随机选择k个样本作为初始质心；
  3. 计算其他点到已选质心的欧式距离，将最小值加入对应的聚类中；
  4. 重新以平均值计算该类的质心；
  5. 若质心不再变化则结束，否则继续执行第三步；
- ***K-means++算法流程***  
    优化质心选择算法：  
  1. 随机选择一个点作为起始质心；
  2. 计算为选择点到已选择点的距离（取各个点中的最小值），取其最大值作为下一个质心；
  3. 重复2直至完成k个点的质心选择；
- ***距离计算优化的elkan K-means算法***  
    执行两种规律，利用质心间的距离减少点到质心的计算距离：  
  1. 是对于一个样本点x和两个质心μj1,μj2。如果我们预先计算出了这两个质心之间的距离D(j1,j2)，则如果计算发现2D(x,j1)≤D(j1,j2),我们立即就可以知道D(x,j1)≤D(x,j2)。此时我们不需要再计算D(x,j2),也就是说省了一步距离计算。
  2. 规律是对于一个样本点x和两个质心μj1,μj2。我们可以得到D(x,j2)≥max{0,D(x,j1)−D(j1,j2)}。这个从三角形的性质也很容易得到。
- ***大样本优化 Mini Batch K-Means算法***  
  选取部分集中的样本首先进行传统K-means算法，batch size一般是通过无放回的随机采样得到的。  
  为了增加算法的准确性，我们一般会多跑几次Mini Batch K-Means算法，用得到不同的随机采样集来得到聚类簇，选择其中最优的聚类簇。

### DBSCAN聚类算法

[参考博客链接](https://blog.csdn.net/hansome_hong/article/details/107596543)

DBSCAN是一种基于密度的聚类算法，基于定义距离下的半径内最少点数目进行聚类；邻域半径R内的点的个数大于最少点数目时就是密集。

评价：简单快捷，仅按照点与点之间的距离作为判断依据，因此半径和最小内点数量需要经验设计；

***节点定义***：

- *核心点*：邻域半径R内样本点的数量大于等于最小内点数量；
- *边界点*：不属于核心点但在某个核心点的邻域内；
- *噪声点*：排除上述两者剩余的点；

***关系定义***：

- *密度直达*：
  - 出发点是核心点（具有单向性）；
  - 在R邻域内；  
- *密度可达*：
  - 间接直达；
  - 基于直达，以此也具有单向性；
- *密度相连*：
  - 取消起点是核心点的要求（去除单向性）后，密度可达；
  - 具有双向性；
  - 在该定义下，密度相连的两组认为同属一个簇；
- *非密度相连*：
  - 非密度相连的情况；
  - 表示不属于同簇或者为噪声点；  
![图 1](../images/6be44811f06330664413b8b31d79916981f06a1f897e6cbdc4cc4d52513a9357.png)  

***聚类流程***：

*输入*：数据集，邻域半径 Eps，邻域中数据对象数目阈值 MinPts;
*输出*：密度联通簇的集；

1. 从数据集中任意选取一个数据对象点 p，按照参数Eps（半径）和MinPts判断点p是否为核心点；
2. 是，则找出所有从 p 密度可达的数据对象点，形成一个簇；
3. 否则选取另一个数据对象点；
4. 重复2、3步，直到所有点被处理。

## 图神经网络

### ***Scalable Graph-based Bug Search for Firmware Images***  

[论文链接](../AI漏洞挖掘/Graph/Scalable%20Graph-based%20Bug%20Search%20for%20Firmware%20Images.pdf)  

固件漏洞挖掘

参考计算机视觉中的技术，基于CFG的高阶向量的表示方法 Genius
  
计算机视觉图形检索的主要步骤：  

1. 原始特征提取
2. 码本生成
3. 特征编码
4. 在线搜索
离线索引（包括前三步）和在线搜索

#### 文章提出的ACFG
  
![图 1](../images/cdebf2f7de4f85f6b87f956bf48ff41154e83a1a42b966c8982896d20f96f139.png)  
![图 4](../images/968ed2073433c3a3a94664f60c99289b955b3312263923cc8face66b466b9155.png)  
![图 2](../images/d73fe08ae22f4b3d70cb991e7fdf4f9b8892e771db860534866cbe71668763ba.png)  

其他方法MCS最大公共子图，效率有限

#### 码本生成

从原始特征中学习一组分类：C={c1，c2，…，ck}，其中ci是第i个码字或“质心”，共分为两步：

- 相似性度量计算：
  二部图法量化相似性，并用结构特征添加来防止二部图无图结构特征造成的误差积累导致不精确  
  将两张ACFG图组合为一张二部图，每个匹配都与成本相关联。两个图的最小代价是映射上所有边代价的总和。二部图匹配可以有效地遍历所有映射，并以最小的代价选择从G1到G2的节点上的一对一映射。边缘成本由该边缘上两个基本块之间的距离计算。  
  ![图 6](../images/8e1d5d4507ea48ab477a94fb3eb35abb4b2fc3d0bd324bb44f64208e8f1c7d88.png)  
  如果特征是集合，我们使用Jaccard来计算集合差。  
- 利用空图计算的归一化；  
  两个图的匹配成本大于一，并且与比较的ACFG的大小正相关。因此，我们将成本归一化以计算相似性得分。对于成本归一化，我们为每个比较的ACFG创建一个空ACFGΦ。空图中的每个节点都有一个空特征向量，并且空图的大小被设置为对应的比较图的大小。通过与这个空的ACFG进行比较，我们可以获得被比较图可以得到的最大匹配成本;  
  $\kappa(g_1,g_2)=1-\frac{cost(g_1,g_2)}{max(cost(g_1,\phi),cost(\phi,g_2))}$  

  学习目标是找到能够最大化不同ACFG的距离同时最小化等效ACFG距离的权重参数(人话：不同类差距最大化，近似类差距最小化)  

  雅卡尔指数（英语：Jaccard index），又称为交并比、雅卡尔相似系数，比较样本集的相似性与多样性的统计量，定义为交集与并集的比值；  
  雅卡尔距离（Jaccard distance）用于量度样本集之间的不相似度，其定义为1减去雅卡尔系数；
  有人将雅卡尔距离定义两集合对称差$A\Delta B=|A\cup B|-|A\cap B|$的大小与并集大小之间的比例
  
- 聚类
  输入为相应ACFG的相似性得分核矩阵，为用于训练集的ACFG划分，寻找聚类和划分质心，所有质心节点的集合构成代码本。此处考虑效率和准确率，码本大小设置为16；

  分层抽样：首先收集一个数据集，该数据集涵盖了来自不同架构的不同功能的ACFG。参见第5.2节。然后将ACFG分成不同尺寸范围的单独“地层”。然后将每个层作为独立的子群体进行采样，从中随机选择各个ACFG。

加速方式：并行聚类、近似聚类、层次聚类算法

#### 特征编码

- 能更好容忍函数在不同体系结构中的变化，每个维度都是与分类的相似关系，与ACFG本身相比，该分类对二进制函数的变化不太敏感。
- 编码后的ACFG原始特征成为高维空间中的一个点，可用hash方法快速搜索；  
  $q:G\to R^n$ in $C=\{c_1,...,c_n\}$  
  设$NN(g_i)$表示图$g_i$码本中最近质心邻居
  $NN(g_i)=\arg\,\max_{c_i\in C}\kappa (g_i,c_j)$  
  图像检索中的一种常见做法是不仅考虑最近的邻居，还考虑几个最近的邻居;

1. 特征包编码BOF模型  
特征包编码将图形映射到码本中的一些质心，将每个函数表示为特征包。量化器是将图转化至码本中的最近质心的独热码；

2. VALD编码  
词袋是只要质心是图的最近邻居，图与质心距离就会被忽视；
该方案合并一阶差异，将图分配给单个混合物组分
![图 1](../images/9f9c0bf5318fe69804dee2ecf970deb89b0cad029affefc69474b9539610d125.png)  
将独热码更改为相关信息，提高了向量包含的语义信息，反应了质心的相似性分布；  
以三个函数举例：
F1在x86的架构下编译的结果，F1在mips架构下编译的结果，F2在mips下编译的结果；
![图 2](../images/039e6fd4f9e6195c16f26a4a7d00ab665f748e52cbf02ec69b1269990fac42e9.png)  
   - 编译不同，结构图存在一定的差别；
   - 相似性是最大共子图/最大图；
   - 成对匹配将通过ACFG直接匹配两个函数，而Genius将通过编码向量匹配它们。VLAD编码通过将ACFG与其码本中最接近的前3个质心节点进行比较来生成编码向量。

#### 在线搜索

LSH（位置敏感散列）

1. 使用BOF算法或VALD算法，进行函数特征编码；
2. 使用LSH，通过学习投影来在大数据集中进行查询；投影公式：  
$h_i(q(g))=\lfloor(v·q(g)+b)/w\rfloor$  
where w is the number of quantized bin, v is a randomly selected
vector from a Gaussian distribution, and b is a random variable
sampled from a uniform distribution between 0 and w.  
理论基础：如果两个点在特征编码空间中更靠近，那么它们在哈希空间中的投影之后应该保持接近；
$lsh(g)=[h_1(q(g)),...,h_w(q(g))]$
距离可用余弦距离和欧氏距离；

基线软件：

- discovRe
- Multi-MH和Multi-k-MH
- 基于质心的搜索

## 图模型

部分性能的比较图如下：  

- 图模型：  
![picture 3](../images/406be646941bfa0d07fb183f2a0766214dc0c73d7620820722200578770ad854.png)  

- 图表示：  
![picture 4](../images/c653c8755e9d50f3dd71d0152b161dfddbccecee44762201460ced90cc6adf52.png)  

- 图嵌入：  
![picture 5](../images/5d21762565e2342d46d71ab537c6b19993d62bd8da641dabe0edf58a8b64c087.png)  

来自论文[Neural software vulnerability analysis using rich intermediate graph representations of programs](../AI漏洞挖掘/Graph/Neural%20software%20vulnerability%20analysis%20using%20rich%20intermediate.pdf)

### GGNN

[论文链接](../AI漏洞挖掘/Graph/GGNN.pdf)

先前关于图结构输入的特征学习的工作主要集中在产生单个输出的模型上，如图级分类，但图输入的许多问题需要输出序列。比如图上的路径、具有所需属性的图节点的枚举，或与起始节点和结束节点混合的全局分类序列。

图上的特征学习有两种设置：（1）学习输入图的表示，(2) 在生成序列的过程中学习内部状态的表示输出。

是基于GRU在空间域message passing的模型；

![图 1](../images/65f08b4d3caf68fa5394cc4ef296431bb0175ab7a2af44fa0908c6a1260dc714.png)  
上图为控制图中节点如何通信的稀疏矩阵的例子表示

输入与训练：  
![图 2](../images/149be8a669cb6cddb743cb48b2a62d67d72da6f220dbecac41f8847f0e7e566c.png)  
等式1是初始化步骤，它将节点注释复制到隐藏状态的第一个分量中，并用零填充其余部分。  
等式2是通过输入和输出边在图的不同节点之间传递信息的步骤，其参数取决于边类型和方向。$a^{(t)}_v\in R^{2D}$包含来自两个方向的边的激活。  
其余的是类似GRU的更新，它包含了来自其他节点和前一个时间步的信息，以更新每个节点的隐藏状态。  
z和r是更新门和重置门;
使用BPTT算法（Back Propagation Through Time）以计算梯度。

输出：

- 图级输出  
图级表示向量：
$h_G=tanh(\sum_{v\in V}{\sigma(i(h_v^{(T)},x_v))\odot tanh(j(h_v^{(T)},x_v))})$
i和j是神经网络,以$h_v^{(T)}$和$x_v$的级联作为输入,输出实值向量的。$\sigma(i(h_v^{(T)},x_v))$可以作为一种注意力机制；
- 节点输出

->GGS-NNs(Gated Graph Sequence Neural Networks)使用多个GGNN网络生成输出序列；

### GCN

RNN针对一维结构，针对序列前后信息的互相影响，图不存在这样的线性关系；
CNN针对二维结构，依靠的是平移时的结构不变性，使得参数能够在各个核中共享，但图不存在这样的优势；
图并不能用上述欧式空间描述；-> GNN;DeepWalk;Node2vec  

![图 4](../images/ba8cc8f067bf58fbc6831c74fec422d951584b30a754553f3539721faee03ad6.png)  

$\hat{A}=A+I, \hat{D}是A$的节点度矩阵；

邻接矩阵A对角为0，因此与H相乘时，会放弃自己node的特征，因此$\hat{A}=A+I$,让H相乘时获取自身特征；  

$\hat{D}^{-\frac{1}{2}}\hat{A}\hat{D}^{-\frac{1}{2}}$进行归一化  

![picture 2](../images/01842f73546788c10ca4392d35bd01ba73f65a4c800c0fcffe7dc02e63125957.png)  

$c_{ij}$为归一化因子；N是该层中第i个单位的单跳邻居集合；  

![图 3](../images/16fba8ee3d3a2733c50f8ede3ee324e03b19023a42b62708ff35f044d6df9ab3.png)  

[作者博客链接](http://tkipf.github.io/graph-convolutional-networks/)

### GAT

[博客链接](https://zhuanlan.zhihu.com/p/134148937)  
图方法分为谱方法和空间方法：

- 谱方法是将图映射到谱域上，例如拉普拉斯矩阵经过特征分解得到的空间，代表方法之一是GCN；
- 空间方法是直接在图上进行操作，代表方法之一GAT；

学习流程：

- 输入:N个节点的特征$h=\{h_1,...,h_N\}$，$h_i\in \Kappa^F$  
- 乘W变换，将h映射到维度$\hat{F}$
- 注意力权重$e_{ij}=a(Wh_i,Wh_j)$
- softmax函数归一化
- 注意力机制是一个单层的前馈神经网络，激活函数采用LeakyReLU
- 注意力参数$a_{ij}=softmax_j(e_{ij})=\frac{exp(e_{ij})}{\sum_{k\in N_i}exp(e_{ik})}$
- $\hat{h_i}=\sigma(\sum_{j\in N_i} a_{ij}W\hat{h}_j)$
- 输出:$\hat{h}=\{\hat{h}_1,...,\hat{h}_i\}$，$\hat h_i\in \Kappa^F$

采用多头注意力（Multi-head Attention）扩展注意力对模型是有提升的。  
采用K头注意力机制的两种计算公式如下：

1. 拼接方式：  
![图 6](../images/970a4a3b91082701f3a1a00fdd97b9a256c717300e1294261ed1bed9239d7d72.png)  
2. 均值方法：  
![图 7](../images/d50803a7e7da43a06a812824d82efcd2d5a3e0a6f1640bc42d403a79c29c4f3d.png)  

### Highway GCN

缩写为H-GCN，来自于Highway Network；

- Highway Networks
  - 在门机制引入了transform gate T,carry gate C;
  - 残差连接：$y=H(x,W_H)\cdot T(x,W_T)+x\cdot (1-T(x,W_C))$
  ![图 1](../images/77fe0a480564856489e8bbbb7e72773e1a58f04c2604331eec3796a327b7daf0.png)  
  ![图 2](../images/7112e2d883bfbedca878b0b268e9b737635d018e906550a6c5ca6241cc671b06.png)  
  由上图可知，该网络部分忽视输入，部分处理；

### DEEPGCNs

TODO

### JUMP KNOWLEDGE NETWORK

TODO

## TF-IDF

TF-IDF是潜在语义分析（LSA）技术的一个示例，该技术给出了一个文档语料库，为语料库的每个文档中的每个术语提供了分数。  
TF-IDF(t,d,D)=$f_{t,d}\multimaplog\frac{|D|}{|D_t|}$

其中$f_{t,d}$,是文档d中的t术语频率；|D|文档数量，|$D_t$|包含t的文档数量；TF-IDF的一个重要限制是该技术产生的张量的高维度。解决这个问题的一种方法是使用统计降维技术，例如主成分分析（PCA）或奇异值分解（SVD）。这种方法执行正交线性变换，并且能够将高维数据投影到低维空间[1]。  

![picture 1](../images/477b3503abfb8eab4b9d2e51a789139ee69fd5c70a79e375d465569fb812a3aa.png)  

