<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-12-01 20:57:24
 * @LastEditTime: 2022-12-03 15:57:38
 * @LastEditors: Suez_kip
 * @Description: 
-->
# 结合传统漏挖技术的AI

## A deep learning based static taint analysis approach for IoT software vulnerability location

Main Idea：污点分析+Bi-LSTM  
![图 2](../images/1c03a3aaed4823ea9aeab2b3d3feaf00f3970478dd13ed0519417603e12991ae.png)  

### 静态分析工作总结

- Flawfinder：内置的C/C++函数数据库进行简单的文本模式；
- RATS：提供了C、C++、Perl、PHP和Python源代码的潜在问题列表；
- 针对交互式编程环境的ITS4：无上下文解析器生成的解析树与token来表示程序并匹配；
- Checkmarx的CxSAST：多语言，搭配词汇分析技术使用CxQL专利查询技术；
- Coverity：和CI/CD系统的集成，多语言，提供深度、全路径覆盖精度；使用过程间分析；
- HP Fortify：数据流、语义、结构、控制流、配置流分析引擎，但无法有效定位漏洞的位置；
- Vulture：用于从组件级别挖掘漏洞数据库、版本存档和代码库，并将过去的漏洞映射到组件，根据新组件的导入和函数调用预测新组件的漏洞；
- Neuhaus：使用支持向量机来预测易受攻击的包；
- Yamaguchi1：在向量空间中嵌入代码，并使用机器学习自动确定API使用模式；
- Yamaguchi2：AST，基于漏洞外推的思想搜索漏洞，但它们无法自动识别漏洞；
- Grieco：ML+轻量级静态和动态特征；
- VulPecker：生成目标程序的签名，然后使用代码相似性算法检测漏洞；
- VUDDY：函数级粒度和长度过滤技术；：利用信息理论预测臭味的数学模型
- TFI-DNN：自动漏洞分类模型
- Jurn等人：二进制复杂度分析的混合引信方法，并引入了一种自动补丁技术，修改了PLT/GOT表，以将脆弱函数转换为安全函数；
- Spanos：文本分析和多目标分类技术，将脆弱性特征视为六个目标的向量；
- Aakanshi等人：利用信息理论预测臭味的数学模型（Shannon、Rényi和Tsallis熵）；
- Madhu等人：用户提交的错误和评论的摘要描述，提出了基于错误依赖性的数学模型；
![图 1](../images/ac016f6ae0eba9a3bb174c4633542b7b85a02ea310a12e6bc1e73bc4d1d70b2b.png)  

本文还总结了一些其他IOT方向的工作，不做收录；

### I diff文件获取

1. 使用difflib获取源代码和补丁代码之间的Diff文件；其中常见源代码比较工具包括：
   1. DiffMerge
   2. Textdiff
   3. Meld
   4. Gitdiff
   5. difflib

### II 污点分析

1. 根据污点选择原则标记初始污点；
   1. 基于补丁的diff文件中删除和添加的行共享的变量；
   2. 已知漏洞函数或普通函数的参数；
   3. if条件语句中的受限变量；
2. 污点权重（专家干预）（泛化性也太弱了）
   1. 如果污点是CWE-119或CWE-339漏洞相关函数的参数，则污点权重为1
   2. 如果污点是普通函数的参数，则污点权重为2；
   3. 如果污点受If语句约束，则污点权重为3；
   4. 否则，污染权重为4。
3. 基于静态污染分析和污染首次出现的行号生成污染传播路径；

### III 污点传播路径嵌入

1. 将污点传播路径转换为符号表示；
   1. 使用keras:preprocessing:text:tokenizer过滤特殊字符后进行数据分割；
   2. 基于词频生成单词分词词典；
   3. 将原始代码段中的每个单词替换为与词典对应的单词的编号；
2. 将所述符号表示编码成向量；
   1. word2vec的CBOW

### IV 基于深度学习的物联网软件漏洞定位系统

CNN-BLSTM神经网络来定位漏洞

### V 结果

DB：NVD+SARD
始终在和RNN、LSTM、BLSTM、CNN-BLSTM比较，效果有但不明显，30000+的数据集训练大约50分钟，8000文件训练30s；
在特定数据集上acc数据达到97%，但是比较的有点云里雾里，都在和CNN-BLSTM比较FP、FN；
