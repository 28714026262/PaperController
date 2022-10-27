<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-10-26 14:54:55
 * @LastEditTime: 2022-10-27 20:12:15
 * @LastEditors: Suez_kip
 * @Description: 
-->

# VulDeePecker

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
