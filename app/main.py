from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import subprocess

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTask

app = FastAPI(title="DocConvert")
BASE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

MAX_BYTES = 25 * 1024 * 1024
ALLOWED = {".pdf", ".docx", ".doc"}

@app.get("/")
def home():
    return FileResponse(BASE / "templates" / "index.html")


def cleanup(path: str):
    shutil.rmtree(path, ignore_errors=True)


def libreoffice_convert(source: Path, outdir: Path, fmt: str):
    cmd = ["libreoffice", "--headless", "--convert-to", fmt, "--outdir", str(outdir), str(source)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except FileNotFoundError:
        raise HTTPException(500, "服务器未安装 LibreOffice。请先安装 LibreOffice。")
    except subprocess.TimeoutExpired:
        raise HTTPException(500, "转换超时，请尝试较小的文件。")
    if result.returncode != 0:
        raise HTTPException(500, f"Word 转 PDF 失败：{result.stderr or result.stdout}")


@app.post("/api/convert")
async def convert(file: UploadFile = File(...)):
    original = Path(file.filename or "upload")
    ext = original.suffix.lower()
    if ext not in ALLOWED:
        raise HTTPException(400, "只支持 PDF、DOCX 和 DOC 文件。")

    data = await file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "文件不能超过 25 MB。")

    temp = TemporaryDirectory(prefix="docconvert_")
    work = Path(temp.name)
    source = work / ("input" + ext)
    source.write_bytes(data)

    try:
        if ext == ".pdf":
            from pdf2docx import Converter
            output = work / f"{original.stem}.docx"
            cv = Converter(str(source))
            try:
                cv.convert(str(output))
            finally:
                cv.close()
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            libreoffice_convert(source, work, "pdf")
            generated = work / "input.pdf"
            if not generated.exists():
                raise HTTPException(500, "未生成 PDF 文件。")
            output = work / f"{original.stem}.pdf"
            generated.rename(output)
            media_type = "application/pdf"
    except HTTPException:
        temp.cleanup()
        raise
    except Exception as e:
        temp.cleanup()
        raise HTTPException(500, f"转换失败：{str(e)}")

    # Keep temp object alive until response cleanup by detaching its automatic finalizer.
    temp._finalizer.detach()
    return FileResponse(
        output,
        media_type=media_type,
        filename=output.name,
        background=BackgroundTask(cleanup, str(work)),
    )
