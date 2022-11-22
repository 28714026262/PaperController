<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-11-22 10:08:30
 * @LastEditTime: 2022-11-22 16:32:05
 * @LastEditors: Suez_kip
 * @Description: 
 * 
-->
# Combining Graph-Based Learning With Automated Data Collection for Code Vulnerability Detection

[论文链接](../AI漏洞挖掘/Graph/Combining_Graph-Based_Learning_With_Automated_Data_Collection_for_Code_Vulnerability_Detection.pdf)

- 标准GNN在具有非类型化边的单个图形表示上运行，因此无法区分控制和数据流信息。
- FUNDED扩展了GNN区分和建模多个代码关系的能力。不同的关系图编码不同的代码关系，然后使用可学习的、特定于关系的函数在关系图中传播和聚合信息来实现的。
- 基于GGNN的建模与区分多代码关系；

自动收集漏洞：

- 通过使用离线训练模型来预测哪个代码提交用于修补代码漏洞来实现这一点；
- 问题1：难以分辨修补用代码提交；需要一定人工介入；

![图 1](../images/18580ba32c43e6078a24062c52727aa1e67c31314ae0dd908a3c9b8ea1666c9f.png)  

GGNN由基于门控递归单元（GRU）的四个堆叠嵌入模型组成

预处理：

- 代码：命名方案重写变量名；
- 程序图：AST，包含

   1. 语法节点（语言语法中的非终结符，if,函数声明）
   2. 语法标记（如标识符名称和常量值）

八种额外边类型：

  1. 数据流与控制流：从PCDG提取至AST.
  2. GuardedBy: 连接AST参数的token与变量的封闭保护表达式；如if（A）{B}表达式B对应到A这个封闭守护表达式；
  3. Jump: 变量与控件依赖项连接，GuardedBy和Jump可用于描述控制流；
  4. 计算源于: v=expression；
  5. 下一token: 每个语法标记连接到其后续节点；
  6. 上次使用与上次词典使用: 对同一个变量的上次操作/上一次statement操作，可以刻画数据流

- 用邻接矩阵来记录每个关系图的边缘连接，还添加了各自的后向边（通过调换邻接矩阵）

word2vec处理节点未定长向量；
