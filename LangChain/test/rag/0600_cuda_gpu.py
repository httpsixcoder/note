import time
import torch
from langchain_huggingface import HuggingFaceEmbeddings

# 准备 1000 条测试数据
test_texts = [f"这是第 {i} 条用来测试速度的文本数据" for i in range(1000)]


def test_speed(device_type):
    print(f"\n========== 正在测试 {device_type.upper()} ==========")

    # 1. 加载模型，指定设备
    model = HuggingFaceEmbeddings(
        model_name='../../assets/models/bge-base-zh-v1.5',
        model_kwargs={'device': device_type},
        encode_kwargs={'batch_size': 32}  # 分批大小
    )

    # 2. 开始计时
    start_time = time.time()

    # 3. 执行批量向量化
    results = model.embed_documents(test_texts)

    # 4. 结束计时
    end_time = time.time()

    print(f"✅ 完成了 {len(results)} 条文本的向量化")
    print(f"⏱️ 耗时: {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    if not torch.cuda.is_available():
        print("❌ 显卡不可用，请检查 PyTorch 安装！")
    else:
        # 跑 CPU 测试
        test_speed("cpu")
        # 跑 GPU 测试
        test_speed("cuda")

"""
========== 正在测试 CPU ==========
✅ 完成了 1000 条文本的向量化
⏱️ 耗时: 25.60 秒

========== 正在测试 CUDA ==========
✅ 完成了 1000 条文本的向量化
⏱️ 耗时: 3.36 秒
"""
