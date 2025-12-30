import csv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

csv_file = 'Python编程英语单词.csv'
md_file = 'Python编程英语单词.md'

def escape_markdown(text):
    if not text:
        return ''
    text = str(text).replace('|', '\\|')
    text = text.replace('\n', '<br>')
    return text

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

print('Success')


