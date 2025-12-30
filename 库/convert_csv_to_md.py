import csv

# 读取CSV文件
csv_file = 'Python编程英语单词.csv'
md_file = 'Python编程英语单词.md'

# 转义Markdown表格中的特殊字符
def escape_markdown(text):
    """转义Markdown表格中的管道符和换行符"""
    if not text:
        return ''
    text = str(text).replace('|', '\\|')  # 转义管道符
    text = text.replace('\n', '<br>')  # 换行符替换为<br>
    return text

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# 生成Markdown内容
md_content = '# Python编程英语单词\n\n'
md_content += '| 单词 | 音标 | 中文翻译 | 词根构成 | 编程相关例句 | 记忆技巧 |\n'
md_content += '|------|------|----------|----------|--------------|----------|\n'

# 添加数据行（跳过表头，跳过空行）
for row in rows[1:]:
    if len(row) >= 6 and any(cell.strip() for cell in row):  # 确保不是空行
        # 确保每行有6列，不足的用空字符串填充
        while len(row) < 6:
            row.append('')
        # 转义每一列的内容
        escaped_row = [escape_markdown(cell) for cell in row[:6]]
        md_content += '| ' + ' | '.join(escaped_row) + ' |\n'

# 写入Markdown文件
with open(md_file, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f'成功生成Markdown文件: {md_file}')

