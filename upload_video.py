from google import genai
import time

# 1. 初始化客户端
client = genai.Client(api_key="sk-0H1Wi23rA9DScpEehRPNEduBObrXYxD8Y7WoxkXsG1pJNkFa")

# 2. 上传视频
video_path = "C:\\Users\\贝贝\\Desktop\\e887abff5cf0b7df32dd1e1005291d53.mp4"
print(f"正在上传 {video_path}...")
myfile = client.files.upload(file=video_path)

# 3. 等待视频处理完成
print("等待视频处理...")
while myfile.state and myfile.state.name != "ACTIVE":
    print("处理中...")
    time.sleep(5)
    myfile = client.files.get(name=myfile.name)

print(f"上传完成！File URI: {myfile.uri}")

# 4. 发起分析请求
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        myfile,  # 直接传入文件对象
        "请用中文总结这段视频的主要内容。"
    ]
)

print(response.text)