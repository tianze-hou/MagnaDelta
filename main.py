import difflib
from diff_match_patch import diff_match_patch
import re

def parse_md(filename):
    """解析Markdown文件为层级结构（支持多级序号内容）"""
    structure = []
    current_chapter = None
    current_section = None
    current_article = None  # 新增当前条文跟踪
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # 优先识别章节和节
            if line.startswith('# '):
                current_chapter = {
                    'type': 'chapter',
                    'title': line[2:].strip(),
                    'sections': [],
                    'articles': []
                }
                structure.append(current_chapter)
                current_section = None
                current_article = None  # 章节变更时重置当前条文
            elif line.startswith('## '):
                current_section = {
                    'type': 'section',
                    'title': line[3:].strip(),
                    'articles': []
                }
                current_chapter['sections'].append(current_section)
                current_article = None  # 节变更时重置当前条文
            # 识别法律条文（支持中日式空格）
            elif line.startswith('第') and any(c in line for c in ['条　', '条 ']):
                # 使用正向后视断言保留"条"字
                parts = re.split(r'(?<=条)[　 ]+', line, 1)  # 修改正则表达式
                article_number = parts[0].strip()
                content = parts[1].strip() if len(parts) > 1 else ''
                
                current_article = {
                    'type': 'article',
                    'number': article_number,
                    'content': content
                }
                
                # 确定归属层级
                if current_section:
                    current_section['articles'].append(current_article)
                else:
                    current_chapter['articles'].append(current_article)
            else:
                # 将内容持续追加到当前条文
                if current_article:
                    # 保留原始换行格式
                    current_article['content'] += '\n' + line
                # 否则视为章节/节的描述内容（根据需求可选择性处理）

    return structure

def flatten_structure(structure):
    """将层级结构扁平化为序列"""
    flat = []
    for chapter in structure:
        flat.append({'type': 'chapter', 'title': chapter['title']})
        for section in chapter['sections']:
            flat.append({'type': 'section', 'title': section['title']})
            flat.extend(section['articles'])
        flat.extend(chapter.get('articles', []))
    return flat

def find_best_match(old, new_list, used):
    """找到最佳匹配的旧条文"""
    best_score = 0
    best_idx = -1
    for i, o in enumerate(new_list):
        if i in used:
            continue
        score = difflib.SequenceMatcher(None, old['content'], o['content']).ratio()
        if score > best_score and score > 0.4:
            best_score = score
            best_idx = i
    return best_idx

def mark_diff(old, new):
    """生成差异标记"""
    dmp = diff_match_patch()
    diffs = dmp.diff_main(old, new)
    dmp.diff_cleanupSemantic(diffs)
    
    result = []
    for op, text in diffs:
        if op == dmp.DIFF_DELETE:
            result.append(f"~~<font color='red'><b>{text}</b></font>~~")
        elif op == dmp.DIFF_INSERT:
            result.append(f"<u><b><font color='red'>{text}</font></b></u>")
        else:
            result.append(text)
    return ''.join(result).replace('\n', '<br/>')

def generate_comparison(new_structure, old_flat):
    """生成对比表格"""
    # 准备旧数据
    old_articles = [a for a in old_flat if a['type'] == 'article']
    used_old = set()
    table = []

    # 处理新版结构
    for item in flatten_structure(new_structure):
        if item['type'] in ['chapter', 'section']:
            # 直接添加标题行
            table.append({
                'left': item['title'],
                'right': item['title'],
                'type': item['type']
            })
        elif item['type'] == 'article':
            # 寻找旧版匹配
            matched_idx = find_best_match(item, old_articles, used_old)
            
            if matched_idx != -1:
                old_article = old_articles[matched_idx]
                used_old.add(matched_idx)
                diff_content = mark_diff(old_article['content'], item['content'])
                left = f"{old_article['number']} {old_article['content'].replace('\n', '<br/>')}"
                right = f"{item['number']} {diff_content}"
            else:
                left = "新增条文"
                right = f"<u><b><font color='red'>{item['number']} {item['content'].replace('\n', '<br/>')}</font></b></u>"
            
            table.append({
                'left': left,
                'right': right,
                'type': 'article'
            })

    # 处理被删除的旧条文
    for i, old in enumerate(old_articles):
        if i not in used_old:
            table.insert(i, {
                'left': f"{old['number']} {old['content'].replace('\n', '<br/>')}",
                'right': "删除条文",
                'type': 'article'
            })

    return table

def main():
    # 解析文件
    new_structure = parse_md('new_law.md')
    old_structure = parse_md('old_law.md')
    
    # 生成对比数据
    old_flat = flatten_structure(old_structure)
    comparison = generate_comparison(new_structure, old_flat)
    
    # 写入Markdown文件
    with open('comparison.md', 'w', encoding='utf-8') as f:
        f.write("| 旧版 | 新版 |\n")
        f.write("|------|------|\n")
        for row in comparison:
            if row['type'] in ['chapter', 'section']:
                f.write(f"| **{row['left']}** | **{row['right']}** |\n")
            else:
                f.write(f"| {row['left']} | {row['right']} |\n")

if __name__ == '__main__':
    main()