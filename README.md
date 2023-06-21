# 会话内容存档

基本使用说明：

- https://zhuanlan.zhihu.com/p/597147920
- https://developer.work.weixin.qq.com/document/path/91360

本项目为基于企业微信提供的C_sdk，进行会话记录数据的获取、媒体数据的获取。

## openssl

```
# Windows
choco install openssl.light
```

```
# 生成私钥
openssl genrsa -out private.pem 2048
# 从私钥产生公钥
openssl rsa -in private.pem -pubout -out public.pem
```

## tool_testSdk.cpp

### 配置

修改以下部分为自己的企业配置：
```c
    ret = init_fn(sdk, "wwd08c8e7c775ab44d", "zJ6k0naVVQ--gt9PUSSEvs03zW_nlDVmjLCTOTAfrew");
```

### 优化

修改以下部分内容从显示为保存到jsonl文件：

1. 修改
```c
        printf("GetChatData len:%d data:%s\n", chatDatas->len, chatDatas->buf);
```
为
```c
        // 保存到文件
        FILE* file = fopen("chat.jsonl", "a");
        if (file != NULL) {
            fprintf(file, "%s\n", chatDatas->buf);
            fclose(file);
            printf("Chat data saved to chat.jsonl\n");
        } else {
            printf("Failed to open file\n");
        }
```

2. 修改
```c
        printf("chatdata :%s ret :%d\n", Msgs->buf, ret);
```
为
```c
        // 保存到文件
        FILE* file = fopen("chatdata.jsonl", "a");
        if (file != NULL) {
            fprintf(file, "%s\n", Msgs->buf);
            fclose(file);
            printf("Chat data saved to chatdata.jsonl\n");
        } else {
            printf("Failed to open file\n");
        }
```

### 编译

```
g++ tool_testSdk.cpp -ldl -o sdktools
```

### 用法

```c
//seq 表示该企业存档消息序号，该序号单调递增，拉取序号建议设置为上次拉取返回结果中最大序号。首次拉取时seq传0，sdk会返回有效期内最早的消息。
//limit 表示本次拉取的最大消息条数，取值范围为1~1000
//proxy与passwd为代理参数，如果运行sdk的环境不能直接访问外网，需要配置代理参数。sdk访问的域名是"https://qyapi.weixin.qq.com"。
//建议先通过curl访问"https://qyapi.weixin.qq.com"，验证代理配置正确后，再传入sdk。
//timeout 为拉取会话存档的超时时间，单位为秒，建议超时时间设置为5s。
//sdkfileid 媒体文件id，从解密后的会话存档中得到
//savefile 媒体文件保存路径
//encrypt_key 拉取会话存档返回的encrypt_random_key，使用配置在企业微信管理台的rsa公钥对应的私钥解密后得到encrypt_key。
//encrypt_chat_msg 拉取会话存档返回的encrypt_chat_msg
```
```
./sdktools 1(chatmsg) 2(mediadata) 3(decryptdata)
./sdktools 1 seq limit proxy passwd timeout
./sdktools 2 fileid savefile proxy passwd timeout
./sdktools 3 encrypt_key encrypt_chat_msg
```

> 注：获取会话记录内容不能超过5天，如果企业需要全量数据，则企业需要定期拉取聊天消息。返回的ChatDatas内容为json格式。

## python

    python3 -m pip install pycryptodome


### GetData

自动从头拉取聊天记录并保存至`chat.jsonl`

    python GetData.py

### Data2Excel

把拉取的聊天记录转为excel格式

    python Data2Excel.py chat.jsonl

### chatData

解密聊天记录并转存为`chatdata.jsonl`

    python chatData.py chat.xlsx

### WxChat.py

封装的类，提供从数据获取到解密格式化的所有功能，直接把chat.jsonl转为chatdata.jsonl。

### chatMsg

把解密的聊天记录格式化处理为`chat_<msgtype>.xlsx`

    python chatMsg.py chatdata.jsonl

### getFile

根据转换后的聊天记录获取图片、语音、文件等内容。

    python getFile.py

---

推荐直接`./run.sh`一键处理数据~