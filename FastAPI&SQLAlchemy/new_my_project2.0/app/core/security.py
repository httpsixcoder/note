from fastapi import Header, HTTPException


# 1. 模拟权限校验依赖（真实项目会放在 core/security.py 中）
def verify_token(token: str = Header(...)):
    pass  # 测试都注释了
    # if token != "Bearer secret_token":
    #     raise HTTPException(status_code=401, detail="无效的认证凭据")
    # return {"id": 1, "name": "管理员"}
