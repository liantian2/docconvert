# DocConvert

一个简单的 PDF ⇄ Word 在线转换网站。

## 功能
- PDF -> DOCX（pdf2docx）
- DOC/DOCX -> PDF（LibreOffice headless）
- 拖拽上传、格式检测、25MB 限制
- 转换后直接下载
- 请求完成后删除服务器临时文件

## 运行
需要 Python 3.10+ 和 LibreOffice。

### Windows / macOS / Linux
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
然后浏览器打开 http://localhost:8000

## LibreOffice
Word -> PDF 依赖 `libreoffice` 命令可从 PATH 调用。Windows 如果找不到命令，可以把 LibreOffice/program 加入 PATH，或在 `main.py` 中把 `libreoffice` 改为 soffice.exe 的完整路径。

## 注意
PDF -> DOCX 不是无损转换。复杂排版、特殊字体、公式以及扫描 PDF 可能无法完整还原。扫描件需要另加 OCR。
