<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-10-18 19:43:22
 * @LastEditTime: 2022-10-26 14:55:40
 * @LastEditors: Suez_kip
 * @Description: 
-->

# 漏洞检测

***PAPER SOURCE：Software Vulnerability Detection Using Deep Neural Networks: A Survey***  
  
代码分析技术是漏洞检测的基础，可以分为静态、动态和混合方法。

## 静态技术

基于规则模板的分析、代码相似性检测和符号执行，主要依赖于对源代码的分析，但往往存在较高的误报率。

## AI

### 基本介绍

使用模式识别和机器学习（ML）的数据驱动漏洞发现，
具有显著提高泛化水平的潜力。
现有的基于ML的方法主要操作源代码，有高可读性。
研究人员应用了基于源代码的功能（潜在脆弱文件或代码片段的指标）：

- 导入（例如头文件）
- 函数调用
- 软件复杂性度量
- 代码更改

从版本控制系统获得的特性和信息：

- 代码提交
- 开发人员活动  
  
**任务目标**：缩小语义鸿沟（语义鸿沟是指从业者可以理解的漏洞抽象语义与ML算法可以学习的获得语义之间缺乏一致性）  
  
### 传统ML

专家定义特征取决于人类经验、专业知识水平和领域知识的深度，特征工程过程可能很耗时，并且可能容易出错。如早期根据最佳编程实践提取规则模板&抽象语法树（AST）和控制流图（CFG）；系统从特征集中学习到的内容也可能受到各种因素的影响（例如，模型的表达能力、数据过拟合、数据中的噪声等）  

**解决方案：**  
1)基于软件度量的方法;使用度量的漏洞检测模型建立在这样一个假设上:复杂的代码对于从业者来说很难理解，因此很难维护和测试。作为漏洞检测指标的代码流失指标意味着频繁修改的代码往往是错误的，因此更有可能是有缺陷的和可能是脆弱的；  
显然存在较大的假阳性概率，因此后续研究者会从源代码上下文中提取代码模式，使用词袋技术（bag-of-words based on N-gram），来仅仅统计术语、关联令牌等代码特征共出现的计数，但不能保留代码的长期上下文依赖性；  
相较于上述扁平化代码分析，现在会使用高纬度特征集，这些特征集是从静态分析生成的不同形式的程序表示中提取出来的，包括ast、cfg、数据流图(dgs)、程序依赖图(PDGs)等。将AST、CFG和PDG组合成一种称为代码属性图(CPG)的联合表征，而从动态分析中获得的程序执行轨迹也被用作特征；  
2)基于脆弱代码模式与3)基于异常：  
脆弱的代码模式是偏离正确和正常的代码模式的异常模式，异常状态包括：***异常API使用模式[6]、导入和函数调用[73]以及API符号缺失检查***
导致许多假阳性或只适用于特定任务的应用程序

### 新兴ML

抽象和高度非线性模式的学习，能够捕获复杂数据的内在结构。自动提取特征，并且具有多个抽象级别，并且可能具有更高的泛化级别以及发现未考虑过的潜在特征；该类方案目标是使基于ML的检测系统最终能够像人类一样学习和理解易受攻击的代码语义，用以进一步减少语义差距。  
如RNN，将长短期记忆(LSTM)网络与密集层结合起来，用于学习函数级表示作为高级特征，实现注意层以学习特征重要性，并添加外部内存“插槽”以捕获远程代码依赖；  

#### 常见架构类型

*FCN*  
    FCN也被称为多层感知器（MLP），与随机森林、支持向量机(SVM)和C4.5等传统的ML算法相比，FCN能够拟合高度非线性和抽象的模式，通用逼近定理[23]所支持的，一个具有单一隐层和有限数量神经元的FCN可以近似任何连续函数。FCN的另一个优点是它是“输入结构不可知的”，这意味着网络可以采用多种形式的输入数据；  

*CNN*  
    在文本分类任务中，应用于上下文窗口(即包含少量单词嵌入)的CNN过滤器可以将上下文窗口中的单词投影到上下文特征空间中的局部上下文特征向量上，其中语义相似的单词向量非常接近。  

*RNN*  
    ![图 2](images/0097230d823dbfc35731cb14c74000187a55c76ceb692ae0344c3aad42976d1b.png)  
    ![图 3](images/be71d363d49f35030983b65f0943ec844b2bdaad5c4182bed5a71ee0383116b3.png)  
    双向形式的rnn能够捕获序列的长期依赖性。许多研究利用双向LSTM (Bi-LSTM)和门通循环单元(GRU)结构来学习代码上下文依赖关系，这对于理解许多类型漏洞(例如缓冲区溢出漏洞)的语义至关重要。

*Other*  
    一些网络结构不适合上述类型，如深度信念网络(DBN)和变分自编码器(VAEs)；  
-DBN：  
    假设有一个二部图，每一层的节点之间没有链接，一层是可视层，即输入数据层（v)，一层是隐藏层(h)，如果假设所有的节点都是随机二值变量节点（只能取0或者1值），同时假设全概率分布p(v,h)满足Boltzmann 分布，我们称这个模型是Restricted BoltzmannMachine (RBM)。在已知v的情况下，所有的隐藏节点之间是条件独立的，同理所有的可视节点都是条件独立的，所有的v和h满足Boltzmann 分布；我们把隐藏层的层数增加，我们可以得到Deep Boltzmann Machine(DBM)；  
    ![图 5](images/7f99fb00439dd94f2939f56a3bcdd8decc10a0b65896510b05cdc1ed8674430e.png)  
    ![图 6](images/6c8bdcec7909a849c6eb53c3add6071b44b6e2d561882fc2b6a6397ab6dee18e.png)  

-VAEs：
    ![图 7](images/f37d3523afe1d4da9947ade6be47e1bf1c71e2ea372b9afeb2b04b4a001c0503.png)  

-记忆网络：  
    该网络配备了外部内存“插槽”，用于存储之前引入的信息，以供未来访问。与LSTM结构相比，该网络能够捕获更远距离的序列相关性;因此，它增强了捕获范围更广的代码序列的能力，这些代码序列是识别依赖于上下文的缓冲区溢出漏洞的关键；  

#### 研究现状

- 基于图的特征表示:大量研究应用dnn从不同类型的基于图的程序表示中学习特征表示，包括AST、DFG、CFG、PDG和它们的组合。  
- 基于序列的特征表示:这类研究利用dnn从序列代码实体中提取特征表示，如执行跟踪、函数调用序列和变量流/序列。  
- 基于文本的特征表示:对于这类作品，特征表示直接从代码的表面文本中学习。  
- 混合特征表示:这一类包括最近结合上述三种类型的特征表示的研究。  
  
***Target：***  

- 如何处理软件代码以生成特征表示->促进DNN对代码语义的理解，并将模式捕获为潜在脆弱代码片段的指示器；  
  
- DNN模型用作具有内置表示学习能力的分类器;  

##### 基于图的特征表示

包括AST、CFG、PDG和数据依赖图（DDG）作为DNN的输入；  

一个针对语句级检测的细粒度解决方案，针对PHP的web应用程序的SQL注入（SQLI）和跨站点脚本（XSS）漏洞。他们提出了一组静态代码属性，用于描述CFG（生成输入）和DDG（定位执行输入净化）中的杀毒代码模式；输入以20-D特征向量描述消毒模式，以C4.5、朴素贝叶斯（NB（追求最高概率））FCN作为分类器进行训练和分类，其中FCN在数据集上优于其他两种传统的ML分类器。  
***PAPER SOURCE：L . K . S h a r a n d H . B . K . T a n , “ P r e d i c t i n g S Q L injection and cross site scripting vulnerabilities through mining input sanitization patterns,” Inf. Softw. T echnol., vol. 55, no. 10, pp. 1767–1780, Oct. 2013.***：  

利用AST学习神经表示来检测Java源代码。AST包含了3种类型的节点 ***（1）函数调用和类实例创建的节点；（2）声明节点；（3）控制流节点。***  
之后，将节点转换为token seq，特定于项目的标记被通用名称替换，例如方法声明/调用。应用距离相似度计算算法从数据中去除噪声。之后使用k最近邻算法计算距离。如果某个实例的标签与其相邻实例的标签相反，则该实例将作为杂讯被删除。最后，通过使用一对一映射表将剩余的令牌序列标记化，以将每个令牌映射为一个整数，从而将序列用作DBN的输入。  
作者将样本馈送到经过训练的DBN，以自动生成高级特征表示，然后将其用于训练常规ML算法，如ADTree、NB和逻辑回归（LR）；作者从PROMISE3缺陷库中选择了Java项目，并将他们提出的方法与两个不同的特征集进行了比较：1）软件度量和2）AST。DBN生成的基于AST的特征在所有选定的项目中都取得了最佳性能。  
绩效评估显示，在22个跨项目场景中的17个场景中，基于DBN的方法在F1得分方面优于TCA+。  
***PAPER SOURCE：S. Wang, T . Liu, and L. Tan, “ Automatically learning semantic features for defect prediction,” in Proc. 38th Int. Conf. Softw. Eng. (ICSE), 2016, pp. 297–308.***  

基于AST的方法应用Bi-LSTM网络学习跨项目漏洞发现的特征表示。他使用自动生成的软件复杂度替代实际标签，从源代码函数的AST中提取了原始特征，使用了***CodeSensor***（能够在没有AST提取工作构建环境的情况下获得AST），使用深度优先遍历（DFT）将AST转换为序列。  
将AST序列模糊化（标记与项目无关）并整数化，并映射到64维嵌入向量以便剩下的，该网络由两个Bi-LSTM层组成，用于从嵌入的AST序列学习上下文信息和两个全连接层；**开源项目FFmpeg和LibTIFF作为训练集，LibPNG作为实验测试集**  
考虑到表示没有提供标签信息，使用代码复杂度度量来代替实际标签or通过从历史软件项目的漏洞数据中学习可转换表示；  
***PAPER SOURCE：G. Lin, J. Zhang, W . Luo, L. Pan, and Y . Xiang, “POSTER: Vulnerability discovery with function representation learning from unlabeled projects,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur ., Oct. 2017, pp. 2539–2541.***  

相较于Paper60他们将Word2vec[67]与连续词袋（CBOW）模型结合起来，将序列的每个元素转换为100维的嵌入，以恢复代码语义信息；他们提出的网络仅包括一个用于学习AST序列上下文信息的Bi-LSTM层，然后是一个全局最大池层和两个完全连接的层。全局最大池层的功能类似于CNN结构中的最大池层，**资源为CVE，国家脆弱性数据库NVD**  
***PAPER：SOURCE：G. Lin et al., “Cross-project transfer representation learning for vulnerable function discovery ,” IEEE Trans. Ind. Informat., vol. 14, no. 7, pp. 3289–3297, Jul. 2018.***  

基于序列对序列（seq2seq）LSTM网络对Java源代码检测，AST->seq构建查找表，将每个token映射到一个固定长度的向量用于（seq2seq）LSTM网络,网络能够学习令牌序列的关系。  
为了生成顺序结构的语法特征，作者将序列嵌入馈送到网络，并将均值池应用到网络的输出，状态聚合同一序列中的令牌输出功能向量，将功能级向量组合成文件向量。  
word vec->pooling->function vec->combine->file vec  
作者为提高泛化性总结了所有令牌状态（即语义空间），用于执行跨项目检测。使用k-means对训练集中的所有状态向量进行聚类，获得令牌的状态。算了文件中所有状态向量与每个簇的最近质心之间的距离，以生成该文件的特征向量。
***PAPER SOURCE：H . K . D a m , T . T r a n , T . P h a m , S . W . N g , J . G r u n d y , and A. Ghose, “ Automatic feature learning for vulnerability prediction,” 2017, arXiv:1708.02368. [Online]. Available: <http://arxiv> .org/abs/1708.02368***  

使用基于语法的脆弱性候选（SyVC），作者需要将其转换为基于语义的脆弱性候选人（SeVC），以容纳与SyVC语义相关的语句并转化为CFG-程序切片技术->DFG->PDG  
SyVC与向量的描述语句编码->word2vec固定长度；**数据来源NVD、SARD**
对CNN、DBN、LSTM、GRU和Bi-GRU进行检测，Bi-GRU上表现最好，DBN上表现最差；
先进的漏洞检测系统进行了比较，包括**Flawfinder、RATS、Checkmarx、VUDDY和VulDeePecker**
***PAPER　SOURCE：G. Grieco, G. L. Grinblat, L. Uzal, S. Rawat, J. Feist, and L. Mounier , “Toward large-scale vulnerability discovery using machine learning,” in Proc. 6th ACM Conf. Data Appl. Secur . Privacy (CODASPY), 2016, pp. 85–96***  

***总结***  
AST可以成为不同类型的神经模型学习与潜在脆弱模式相关的特征表示的有用来源；  
AST与其他形式的基于图形的程序表示（如CFG、PDG或DDG）进行比较、  
哪种程序表示可以使神经模型学习更有效的代码语义
研究并没有使用原始树形图进行处理，而是在将它们送入深层网络之前将其“展平”  

##### 序列特征表示  

基于序列的特征表示:这类研究利用dnn从序列代码实体中提取特征表示，如执行跟踪、函数调用序列和变量流/序列：  
  
***现有工作：***  
  
动静态提取轻量级特征，假设分析调用序列/跟踪可以揭示C库函数的使用模式（如存在内存损坏漏洞）以c库提取的静态特征（反汇编二进制文件）进行操作
动态：有限时间的执行与获取->动态调用序列包含大量函数调用的参数（低级计算值）要求进行子分类以减少类型量。N-gram语言模型和Word2vec将文本序列转换为有意义的向量表示，输入三个分类器：LR、FCN和随机森林，用于训练、验证和测试。  
***PAPER SOURCE：G. Grieco, G. L. Grinblat, L. Uzal, S. Rawat, J. Feist, and L. Mounier , “Toward large-scale vulnerability discovery using machine learning,” in Proc. 6th ACM Conf. Data Appl. Secur . Privacy (CODASPY), 2016, pp. 85–96.***  

比较不同类型DNN在从动态函数调用序列提取的特征集上的性能：
-CNN网络
-仅包含一个LSTM层的LSTM网络
-分别具有一个卷积层和一个LSTM-层的CNN-LSTM网络
-具有两个隐藏层的FCN
基于允许程序在有限的时间段内执行来获得C标准库函数调用序列，提取函数的参数子类型来减少参数类型的多样性，使用**Keras**提供的标记化工具，将函数调用序列转换为数字，为了将输入序列馈送到网络，添加了一个嵌入层作为三个网络的第一层；  
LSTM网络的误报率最低（19%），CNN-LSTM网络在F-Score方面优于其他网络，为83.3%。  
***PAPER SOURCE：F . Wu, J. Wang, J. Liu, and W . Wang, “Vulnerability detection with deep learning,” in Proc. 3rd IEEE Int. Conf. Comput. Commun. (ICCC), Dec. 2017, pp. 1298–1302.***  
  
针对缓冲区错误和资源管理错误漏洞；代码段语义上相互关联，形成一系列描述变量流和数据依赖性的语句；关系定义：数据依赖或控制依赖。**Checkmarx**的商业工具用于提取与数据流或控制流相关的库/API调用和相应的程序切片，程序切片转换为令牌序列，并应用Word2vec将其转换为固定长度的向量表示。
code gadget-只能基于商业提取工具
***PAPER SOURCE：Z. Li et al., “Vuldeepecker: A deep learning-based system for vulnerability detection,” in Proc. NDSS, 2018, pp. 1–15*** with github code  

在paper56的基础上，提出了代码关注，关注语句中的本地化信息，如特定库或API调用中的参数。该架构有两个具有相同设置但规模不同的深度Bi-LSTM网络。最终，他们使用了一个合并层来融合全局和局部特征。融合的特征表示被传递到另一个Bi-LSTM层，然后是softmax层用于分类。该作者**扩展了Li发布的数据集**  
***PAPER SOURCE：D. Zou, S. Wang, S. Xu, Z. Li, and H. Jin, “µVulDeePecker: A deep learning-based system for multiclass vulnerability detection,” IEEE Trans. Dependable Secure Comput., early access, Sep. 23, 2019, doi: 10.1109/TDSC.2019.2942930.*** with github code  

包含更多信息的code gadget  
***PAPER SOURCE：Z . L i , D . Z o u , S . X u , H . J i n , Y . Z h u , a n d Z . C h e n , “SySe VR: A framework for using deep learning to detect software vulnerabilities,” 2018, arXiv:1807.06756. [Online]. Available: <http://arxiv> .org/abs/1807.06756***  

##### 基于文本的特征表示

代码文本指的是源代码的表面文本、汇编指令和代码词法器处理的源代码。  
假设可以通过挖掘源代码令牌的频率来识别易受攻击的模式。  
当使用N＞2的N-gram模型时，为了处理所得特征向量的高维性，他们通过应用Wilcoxon秩和来过滤不相关的特征  
***PAPER SOURCE：F . Wilcoxon, “Individual comparisons by ranking methods,” Biometrics Bull., v o l . 1 , n o . 6 , pp. 80–83, Dec. 1945***  

基于Word2vec实现的Instruction2vec。汇编代码操作码、寄存器、指针值和库函数映射到相应的九个值（一个操作码和两个操作数，每个操作数包含四个值）的固定长度密集向量，生成汇编代码的查找表。将代码转换为为9mn维向量（其中m是由Word2vec模型确定的嵌入维数，n条指令组成的汇编代码）
测试 **Juliet测试套件**
**Paper46**的一个卷积层和九种不同类型的滤波器、两个卷积层层和32个3×3滤波器和64个3×3滤波器，46+54效果较好；
***PAPER SOURCE：Y . J. Lee, S.-H. Choi, C. Kim, S.-H. Lim, and K.-W . Park, “Learning binary code with deep learning to detect software weakness,” in Proc. KSII 9th Int. Conf. Internet Symp. (ICONI), 2017.***  
  
将CNN应用于功能级漏洞检测**Juliet测试套件**、等c、c++代码  
最小化标记词汇表的大小（去除关键字、运算符和分隔之外不影响编译的）只使用了156个标记；转换为k-vec；  
框架使用：**Paper46**中提出的CNN结构，具有一个卷积层和一个两层GRU网络，然后是最大池层。作者将训练和测试数据输入训练网络，并获得两个网络的最大池层的输出作为学习特征，称为神经表示，神经表示被用作输入到随机森林分类器；  
最大散度顺序自动编码器（MDSAE）；它建立在VAE的基础上，用于自动学习机器指令序列的表示，以检测二进制级别的漏洞。对每一类（脆弱类和非脆弱类）应用了两个可学习的（非固定的）高斯先验，并在分发之前将潜在空间中的代码拟合到数据中。两个先验之间的分歧[例如，Wasserstein（WS）距离或Kullback–Leibler（KL）分歧]被最大化，以分离脆弱和非脆弱类的表征。  
可以作为特征提取器生成表示为用于分类任务的另一独立分类器（例如SVM或随机森林）的特征，或者，该网络可以与浅FCN合并，并同时训练为分类器。
**汇编数据集paper56** ***需要进一步理解***  
***PAPER SOURCE：R. Russell et al., “ Automated vulnerability detection in source code using deep representation learning,” in Proc. 17th IEEE Int. Conf. Mach. Learn. Appl. (ICMLA), Dec. 2018, pp. 757–762.***  
  
Capstone二进制反汇编框架用于将二进制代码转换为更具有语义意义的汇编代码。  
删除冗余前缀，并保留操作码和指令信息（例如，内存位置、寄存器）构建了两个词汇表，分别嵌入操作码和指令信息，将其转换为one hot向量，并将*操作码的one hot矢量与相应的嵌入矩阵相乘*，将指令信息视为一个十六进制字节序列，并以此为基础构造频率向量。指令信息的矢量表示可以通过*频率矢量和对应的嵌入矩阵*的乘法获得。最后，指令的向量表示可以通过将*操作码和指令信息的向量级联*来生成。  
高于以下五个五个基线系统评估：  
-一个用于学习表示的RNN和一个线性分类器，该线性分类器基于所得到的表示进行训练，用于对脆弱和非脆弱功能进行分类；
-具有放置在最后隐藏单元顶部的线性分类器的RNN；
-段落到矢量分布相似性模型*Paper51*；
-顺序VAE；
-*Paper56*中开发的方法。  
***PAPER SOURCE：D. Bahdanau, K. Cho, and Y . Bengio, “Neural machine translation by jointly learning to align and translate,” 2014, arXiv:1409.0473. [ O n l i n e ] . Available: <http://arxiv.org/abs/1409.0473>***  

DBN和FCN的分层结构能够学习高级表示。他们还证明了CNN和RNN的变体（如LSTM网络）能够从文本语料库（如源代码或AST序列）中捕获上下文模式或结构。他们应用记忆网络来跟踪数字语句中不同变量值的变化；  
**Target**  
监控对多个变量的值变化不仅要求网络理解代码的结构，而且网络还应具有记忆变量及其相应值以及对其所做更改的能力。  
传统的RNN结构（即LSTM和GRU）无法准确地记忆长序列（例如，段落或功能体）  
额外构建存储块的网络（神经训练机[34]、存储网络）被使用于保留NLP任务（如问答）的超长序列。

内存网络；源代码作为输入，一行中的每个代码标记都由一个V维one hot向量编码，其中V是数据集中所有程序中唯一标记的词汇表大小。零填充空白至一个内存插槽可以存储的最大行数，d维向量表示每个标记，并使用嵌入矩阵（E− val），位置编码来编码每行中标记的位置
编码行分配给内存插槽，包括代码行内容、代码行的位置  每行内容的Eval和位置信息的Eaddr  
Eaddr矢量查询 查询嵌入和内存地址块的每个时隙之间的内积应用注意机制，关注向量表示每条线与查询的关联程度。关注向量与时隙相乘->响应向量 查看该线内是否存在响应信息，以获取高关注度  
响应向量应用到权重矩阵以生成输出\查询嵌入将用于计算关注向量并最终计算响应向量
CNN在所有级别的样本上都表现不佳。LSTM网络在简单样本上取得了相当的性能，但在较高级别样本上，其性能显著下降，而内存网络性能相对稳定。
缺点：合成代码在语法上是无效、无法编译代码、无控制流、不能反映真实的场景；  
***PAPER SOURCE：M.-J. Choi, S. Jeong, H. Oh, and J. Choo, “End-to-end prediction of buffer overruns from raw source code via neural memory networks,” 2017, arXiv:1703.02458. [Online]. Available: <http://arxiv.org/abs/1703.02458>***  
  
现实的代码数据集（称为s-bAbI）-》非平凡控制流结构的语法准确的C程序  
含六种不同类型的标签，标签在行级别提供。  
行号  
0.3的Dropout  
网络结构和嵌入方法沿用paper18  
随机抽样技术，每个标签的查询行数相等
声音数据集、**Frama-c代码分析工具**、Juliet测试套件无法收敛  
***PAPER SOURCE：C. D. Sestili, W . S. Snavely , and N. M. VanHoudnos, “Towards security defect prediction with AI,” 2018, arXiv:1808.09897. [ O n l i n e ] . Available: <http://arxiv.org/abs/1808.09897>***  

##### 混合型

Android APK反编译-》dalvik指令包的smali文件  
dalvik指令包dalvik指令的频率表示的令牌特征
smali文件-》AST生成的语义特征  
分为八类，并构建了映射表  
AST ->DFS-> 序列-结合-语义特征向量-》特征向量
深度FCN优于SVM、NB、C4.5和LR  
***PAPER SOURCE：F . D o n g , J . W a n g , Q . L i , G . X u , a n d S . Z h a n g , “Defect prediction in Android binary executables using deep neural network,” Wireless Pers. Commun., vol. 102, no. 3, pp. 2261–2285, Oct. 2018.***  
  
基于两组漏洞检测特征：  
基于源代码的特征、Clang和低级虚拟机（LLVM）生成的CFG中派生的基于构建的特征
源代码函数转换为token序列，但单个函数中的每个唯一变量名都被分配了一个单独的索引  
单词袋模型和Word2vec模型-》令牌序列：  
指令级的功能级CFG和基本块中提取了特征：操作以及变量的定义和使用（use-def矩阵）；
特征集包含邻接矩阵和opvec\use-ef向量-平均运算来适应CFG的邻接矩阵和op-vec\use-def向量-》固定大小向量  
基于源特征的模型取得了更好的性能。CNN+树模型分类
***PAPER SOURCE：J. A. Harer et al., “ Automated software vulnerability detection with machine learning,” 2018, arXiv:1803.04497. [Online]. Available: <http://arxiv.org/abs/1803.04497>***
  
两个Bi-LSTM网络应用于学习SARD项目和真实世界漏洞数据源的潜在表示；
使用真实世界样本中提取的AST&合成样本的源代码，用于弥合差异
各自网络中单独训练后，将标记数据馈送到两个经过训练的Bi-LSTM网络获得两组高级表示-》连接以形成聚集特征集-》常规ML分类器
应用于**FFmpeg、LibTIFF和LibPNG**较有优势  
***PAPER SOURCE：G. Lin et al., “Software vulnerability discovery via learning multi-domain knowledge bases,” IEEE Trans. Dependable Secure Comput., early access, Nov . 19, 2019, doi: 10.1109/TDSC.2019.2954088.***  
  
使用单一类型的特征表示相比，组合不同类型的特征表达可以提高检测性能。

#### 展望

-无标准基准数据集  
**PAPER G . L i n , W . X i a o , J . Z h a n g , a n d Y . X i a n g , “ D e e p learning-based vulnerable**  
提到9个用C编程语言编写的开源软件项目、提供了功能级别和文件级别的标签
1400个易受攻击的函数和1300个易受到攻击的文件 **少**
**SAMATE**包括*juliet、SARD*、IARPAd的STONESOUP、静态工具测试集SATE  
缺少来自真实软件项目的标记代码示例

-代码分析和神经学习  
网络模型正变得越来越复杂，表现力也越来越强、
网络模型正变得越来越复杂，代码分析工作减少  
![图 1](images/116ee1fac948ff3b94150e6d265e15f78597cea965273011c40757672cd78e67.png)  
定义不明确的特征要求表达模型从头开始学习，而开发适合感兴趣任务的表达模型也是一项挑战

-语义保留  
1）神经网络语义保留  
记忆网络、生成性对抗网络  
NLP：自我注意机制的Transformer神经网络架构、
Word2vec和Bi-LSTM
2）基于树的神经网络应用于漏洞检测-》解决扁平问题
树结构LSTM（TS-LSTM）、递归神经网络、图神经网络（如图卷积网络（GCN）和图自动编码器（GAE））
**代码存储库的提交消息、对一段代码进行描述/解释的注释以及代码评审注释**github可以使用的信息

-语义鸿沟  
特征工程+高质量的特征较少依赖于复杂的表达模型（需大量训练）-》定义反映特定类型漏洞特征的特征集
-》针对性的56、121√  
嵌入技术-》表示\描述漏洞的特征：  
基于频率的（例如，n-gram模型（有限词））和基于预测的（例如Word2vec模型（无法捕获目标单词与其上下文之间相互依存的意义））单词嵌入解决方案

-人类理解
LIME10被提议通过在预测样本周围局部学习简单且可解释的模型（例如，线性或决策树模型）来为任何模型提供可解释性（特征提取器时不可用）**M. T . Ribeiro, S. Singh, and C. Guestrin, “‘Why should I trust you?’: Explaining the predictions of any classifier,” in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, Aug. 2016, pp. 1135–1144.**
注意机制： 网络关注部分输入（例如，图像或文本序列）
绘制关注部分（例如，**注意力权重矩阵**）-》可解释性  
注意力网络可以了解每个路径上下文应该受到多少关注，已经被应用于缺陷测试；

-误报，需要手动进行进一步检查  

## 动态测试

包括模糊测试和污点分析，通常存在代码覆盖率低的问题。

## 混合方法

结合了静态和动态分析技术，旨在克服上述缺点。

## 元学习

## 附录  

***AST***：abstract syntax tree  
***CFG***：control flow graph  
***CDG***：Control Dependence Graphs  
***DDG***：Data Dependence Graphs  
***PDG***：Program Dependence graphs  
***CPG***：Code Property Graphs
***LR***：逻辑回归模型(Logistic regression)，又称对数几率模型
***随机森林***：属于 集成学习 中的 Bagging（Bootstrap AGgregation 的简称）方法。随机森林是由很多决策树构成的，不同决策树之间没有关联。输入样本进入，就让森林中的每一棵决策树分别进行判断和分类，每个决策树会得到一个自己的分类结果，决策树的分类结果中哪一个分类最多，那么随机森林就会把这个结果当做最终的结果。  
![图解随机森林](https://easyai.tech/wp-content/uploads/2022/08/7a9cf-2019-08-21-Random-Forest.png)

## 目标论文  

46 CNN架构  
56 Code gadget  
86 87 word2vec  
12 juliet套件  
47 VAE  
MDSAE  
34 神经训练机  
100 112 存储网络  
99 位置编码  
31；98 Dropout  
F1得分  
SVM、NB、C4.5和LR  
50 CFG中派生的基于构建的特征  
*vuldeepecker

# 黑盒逻辑漏洞检测

待更新
