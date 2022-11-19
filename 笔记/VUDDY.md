<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-11-17 20:11:02
 * @LastEditTime: 2022-11-19 16:12:35
 * @LastEditors: Suez_kip
 * @Description: 
-->
# VUDDY

[论文链接](../AI漏洞挖掘/VUDDY_A_Scalable_Approach_for_Vulnerable_Code_Clone_Discovery.pdf)

函数级粒度和长度过滤技术（减少了签名比较的次数/搜索空间），实现了其极高的可扩展性。

## 相关工作

### Token级别粒度

- CCFinder 高复杂性，用后缀树算法来测量程序的token序列相似性；参数替换策略激进，多误报；
- CPMiner 使用称为CloSpan的“频繁子序列挖掘”算法比较生成的令牌序列；启发式，中等规模的代码库,复杂度$O(n^2),n=LoC$,执行时间与CCFinder类似，假阳性率高；

### 行级别粒度

- ReDeBug 由n行（默认4）组成的窗口；并对每个窗口应用三个不同的哈希函数，用bloom过滤器成员身份检查来检测文件之间的代码克隆，针对重构代码克隆，无法检测重命名代码克隆；行粒度上下文信息有限；

### 函数级别粒度

- SourcererCC 使用一套令牌策略管理变化，错误地将补丁检测为未修补代码片段的克隆；可以高效针对重构代码克隆；应用Overlap函数推断函数的相似性(共有令牌数)；SourcererCC无法区分修补的和未修补的代码片段，例如是否插入if。
- Yamaguchi 漏洞外推与扩展方法；能检测语义克隆，但消耗很高；

### 文件级粒度

- DECKARD 文件->AST->特征向量->基于欧氏距离聚类：子图同构问题为NP问题，任务消耗很高；有人指出有90%的假阳性可扩展性不足；
- FCFinder 预处理冗余信息后hash，都成文件hash的键值对；比较重叠hash

### 混合粒度

- VulPecker
