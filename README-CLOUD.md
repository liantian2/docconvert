# DocConvert 云端部署版

这个版本使用 Docker，把 Python、PDF 转 Word 所需库和 LibreOffice 一起安装到云服务器中。访问网站的电脑不需要安装 Python 或 LibreOffice。

## Render 部署

1. 在 GitHub 新建一个 repository，例如 `docconvert`。
2. 把本项目目录中的所有文件上传到 repository 根目录。确保根目录能直接看到 `Dockerfile`、`render.yaml`、`requirements.txt` 和 `app` 文件夹。
3. 登录 Render，创建新的 Web Service，并连接刚才的 GitHub repository。
4. Render 识别到 Dockerfile 后使用 Docker 部署。若要求填写端口，应用使用 Render 提供的 `PORT` 环境变量，无需手工修改代码。
5. 等待 Build/Deploy 完成后，Render 会提供一个 `onrender.com` 地址。打开即可使用。

## 功能

- PDF -> DOCX
- DOC/DOCX -> PDF
- 单文件最大 25 MB
- 转换文件使用服务器临时目录，响应下载完成后清理

## 注意

PDF -> Word 属于版面重建，复杂表格、字体、扫描件可能无法 100% 还原。当前版本不含 OCR，因此纯扫描 PDF 的文字识别效果有限。
