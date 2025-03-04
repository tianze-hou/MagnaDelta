# MagnaDelta
MagnaDelta​ 是一个基于格式化中文 Markdown 文件的法律条文对比生成器。它能够解析两个格式化的 Markdown 文件，逐条对比法律条文，并生成一个详细的对比表格，展示新旧版本之间的差异。MagnaDelta 适用于法律文档的修订记录和变更分析，为法律工作者、爱好者和悉心关注法治建设的社会公众提供参考。

## 功能特性
- ​解析格式化 Markdown 文件：支持解析包含章节、节和条文的 Markdown 文件。
- 自动匹配，逐条对比：通过智能匹配算法，自动找到新旧版本中对应的条文，并生成对比结果——**即使条文顺序发生改变，也可以准确匹配**。
- 差异标记：使用删除线和下划线标记出条文内容的增减，清晰展示变更。
- 生成对比表格：将对比结果输出为 Markdown 格式的表格，便于查看和分享。  

## 功能示例
### 输入文件格式
输入md文件基于我国法律条文标准格式，增加一些Markdown标记，格式要求如下：

1. 章标题：使用md一级标题；
2. 节标题：使用md二级标题；
3. 条文：每一个条文以`“第x条”`开始，其中`x`为中文数字，每个条文可以包含多行。

形如：

```
# 第一章　章标题

## 第一节　节标题

第一条　条的内容第一行

条的内容可能会有第二行

第三行，都有可能

第二条　从这里开始才是第二条

```

### 输出文件示例
<img width="671" alt="截屏2025-03-03 下午1 06 55" src="https://github.com/user-attachments/assets/f6ec6dd0-3e2f-44f5-b59d-0e0047c9a114" />

## 实现原理

- **结构化解析**：使用正则表达式识别章节层级（#/##）​
- **智能匹配**：基于SequenceMatcher的相似度算法，全局匹配对应的条文，阈值控制（相似度>40%）
- **差异标注**：diff-match-patch算法，语义清理优化

## 安装与使用

### 安装

1. 克隆本仓库到本地：

   ```bash
   git clone https://github.com/tianze-hou/MagnaDelta.git
   cd MagnaDelta
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```


### 使用

1. 准备两个格式化的 Markdown 文件，分别代表旧版和新版的法律条文。确保文件格式正确。

2. 运行脚本生成对比表格：

   ```bash
   python3 main.py
   ```

3. 生成的对比表格将保存为 `comparison.md` 文件。

## Todo
- [ ] 自动格式化parser
- [ ] 多格式导出支持
- [ ] 处理“拆分”和“合并”的条目

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=tianze-hou/MagnaDelta&type=Date)](https://star-history.com/#tianze-hou/MagnaDelta&Date)
