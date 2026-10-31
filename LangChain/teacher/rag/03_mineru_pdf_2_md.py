"""
    测试：使用MinerU将pdf转换为md
    1.第一次请求，获取上传文件的url
    2.第二次请求，通过第一次请求所获取的url上传pdf文件
    3.第三次请求，获取最终结果（下载pdf转换成md的url地址）
"""
import requests


# 第一次和第二次请求
def upload_file():
    token = "sk-pP4TFc6Jdwk5zEB2nMPdNL4wcLpAduBafHUmR2xdMrogChOS"
    # 第一次请求的请求地址：获取上传PDF文件的url
    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "files": [
            {"name": "demo.pdf", "data_id": "abcd"}
        ],
        "model_version": "vlm"
    }
    try:
        # 发送第一次请求，获取上传的url
        # json是请求体里面是json的时候
        # data是请求体里面是不是json的时候，例如文件
        response_first = requests.post(url, headers=header, json=data)
        # 判断请求发送是否成功
        if response_first.status_code == 200:
            print(f"第一次请求成功，响应状态码：{response_first.status_code}")
            result_first = response_first.json()
            if result_first.get("code") == 0:
                print(
                    f"第一次请求调用接口成功，接口状态码：{result_first.get("code")}，接口处理信息：{result_first.get("msg")}")
                # 分别获取任务id和第二次上传文件的请求地址
                batch_id = result_first.get("data").get("batch_id")
                file_url = result_first.get("data").get("file_urls")[0]
                pdf_file_path = "../../assets/sample.pdf"
                with open(pdf_file_path, "rb") as f:
                    # 发送第二次请求
                    response_second = requests.put(file_url, data=f)
                    if response_second.status_code == 200:
                        print(f"发送第二次请求，文件上传成功")
                        return batch_id
                    else:
                        print(f"发送第二次请求，文件上传失败")
            else:
                print(
                    f"第一次请求调用接口失败，接口状态码：{result_first.get("code")}，接口处理信息：{result_first.get("msg")}")
        else:
            print(f"第一次请求失败，响应状态码：{response_first.status_code}")
    except Exception as e:
        print(f"pdf文件上传过程中出现异常，信息：{e}")


# 第三次请求
def get_zip_url(batch_id):
    token = "sk-pP4TFc6Jdwk5zEB2nMPdNL4wcLpAduBafHUmR2xdMrogChOS"
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response_third = requests.get(url, headers=header)
    if response_third.status_code == 200:
        print(f"第三次请求成功，响应状态码：{response_third.status_code}")
        result_third = response_third.json()
        print(result_third)
        # result_third=response_third.json()
        # if result_third.get("code") == 0:
        #     print(f"第三次调用接口成功，接口状态码：{result_third.get("code")}")
        #     """
        #     任务处理状态，完成:done，
        #     waiting-file: 等待文件上传排队提交解析任务中，
        #     pending: 排队中，
        #     running: 正在解析，
        #     failed：解析失败，
        #     converting：格式转换中
        #     """
        # service_state=result_third.get("data").get("extract_result").get("state")
        # return service_state
        # else:
        #     print(f"第三次调用接口失败，接口状态码：{result_third.get("code")}")
    else:
        print(f"第三次请求失败，响应状态码：{response_third.status_code}")


if __name__ == "__main__":
    pass
    # 第一次执行，（获得batch_id后注释）
    # batch_id = upload_file()
    # print(batch_id)
    # 第二次执行，直接携带 batch_id
    # get_zip_url("7baa4cf2-9e67-4ad3-9029-478906232beb")
