<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-10-26 14:56:24
 * @LastEditTime: 2022-10-26 16:16:24
 * @LastEditors: Suez_kip
 * @Description: 
-->

# DATA SET

## NVD  
  
NVD in NIST(National Institute of Standards and Technology)<https://nvd.nist.gov/>  
NVD中CVE信息：一个完整的CVE信息 包含 六部分：

- 元数据  
- 漏洞影响软件信息  
- 漏洞问题类型  
- 参考和漏洞介绍  
- 包含CPE信息
- 漏洞影响和评分

tips：CPE是（Common Platform Enumeration的缩写）以标准化方式为软件应用程序、操作系统及硬件命名的方法。CPE是用于信息技术系统，软件和程序包的结构化命名方案。基于统一资源标识符（URI）的通用语法，CPE包括形式名称格式，用于根据系统检查名称的方法以及用于将文本和测试绑定到名称的描述格式。

```cpe:/<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>:<sw_edition>:<target_sw>:<target_hw>:<other>```  

其中，part表示目标类型，允许的值有a（应用程序）、h（硬件平台）、o（操作系统）；vendor表示向量类型；product表示产品名称；version表示版本号；update表示更新包；edition表示版本；language表示语言项。  
具体下载地址：<https://nvd.nist.gov/vuln/data-feeds>  

## SARD  
  
SARD(Software Assurance Reference Dataset)网站主页：<https://samate.nist.gov/SRD/index.php>  
包含代码类型：Java、C、php、C++、c#；漏洞类型：150 classes of weaknesses  
具体测试套件下载地址：<https://samate.nist.gov/SARD/test-suites>  
![图 1](../images/4abf6a360ca1cb6343bcabc6621bd93269951b397ff66213f45cb6220cb9bca9.png)  

## CWE

Community-developed list of software and hardware weakness types.<https://cwe.mitre.org/>

## 其他（待研究）

1, 赛门铁克的漏洞库 <https://www.securityfocus.com/>
2, 美国国家信息安全漏洞库 <https://nvd.nist.gov/>---------
3, 全球信息安全漏洞指纹库与文件检测服务 <http://cvescan.com>
4, 美国著名安全公司Offensive Security的漏洞库 <https://www.exploit-db.com/>
5，CVE(美国国土安全资助的MITRE公司负责维护) <https://cve.mitre.org/>
工控类
1, 美国国家工控系统行业漏洞库 <https://ics-cert.us-cert.gov/advisories>
2, 中国国家工控系统行业漏洞：<http://ics.cnvd.org.cn/>
国内：
1，中国国家信息安全漏洞共享平台(由CNCERT维护): <http://www.cnvd.org.cn>
2，国家信息安全漏洞库(由中国信息安全评测中心维护)：<http://www.cnnvd.org.cn/>
3，绿盟科技-安全漏洞：<http://www.nsfocus.net/index.php?act=sec_bug>
其他：
<https://blog.csdn.net/weixin_41843972/article/details/103885572?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_utm_term~default-0-103885572-blog-109024171.pc_relevant_recovery_v2&spm=1001.2101.3001.4242.1&utm_relevant_index=3>

## 预处理（待研究）

四、软件漏洞文本预处理：  

- 去除标点符号和特殊字符

原始漏洞文本中包含很多标点符号和特殊字符，而这些元素与上下文并不存在语义上的联系，因此首先需要对文本中的所有标点符号和特殊字符进行过滤，只保留含有较多语义信息的词汇。（可以使用正则表达式去除）

- 分词并将所有字符的大写转换为小写

对漏洞文本进行分词是指将连贯的漏洞文本信息切分成一个一个的单词，即将整个漏洞文本信息转换为可以通过统计学进行统计的最小语义单元。对于英文描述的漏洞文本，分词是非常简单的，只需要通过识别文本之间的空格或者标点符号即可将整条漏洞文本划分成一个一个的单词。然后将单词中所有字母的大写形式转换为字母的小写形式。

- 词形还原

词形还原是把一个任何形式的英文单词还原为一般形式，即将英文描述中的动词根据人称不同而变化的单词转换为动词原形；将名词的复数形式转换为名词的单数形式；将动名词形式转换为动词原形等，这些词都应该属于同一类的语义相近的词。比如“attack”，“attacking”，“attacked”则可划分为同属于一个词，用词根形式“attack”表示即可。

- 停用词过滤

停用词是指在漏洞文本中频繁出现且对文本信息的内容或分类类别贡献不大甚至无贡献的词语，如常见的介词、冠词、助词、情态动词、代词以及连词等对于漏洞分类来说毫无意义，因此这类词语应该被过滤掉。同时针对漏洞文本中有些词如“information”,“security”,“vulnerability”等词对于漏洞分类来说毫无意义，因此这类词语也应该被过滤掉。  
  
本实验通过参考从网上下载的通用停用词表，并结合漏洞文本信息自身的特点构建针对漏洞分类专属的专用停用词表实现频繁无用词的过滤。（针对漏洞自身的频繁无用词的提取方法可以使用基于词频统计的方法，比如将每个单词按词频大小降序排列，然后设定一个阈值，将低于这个阈值的单词加入到专业停用词表中。）  
  
停用词的过滤可以大大消除漏洞文本中的冗余信息，减少数据的冗余性。
