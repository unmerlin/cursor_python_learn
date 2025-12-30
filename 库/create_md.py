# -*- coding: utf-8 -*-
import csv
import os
import sys

# 设置工作目录为脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

csv_file = 'Python编程英语单词.csv'
md_file = 'Python编程英语单词.md'

def escape_markdown(text):
    if not text:
        return ''
    text = str(text).replace('|', '\\|')
    text = text.replace('\n', '<br>')
    return text

try:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    md_content = '# Python编程英语单词\n\n'
    md_content += '| 单词 | 音标 | 中文翻译 | 词根构成 | 编程相关例句 | 记忆技巧 |\n'
    md_content += '|------|------|----------|----------|--------------|----------|\n'
    
    for row in rows[1:]:
        if len(row) >= 6 and any(cell.strip() for cell in row):
            while len(row) < 6:
                row.append('')
            escaped_row = [escape_markdown(cell) for cell in row[:6]]
            md_content += '| ' + ' | '.join(escaped_row) + ' |\n'
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f'Success: {md_file}')
    sys.exit(0)
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)

