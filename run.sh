#!/bin/bash

if [ -f "chat.jsonl" ] || [ -f "chatdata.jsonl" ]; then
    echo "chat.jsonl 或 chatdata.jsonl 文件已存在，请先备份或删除"
    exit 1
else
    python3 WxChat.py
fi

if [ -f "chatdata.jsonl" ]; then
    python3 chatMsg.py

else
    echo "chatdata.jsonl 文件不存在，请先执行 WxChat.py"
    exit 1
fi

if [ -f "chat_list.xlsx" ]; then
    python3 getFile.py
else
    echo "chat_list.xlsx 文件不存在，请先执行 chatMsg.py"
fi