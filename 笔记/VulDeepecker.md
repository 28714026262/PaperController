<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-10-26 14:54:55
 * @LastEditTime: 2022-12-19 00:02:03
 * @LastEditors: Suez_kip
 * @Description: 
-->

# vulpecker

[论文链接](../AI%E6%BC%8F%E6%B4%9E%E6%8C%96%E6%8E%98/TraditionalStatic/VulPecker.pdf)

测试基准：表征补丁的一组特征；代码相似性算法；

基于假设：代码重用(精确克隆、重命名克隆、近乎缺失克隆和语义克隆)

当时研究存在的问题：

- 不存在稳定的训练集；
- 代码相似性算法缺失；无法区分脆弱代码和其修补代码!
ReDeBug[13]可以在代码库的OS分发规模上快速找到未修补的代码克隆，但很难应用于涉及变量名修改、行添加或删除等的代码克隆。

该程序贡献：自动化检测漏洞的存在性和位置;VPD与VICD的漏洞集<https://github.com/vulpecker/Vulpecker>  
![图 4](../images/4689dac246d8c8d0b1962685905173bac23d8d00aca9d539eeda2b40a2a3811d.png)  

五种补丁特征：

- 非实质性特性：对有用代码没有影响的空白、格式或注释的更改。
- 组件特征：变量、运算符、常量和函数等语句中组件的变化。
- 表达式特征：赋值表达式、if条件和for条件等语句中表达式的变化。
- 语句特征：涉及添加、删除和移动的语句的变化。
- 函数级特性：函数的变化或函数外部的变化，如宏和全局变量定义。
![图 1](../images/b37faae08429488a569cbe4b4d237f7b7d98a91332efe29480608fc3414e0be0.png)  

## 代码表示粒度

无上下文补丁、切片、带上下文补丁、函数和文件/组件  
在无上下文补丁片段级别，通过提取以“-”符号为前缀的连续行（表示应该修补的行），从diff文件中获取片段。该粒度已用于错误检测。在切片片段级别，根据程序依赖图（PDG）对程序进行切片。由于切片通常保留PDG的结构，因此子图之间的同构表示代码相似性。该粒度已用于克隆检测。在具有上下文片段级别的补丁中，通过提取以“-”符号为前缀的行和没有前缀的行，从diff文件中获取片段。该粒度已用于错误检测和漏洞检测。在函数片段级别，函数被视为一个独立的单元。该粒度已用于漏洞外推和克隆检测。在文件/组件片段级别，每个文件/组件都被视为一个单元。这种粗粒度主要用于漏洞预测

## 代码表示

特征提取：

1. 可以直接从差异块中提取非实质性特征和功能级特征。
2. 其他三种类型的补丁特征（即表中的类型3–类型5）可以通过一系列编辑操作从未修补的代码段提取到修补的代码，例如gumtree算法。
3. 漏洞差异块的特征向量由基本特征和补丁特征组成。代码相似性算法选择引擎。

## 表示比较方法

矢量比较和近似/精确匹配。向量比较方法首先将漏洞的表示和目标程序的表示转换为向量，然后比较这些向量以检测漏洞。近似/精确匹配方法通过包含、子串匹配、全子图同构匹配或近似γ-同构匹配搜索目标程序代码表示中漏洞的表示。

1. 根据是否能分类补丁前后的文件，筛选一批算法s；
2. 平均分配一组漏洞代码差一块特征向量F为F1与F2；
3. F1测试算法的正确性，依照准确率a的阈值进行筛选；
4. F2测试相似性算法是否能识别补丁代码为无漏洞来筛选；

5. 将补丁删除的行默认为漏洞点，进一步将切片hi为核心代码片段的近似值；
行数差距量化表示代码片段级别间的差距，五种代码级别cf与未修补代码片段切片cc的近似程度DOA；  
$doa(cc,cf)=\frac{|l_{cf}-l_{cc}|}{l_{cc}}$追求DOA最小化；  
核心代码属于slice左右的粗糙程度，因为补丁删除的代码行被认为是易受攻击的代码行；$doa(cc,sc)<doa(cc,pc)和doa(cc,sc)<doa(cc,pwc)$，slice的DOA最小，若无法提取slice，patch with context的DOA最小，因为没有上下文的补丁在代码片段级别的表示不能从对应于所讨论的差异块的未修补代码片段中提取；
搜索最小化DOA的代码粒度；
6. VCID评估si
   1. 首先进行筛选：
      1. VCID中的代码重用实例不能应用于相似性算法si，对于没有“-”前缀符号的diff hunk，使用无上下文补丁的代码片段级别的代码相似性算法不能用于识别该diff huck的代码重用实例；
      2. 如果两个代码重用实例具有相同的代码重用特性，并且被si同时检测为易受攻击或不受攻击（即si无法区分它们），则其中一个将被消除；
   2. 使用筛选si的FNR
7. 漏洞签名生成；提取与漏洞对应的修补的/未修补的diff代码和未修补的代码片段，“-”、“+”符号和无前缀获得未修补的差异代码；代码预处理，去除空白与冗余，修补不完整部分；根据diff hunk选择的si的代码表示，来表示预处理的有/无补丁的差异块和未补丁的代码块；
8. 签名搜索；漏洞检测引擎使用为diff hunk选择的代码相似性算法的比较方法从目标程序签名中搜索漏洞签名。

![图 2](../images/961fdc35330cbb07f10e78658d1e2beea3bcbab8467ab18ed6bd4faf73636adf.png)  

# VulDeePecker

[论文链接](../AI漏洞挖掘/vuldeepecker.pdf)

***PAPER SOURCE:VulDeePecker: A Deep Learning-Based System for
Vulnerability Detection***
  
## 基本信息

相对VUDDY 和 VulPecker的项目：VUDDY和0%，0%，该文章追求的是只要假阳性率不太高，就可以把重点放在降低假阴性率上。  

**Target：** 泛化性、专业知识转化率（仍然需要人工先验知识）、自动化水平
  
## VulDeepecker设计准则

1. 转化为保留数据依赖性以及控制依赖性等信息的中间状态在进行学习，以保证网络的feed包含非扁平代码信息；code gadget 一串不连续的包含上下文含义的代码段；
2. 细粒度的划分可以保证后期漏洞定位力度，划分粒度应小于函数级别，以确定小代码片段；code gadget
3. 存在上下文分析的需求->适合用于NLP的网络框架（e.g. RNN（存在梯度消失VG问题，其双向变体BRNNs继承）、LSTM、GRU（这二者通过加入memory cell用于解决VG，其中LSTM优于GRU，LSTM单向性导致只受到前缀影响，弃用）、BLSTM（解决LSTM单向性））  
![图 2](../images/6e500bbaad919871637121739a843c03fd3431ab5dec42c9c06e192774b448b6.png)  
softmax layer表示和格式化分类结果
Dense Layer为密集层，也即FCN全连接，此处用于减少复杂BLSTM的输出向量维度；  
BLSTM Layer包含复杂的LSTM cell；参考文献：**S. Hochreiter and J. Schmidhuber, “Long short-term memory,” NeuralComputation, vol. 9, no. 8, pp. 1735–1780, 1997.**
![图 1](../images/8acaec0cd2c9ee3b73cfd89e1e8ec9acbf742338510b3012fabc0b2f9587b048.png)  
![图 2](../images/2e39980b6261de761dc232fb3d8fe08d11834479106cef623af011931446e248.png)  
![图 3](../images/68bfcca11e51be88453111aeba97acc2ba0e202da8062d6bf517d23344cbf181.png)  

## 具体设计

### code gadget

包含数据依赖和控制依赖信息的数段代码句（此处以行为单位）

以关键点的启发式（***该问题可以进一步研究***）：  

- 其中，关键点为漏洞中心或提示存在漏洞的代码段；
- 漏洞中心指该类漏洞的发生点、发生原因等；
- 一对多且多对一（例如，缓冲区错误漏洞可能对应于以下关键点：库\API函数调用、数组和指针）  

该文章仅研究的是与库/API函数调用的关键点相对应->是一篇证明性质的文章

主要研究过程：

![图 4](../images/7675bc21e14442107aad2cf3e5d3e68260a46dc902af42b5ec9566b7c8f9bb0d.png)  

### 学习阶段

- 步骤一：
  
1. 提取关键点（此处是API/库的调用）；包括前向call（来自于命令行、程序、套接字或文件的外部输入直接作用于函数，recv）和后向call（没有来自于外部输入直接作用于函数strcpy）；  
2. 为绕关键点的参数信息提取code slice；前向集中考虑直接输入的参数，后向集中考虑输入参数前期的语句；下面的例子中每一个参数都能提出一条code slice；  
![图 5](../images/affc907ce6c4eaddc46af180b03c4e32bc0895395dd80678ecc8714805877650.png)  
前向切片对应受所讨论的参数影响的语句（调用时或之后的分支与该参数相关的），后向切片对应可能影响所讨论的变量的语句（时或之前合并与该参数相关的）。  
前向调用考虑后续内容，后向调用考虑之前处理；  

- 步骤二：

1. slice->gadget 将一组slice对应到一个centre，此处就是一个API/库函数的调用；这里是将多对一转化为一对一；  
   1) 首先将同一函数域中的slice整合，去重（与同一func存在联系）；
   2) 组装不同函数域的slice，顺序有则保留，没有则随机；
    ***问题：当存在one slice对multiple centre，那么完成后每个centre对应一个gadget，会不会导致一个slice在多个centre里共用？ --复用好像问题也不是很大***

2. lable the code gadget

- 步骤三：code gadget -> vector
  
![图 7](../images/4f763505c29510d93411165b32b9fddfd3d0db89fff64b95181d435606eacb98.png)  

1. 将gadget转化为特定符号，来保留语义；

    - 去除冗余信息（非ASCII，注释）；
    - 标准化用户定义（参数与函数）；

2. 符号表示的gadget转化为向量；word2vec 后向前端补零后端删，前向后端补零前端删，以保证等长

- 步骤四：标准BLSTM学习

### 测试阶段

- 步骤一：跳过学习阶段中的gadget Labeling，完成其前三步；

- 步骤二：使用模型；

检测指标：metrics false positive rate (F P R),
false negative rate (F N R), true positive rate or recall (T P R),
precision (P ), and F 1-measure (F 1)；  
  
测试集选择：  
NVD in NIST(National Institute of Standards and Technology)<https://nvd.nist.gov/>  
SARD(Software Assurance Reference Dataset)<https://samate.nist.gov/SRD/index.php>  

测试目标选择：缓冲区溢出漏洞和资源管理错误漏洞；
minibatch stochastic gradient descent together with ADAMAX；

在足量样本的基础上，如SARD，该项目效果优于VukPecker、Xen4.6.0、Libav10.2,但是在NVD数据集上，260个程序的体量的训练集上，效果没有VulPecker等效果好；  
有人类提供进一步标签的状况下，效果会更优异；

## 未来方向

- 仅限于源代码，目前无法适用于二进制可执行文件类等；
- 仅限于C++；
- 目前vul center仅限于API和库函数的调用；
- 切片的设计仅限于数据流的管理；
- code -> slice -> gadget -> simblization -> vector直观但有待进一步研究；
- 仅限于BLSTM；
- 该论文对系统的评价有限；最好可以发现0day漏洞的能力、扩大研究方向；

## 相关工作

1. 基于模式
   1. 模式由人类专家手动生成：**开源工具Flawfinder、RATS和ITS4、商业工具Checkmarx、Fortify和Coverity**，存在较高的假阳性率或假阴性率；
   2. 根据预先分类的漏洞半自动生成的，特定于一类：***缺失检查漏洞、污点式漏洞和信息泄漏漏洞**
   3. 无预先分类的半自动生成，依赖于人类专家定义特征来表征漏洞；这类粒度粗，导致无法确定位置；
2. 基于代码相似性（划分、抽象、相似性计算）仅能检测i，ii类漏洞（clone），以及一部分iii类（语句的删除、插入和重新排列）；
3. 基于深度学习：标记映射向量、AST节点映射向量

# $\mu$VulDeePecker

基于VulDeePecker的code-gadget，该文章加入了以下内容，实现了一个六步训练模型：

- 除了数据流信息，还捕获了一定控制流信息；
- 注意力机制，针对类似于调用等信息的关注，以获得等有效的语义信息来帮助系统分类；
  - 强制执行数据源检查
  - 关键路径检查（条件语句）
  - 危险函数使用检查
  - ......

数据集来源是SARD和NVD；
针对C/C++库适配的检测范围：
![图 7](../images/a8372697270c2df68c7a15683f70a5ec3eba5e15c53ee3605036ec7532faa7d2.png)  

## Step I

首先将程序分析并分解成code gadget；

1. 在增加节点行为分类的基础上，系统依赖图生成；SDG源自一组程序依赖图（PDG），其表示数据依赖和控制依赖关系（Joern用于构建PDG）；
2. 实现调用的提取，与库定义的调用进行匹配；
3. 使用了双向切片的CF和DF的同时获取，数据流覆盖控制流；对VulDeepecker的三个问题进行改进：仅考虑DFG；仅考虑前向函数和后向函数；考虑这两类的时候只进行相应的切片，切片方式单一；
![图 4](../images/e2c3605ea06c7775b4be19629fdec3ec149d7bc21b5a8183186a1ab199e8e81b.png)  
   1. sbvi识别SDG中节点n的后继节点；
   2. sfvi识别SDG中节点n的前置节点；
   3. 合并sfvi和sbvi；

## Step II

设置gadget标记：0为无漏洞1为各类漏洞；

## Step III

编码习惯影响后期学习，因此对代码进行预处理，将用户定义全部标准化；

## Step IV

解析规范化code gadget，分为以下三步：

1. 分析将语句pi解析为有序的标记集；
2. 通过分析这些标记的上下文结构推断语句pi的属性attr（例如，“def”、“cond”、“expr”）；
3. 对以下内容设置关注度：
   1. 库/API函数call中assignment的定义；
   2. 控制语句，判断边界检查和安全筛选的存在性和合理性；
   3. 库/API函数call语句；  

![图 5](../images/9776dfd52d92d063df2a09596856c7cdd39d9a5bf101dad5c600339a95918b16.png)  

## Step V

对code gadget进行嵌入为的等长的单词向量（skip-gram，窗口大小为10，向量维度为50，完成后拼接、裁剪或填充）和注意力向量；

## Step VI

分为三个Bi-LSTM模型和预处理层：

1. 预处理层主要过滤0向量；
2. 训练局部特征(from attention)使用相同的网络的小规模网络，每个神经元相当于一个时间步长，并在一个code gadget中接收一个单词；
3. 训练全局特征(from code gadget)，使用合并层、BLSTM层和softmax分类器；
4. 基于local and global feature训练综合特征；
![图 6](../images/ecf4b7f3ba080a79c7fc7664ce659b4158a1bebd556cd34ea77e4da536875594.png)  

## 多类型统计

L为漏洞类型总数；  
![图 8](../images/08e4d2ff14d7ea24d1fadc1574e9106fd405ea29d383a8d136cc9241a0aaebe1.png)  

- RQ1:mVulDeePecker对多类漏洞检测的有效性如何？  
![图 9](../images/91975bb2b3706209b81a8678340be43644bb621f4e965ba190afb486a273dea1.png)  
- RQ2：适应控制依赖性确实提高了mVulDeePecker在多类漏洞检测中的有效性吗？  
当额外调节控制依赖性时，mVulDeePecker可以将M_F1提高12.63%，W_F1提高11.13%，M_FNR降低12.27%，W_FNR降低6.9%。  
- RQ3：mVulDeePecker能否与其他基于深度学习的系统（例如，VulDeePecker）一起使用以获得更高的效率？  
![图 10](../images/79ab9ce48b8f30f694a46a3007a654cfe8043efef3da5a68abc9b38292eb916c.png)  

## 附录信息

### 图像处理的注意力机制

分为： 硬注意力、软注意力、此外，还有高斯注意力、空间变换；

- 强注意力是一个不可微的注意力，每个点都有可能延伸出注意力，随机的预测过程，更强调动态变化，训练过程往往是通过增强学习；
- 软注意力是可微的，是确定性的注意力，可以通过网络生成；始终计算，会导致无意义的过度参数化；
  - 空间域(spatial domain)
  - 通道域(channel domain)
  - 层域(layer domain)
  - 混合域(mixed domain)
  - 时间域(time domain)
- 自注意力是注意力机制的改进，其减少了对外部信息的依赖，更擅长捕捉数据或特征的内部相关性，以（key, query, value）的三元组提供了一种有效的捕捉全局上下文信息的建模方式。由于每一个点都要捕捉全局的上下文信息，这就导致了自注意力机制模块会有很大的计算复杂度和显存容量。

# VulDetector

针对函数粒度的C/C++漏洞的静态分析工具

## Prestep 数据收集

1. CVE爬取func name和file name;
2. 函数名、文件名不可用则求助于相关文件名和函数名可能所在的补丁;
3. 补丁链接不可用则搜索其他网站

## STEP I 图提取

在CFG的基础上为加权特征图（WFG）模型：每个节点设置了不同的权重，其中权重表示节点对精确定位语句的敏感性

## STEP II 关键词、code gadget提取

### 关键词获取

解决直接从CVE等专家经验中获取泛用性与兼容性较低，这里使用概括从Diff文件中提取的标识符；  
对标识符进行Kmeans聚类后，手动确定代表性单词（自动化水平降低一大截）  
这里可能错过了if检查和指针算术等语句...  

计算概括标识符的重要性，最后根据其重要性选择关键字：

- TF术语频率：一个术语在文档内部发生（出现）的次数；
- IDF反向文档频率（弃用）：DF逆相关；
- DF文档频率：文档频率是指包含特定术语的文档的数量；
- 重要性由TF ∗ DF表示。

本文CWE确定top-K（K表示所选关键字的数量）关键字；

### Code Gadget 获取

关键字分割函数的控制流图，与匹配关键字具有控制和数据依赖性的节点和语句；  
关键词从定位到根行开始进行BFS搜索（本文设置的阈值为5），获取向前向后行切片；  
关键词从定位到根节点开始进行BFS搜索（本文设置的阈值为5），获取向前向后CFG切片；  
关键思想是将代码块的文本AST表达式嵌入到量化向量中，然后将其分配给图节点。  
这一步排除小函数，因为根据前人经验，小函数复杂度低，脆弱性也相对较低；  

### WFG生成

向量的每个维度表示AST中的一个类型（例如，V值定义，If控制节点），其值测量代码块的AST表达式中该类型出现的频率。对于包含多个语句的节点，我们合并这些语句的AST表达式，计算每个AST类型的数量，最后构建向量。具体如下图所示针对第九行代码：  
![图 1](../images/7bd8673c5e29c839eab8f30ad0dc3b4c23718d633da8d7055cc2b87145c7522d.png)  
LLVM在AST中提供了160多种类型，仅能用大向量表示，本文选top32常用类型。每个WFG由两个矩阵形式化，即P∗P表示图结构的P邻接矩阵，其中P表示节点的数量P∗32特征矩阵，其中每行表示节点的句法特征。  

本文的假设：更接近根的代码贡献更大，赋予更大的权重（分别计算图节点和行节点的权重做综合）

- $W_a=NW_k*argmax(LW_j),j\in n_k$
- Node：$NW_k=NW_0*D^{k-1}$
- Line：$LW_k=LW_0*D^{k-1}$
- D为衰减矩阵；
- 本文设置$LW_0=1,NW_0=1,D=0.85$

获取的重复子图CFG的消除：

1. 如果它们位于不同的根节点，则这两个子图在结构上不同；
2. 否则，考虑节点属性不同，只使用一条线来分割图形：
   1. 通过这一行中匹配关键字的TF*DF值的汇总来计算每一行的权重；
   2. 选择具有最大权重的线；
   3. 如果多条线具有相同的权重，则随机选择一条线作为根线；

### 图相似算法

使用Genius中提出的方法，该方法利用二分图匹配来计算两个属性控制流图（ACFG）之间的相似度；  
本文中将$sim(N_i,N_j)$替换为$W_i\times W_j\times sim(N_i,N_j)$  
利用漏洞VWFG、补丁PWFG来改进相似度计算，只有当sim（T，V）>sim（T，P）时，才认为其易受攻击。

## STEP III 训练

区别漏洞WFG、补丁WFG和测试WFG

## RESULT

![图 2](../images/135430594d15f2a321334362c0617cc6d627a77283b5e4db1f74c9123972ee0c.png)  

# VulDeeLocator

解决的问题：跨文件、函数，宏的忽略，精确的定位

定义一：sSyVC是一串符合漏洞模板的（标识符、运算符、常量和关键字）的连续token；
定义二：iSeVC是sSyVC的中间代码表示，也即源码中间代码的slice；

## STEP I sSyVC

从AST中提取sSyVC，针对四种特征：

- API/库函数漏洞：名称与参数匹配；
- 队列定义：“[” 、“]”；
- 指针定义：“*”；
- 算数表达式：赋值,“=”，后匹配至少一个变量；

## STEP I iSeVC

1. 跨文件：用编译器（Clang）IR文件，然后根据依赖链接LR文件；
2. 跨函数：IR链接后生成CFG和DFG；
3. 通过dg等工具实现基于sSyVC的切片：
   1. 每个局部变量表示为前缀为%的数值；对于LLVM IR切片中的每个函数，第一个局部变量的数值为1，然后每个后续局部变量的值增加1（归一化局部参数）；
   2. 函数调用的插入，循环互调仅各插入一次，插入后再分配局部变量；
4. 标记为漏洞发生点行号或者0（无漏洞）；
5. 为了在捕获程序语义信息时使iSeVC独立于用户定义的函数名，函数定义名规范化；
6. 定长化：使sSyVC出现在结果向量的中间；

![picture 1](../images/25ca1789c65332a1636345108fab4400df992d7725c15eacab1e2b3948e67a70.png)  

## STEP III Training

标准BRNN的输出可以映射回易受攻击的令牌，从而映射到中间代码的易受攻击行（即，多个连续易受攻击令牌）。无法实现粒度细化、注意力机制；

![picture 3](../images/3b86fe6541dafddf325ad06c413a179aafb3371c3d70f9d51c7c6ee9b5790259.png)  

本文使用针对性网络BRNN-vdl：

1. 输入：
   1. 表示iSeVC的向量；
   2. 表示每个向量中漏洞位置的漏洞位置矩阵；
2. 用多层实现注意力机制，用以剔除漏洞代码中包含的无漏洞代码行造成的误报特征（iSeVC向量*漏洞位置对角矩阵，有漏洞的例子漏洞范围内为1，无漏洞的例子均为1z）：
   1. 对于易受攻击的iSeVC，乘法层用于选择与***易受攻击代码行***相对应的令牌的输出。（这些选定的输出将用于BRNN vdl的后续层和反向传播过程，因为它们将有助于以更高的精度（比不使用此乘法层）定位漏洞）
   2. 对于不易受攻击的iSeVC，乘法层旨在选择令牌的***所有输出***（在后续层和BRNN vdl的反向传播过程中使用它们，因为就学习阶段而言，这些令牌同样重要）
3. k个最大元素的均值，来实现池化；

![picture 2](../images/84d1098e465fe4f1d674f056a4aadc0a459682ac2b24ca686ce22deed7781611.png)  

# SySeVR

是VulDeePecker的同作者后续研究
针对C、C++的，基于SyVC的slice切片的，使用BGRU的vuldeepecker；
Syntax-based Vulnerability Candidates (SyVCs)
Semantics-based Vulnerability Candidates (SeVCs)

SySeVR:Syntax-based and Semantics-based vector representation；  
![picture 4](../images/723b01fba86a8927db378486debcd86c4350a34006579a427cc390c9fb40f4d5.png)  

## STEP I SyVC获取

使用程序的抽象语法树（AST）上节点的属性来描述漏洞语法特征；

定义：

- P 程序；
- f 函数：$P={f_1,...,f_n}$无序集；
- s statement 语句：$f=[s_1,...,s_n]$有序集；
- t token：$s=[t_1,...,t_n]$有序集；
- e 代码元素，是在一个s范围内的一串连续的t；

SyVC是匹配$h_k$漏洞模板的e（由于基于不同的漏洞模板，因此同一个e也会被多次提取），对应于：

- AST的叶节点：一个token；
- AST内部节点：一条语句s或由多个连续令牌t组成；

模板在本文中包含：

1. API/库调用；
2. 数组使用；
3. 指针使用；
4. 算数表达式；

## STEP II SyVCs 转换为 SeVCs

1. 生成PDG，在CFG的基础上，研究PDG，同时考略data dependency以及control dependency；
2. 同时进行上下文切片：
   1. foward slice：从SyVC的e出发的可达各节点，根据是否包含func call可以进行细分；
   2. backward slice：从该节点出发可达SyVC的e的节点集合，根据是否包含func call可以进行细分；
   3. program slice： merge fs和bs，删除重复点和重复邻居；
   4. 值得一提的是，文中为了获得SyVC的前向切片，我们仅利用数据依赖性，原因有两个：
      1. 受SyVC通过控制依赖性影响的语句在大多数情况下不会受到攻击；
      2. 利用对SyVC具有控制依赖性的语句将涉及许多与漏洞无关的语句；
3. 生成SeVC，将ps中的statement还原并按与语句原顺序拼接；

## STEP III embedding

1. 归一化；
2. 词划分；
3. 嵌入拼接与居中定长补充或切割；（word2vec在深度学习中更为有效）

## STEP IV training

BGRU其实相对BLSTM仅有少量的优势，需要考虑样本和调参等问题，因此其优势待研究；  
![picture 5](../images/f319137379e751460b2c2047646f9df6d3747bae3e72ff215cb4a33b2f65b062.png)  

# DeepWukong

是一个基于PDG（CPG+DPG）的上下文code gadget获取，从而获取

1. 以边为目标的结构化信息（区分CF和DF）；
2. 以节点为目标的归一化后的doc2vec的嵌入

## 控制流信息提取

节点表示语句，边表示两条语句之间的控制流或执行顺序。

1. 后向支配关系；
   1. 给定CFG上的节点X和Y（X！=Y），如果从Y到程序结束的所有路径都穿过X，则X后向支配Y；
2. 控制依赖关系，Y控制依赖于X存在以下两种可能：
   1. 存在从X到Y的有向路径P，其中P中的任何Z（不包括X和Y）由Y后支配；
   2. X不由Y后向支配；

增广后支配树（APT），其在空间和时间上与程序的大小成比例，以计z算程序的控制依赖性。

## 数据流信息提取

节点表示语句，边表示两条语句之间变量的def-use关系。

使用指令依赖于定义指令：节点X（变量v的定义）是Y（v的定义或使用）在VFG中，如果有从X开始到Y的路径P上没有v的重新定义，Y数据依赖于X；

## 敏感点切片

1. 参考SVF来自动识别系统API调用（总共1449个）
2. 使用antlr来识别算术运算符

## 节点嵌入

doc2vec，将整句的节点嵌入为一个定长向量；

## 训练

![图 3](../images/f0ac54c798feffe785f6b362d6d04386695553380aa80d9147e8fb4977c8eb5d.png)  
节点传播函数：  
![图 4](../images/8c665be5a101adef9da5ed95bfeaf1938a011b8de7b15caef552904ef24f46ee.png)  
pooling：  
$\vec{y}=\frac{F\vec{p}}{||\vec{p}||}$, $\vec{i}=top-k(\vec{y},k)$, $F=(F* tanh(\vec{y}))_{\vec{i}}$, $A' = A_{i,i}$
我们执行全局平均池和全局最大池，以增强表示的性能。 

PRL

![picture 6](../images/7cce88392cd433f3ee9cceebf3070bafb80e1e287ff896171b34e116afed3709.png)  
![picture 8](../images/cc7a6a73093dc65eb9ba32c9854974c0902527f3b68eca7dc0be4185f8a69d13.png)  

MEAN和MAX拼接，然后求和输出；

MLP

$q(lb_i)=\frac{exp(\vec{s}·lb_i)}{\sum_{lb_j\in Y}exp(\vec{s}·lb_j)}$

## datase and result

### dataset

SARD；
realworld： redis-5.0.85（一种著名的数据库系统服务器）和lua-5.346（一种广泛使用的脚本语言）。
![picture 9](../images/de2e6909aae679879454db9cb176d2dc27f4d2d442509d836e10ec996798e4df.png)  

### result

![picture 11](../images/905e25470f602c80fcf00573513113a1ce454549693b81ed2170a7329ffd28ba.png)  
![picture 12](../images/4aa2c07567d1ef874b62237f60ca3e1bfb2644a5d799a41e40b7f7c0a618758a.png)  


# AutoVAS

基于vuldeepecker，讨论切片方法、嵌入方式，使用了API敏感点和修改点；
我们使用Weiser类型（包括控制依赖性信息）和SDG-IFDS类型（包括数据依赖性和控制依赖性）作为算法类型。这项研究使用了llvm切片（GitHub，访问日期：2021d年3月），这是一种基于低级虚拟机（llvm）编译器的开源程序切片工具。

采样平衡：SMOTE（Chawla等人，2002年）、改良SMODE（Hu等人，2009年）和SMOTEENN（Li等人，2013年）；如果数据类别比率不同，则模型在选择优势类别方面的精度会提高，但使用少量数据的类别召回率会迅速降低。如果我们使用平衡技术，召回率会增加，但精度会降低。

切片方案比较：
![picture 13](../images/ae8508a81fe3a2e577acdb2e05f67ac0622d981db797d7b36250964a77189286.png)  

嵌入方案比较：  
![picture 16](../images/31c58e4600b3f3ac735be73626b86a9ecb0448e67d49628ed69b91b96151cfdf.png)  

标准化中的符号化和定长化方式造成的影响，发现定长化方案影响很小，可以忽略：  
![picture 17](../images/1a748d8d6ff0a4d26007da8b72627639bcc61adbf4439e350b6a516b0ccc7c05.png)  

模型选择表示：
![picture 18](../images/9e0864610a16f9755a74ec4b5eca53677ea9b900bee08ad511e3cebf29842935.png)  
