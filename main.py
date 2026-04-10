from flask import Flask, render_template_string, abort, send_from_directory
import markdown
import os

app = Flask(__name__)

# 基础HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4C01的学习资料~</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <h1>4C01的学习资料</h1>
        <div class="nav-links">
            <a href="http://4c01.cn" class="nav-text">4C01</span>
            <a href="https://trystage.cn" class="nav-link desktop-only">Trystage</a>
            <a href="https://gallery.trystage.cn" class="nav-link desktop-only">项目画廊</a>
        </div>
    </nav>
    <div class="container">
        <aside class="sidebar" id="sidebar">
            <h2 onclick="toggleSidebar()">☰</h2>
            <ul>
                <li><a href="/index.md">首页</a></li>
                <li><a href="/cooking/index.md">烹饪</a></li>
                <li><a href="/math/index.md">数学</a></li>
                <li><a href="/culture/index.md">文化</a></li>
                <li><a href="/AI/index.md">AI</a></li>
            </ul>
        </aside>
        <main class="main-content">
            <div class="content">
                {{ content|safe }}
            </div>
        </main>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
"""

# Markdown扩展配置
MARKDOWN_EXTENSIONS = [
    'extra',  # 包含表格、代码块等额外功能
    'codehilite',  # 代码高亮
    'toc',  # 目录生成
    'nl2br',  # 换行转<br>
    'sane_lists'  # 更合理的列表处理
]

@app.route('/')
@app.route('/index.md')
def index():
    """处理根路径和/index.md请求"""
    return serve_markdown('index.md')

@app.route('/<path:filename>.md')
def markdown_file(filename):
    """处理所有以.md结尾的请求"""
    return serve_markdown(f"{filename}.md")

def serve_markdown(filename):
    """服务Markdown文件并将其转换为HTML"""
    # 安全验证，防止路径遍历攻击
    if '..' in filename or filename.startswith('/'):
        abort(404)
    filepath = filename
    # 如果文件不存在，返回404
    if not os.path.isfile(filepath):
        abort(404)
    
    # 读取Markdown文件
    with open(filepath, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 转换Markdown为HTML
    html_content = markdown.markdown(
        markdown_content, 
        extensions=MARKDOWN_EXTENSIONS,
        output_format='html5'
    )
    
    # 使用模板渲染最终HTML
    title = os.path.splitext(filename)[0]
    return render_template_string(HTML_TEMPLATE, title=title, content=html_content)

@app.route('/static/<path:filename>')
def static_files(filename):
    """服务静态文件"""
    return send_from_directory('static', filename)

@app.route('/<path:filename>')
def assets(filename):
    """服务静态资源文件"""
    return send_from_directory('', filename)

if __name__ == '__main__':
    # 创建必要的目录
    os.makedirs('assets', exist_ok=True)
    
    # 如果content目录下没有index.md，创建一个示例文件
    if not os.path.exists('index.md'):
        with open('index.md', 'w', encoding='utf-8') as f:
            f.write("# 欢迎使用Markdown服务器\n\n这是一个示例Markdown文件。")
    
    # 启动Flask应用
    app.run(debug=True, host='0.0.0.0', port=5071)
