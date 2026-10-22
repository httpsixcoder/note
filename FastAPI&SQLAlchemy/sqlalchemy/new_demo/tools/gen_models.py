import subprocess
import sys

from new_demo.sqlalchemy_demo.database import url


def table_test_orm_new_model(run=False):
    """数据库反向生成ORM模型工具"""
    if not run:
        return

    output_path="temp_generated_models.py"
    venv_python=sys.executable
    print("当前Python解释器为",venv_python)
    cmd=[
        venv_python,"-m","sqlacodegen",
       "--generator" ,"tables",
        url
    ]
    result= subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd="D:/git/note/FastAPI&SQLAlchemy/sqlalchemy_demo"  # 指定生成目录
    )
    print("===命令执行结果===")
    print(f"返回码：{result.returncode}")
    print(f"stdout：\n {result.stdout}")
    print(f"stdeer：\n {result.stderr}")

    if result.returncode != 0:
        raise RuntimeError(f"sqlacodegen执行失败:\n{result.stderr}")
    if not result.stdout.strip():
        raise RuntimeError("sqlacodegen输出为空")

    with open(output_path,"w") as f:
        f.write(result.stdout)
    print(f"临时模型文件生成完成：{output_path}，请手动复制合并到models，不要直接覆盖！")

if __name__ == "__main__":
    # 需要反向生成，把下面True打开，运行完立刻改回False
    table_test_orm_new_model(run=False)