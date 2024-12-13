#!/bin/bash

# 1. 复制当前目录中libWeWorkFinanceSdk_C.so到/usr/local/lib/libWeWorkFinanceSdk_C.so
sudo cp ./libWeWorkFinanceSdk_C.so /usr/local/lib/libWeWorkFinanceSdk_C.so
if [ $? -ne 0 ]; then
    echo "复制文件失败，请检查权限或文件是否存在"
    exit 1
fi

# 2. 运行g++ sdktools.cpp -ldl -o sdktools编译文件
g++ sdktools.cpp -ldl -o sdktools
if [ $? -ne 0 ]; then
    echo "编译文件失败，请检查源文件或相关依赖是否正确"
    exit 1
fi

echo "操作成功完成"