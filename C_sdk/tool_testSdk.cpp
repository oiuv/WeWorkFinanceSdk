#include "WeWorkFinanceSdk_C.h"
#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string>
using std::string;

typedef WeWorkFinanceSdk_t *newsdk_t();
typedef int Init_t(WeWorkFinanceSdk_t *, const char *, const char *);
typedef void DestroySdk_t(WeWorkFinanceSdk_t *);

typedef int GetChatData_t(WeWorkFinanceSdk_t *, unsigned long long, unsigned int, const char *, const char *, int, Slice_t *);
typedef Slice_t *NewSlice_t();
typedef void FreeSlice_t(Slice_t *);

typedef int GetMediaData_t(WeWorkFinanceSdk_t *, const char *, const char *, const char *, const char *, int, MediaData_t *);
typedef int DecryptData_t(const char *, const char *, Slice_t *);
typedef MediaData_t *NewMediaData_t();
typedef void FreeMediaData_t(MediaData_t *);

int main(int argc, char *argv[])
{
    int ret = 0;
    // seq ��ʾ����ҵ�浵��Ϣ��ţ�����ŵ�����������ȡ��Ž�������Ϊ�ϴ���ȡ���ؽ���������š��״���ȡʱseq��0��sdk�᷵����Ч�����������Ϣ��
    // limit ��ʾ������ȡ�������Ϣ������ȡֵ��ΧΪ1~1000
    // proxy��passwdΪ����������������sdk�Ļ�������ֱ�ӷ�����������Ҫ���ô��������sdk���ʵ�������"https://qyapi.weixin.qq.com"��
    // ������ͨ��curl����"https://qyapi.weixin.qq.com"����֤����������ȷ���ٴ���sdk��
    // timeout Ϊ��ȡ�Ự�浵�ĳ�ʱʱ�䣬��λΪ�룬���鳬ʱʱ������Ϊ5s��
    // sdkfileid ý���ļ�id���ӽ��ܺ�ĻỰ�浵�еõ�
    // savefile ý���ļ�����·��
    // encrypt_key ��ȡ�Ự�浵���ص�encrypt_random_key��ʹ����������ҵ΢�Ź���̨��rsa��Կ��Ӧ��˽Կ���ܺ�õ�encrypt_key��
    // encrypt_chat_msg ��ȡ�Ự�浵���ص�encrypt_chat_msg
    if (argc < 2)
    {
        printf("./sdktools 1(chatmsg) 2(mediadata) 3(decryptdata)\n");
        printf("./sdktools 1 seq limit proxy passwd timeout\n");
        printf("./sdktools 2 fileid proxy passwd timeout savefile\n");
        printf("./sdktools 3 encrypt_key encrypt_chat_msg\n");
        return -1;
    }

    void *so_handle = dlopen("./libWeWorkFinanceSdk_C.so", RTLD_LAZY);
    if (!so_handle)
    {
        printf("load sdk so fail:%s\n", dlerror());
        return -1;
    }
    newsdk_t *newsdk_fn = (newsdk_t *)dlsym(so_handle, "NewSdk");
    WeWorkFinanceSdk_t *sdk = newsdk_fn();

    // ʹ��sdkǰ��Ҫ��ʼ������ʼ���ɹ����sdk����һֱʹ�á�
    // ���貢������sdk������ÿ���̳߳���һ��sdkʵ����
    // ��ʼ��ʱ�������Լ���ҵ��corpid��secrectkey��
    Init_t *init_fn = (Init_t *)dlsym(so_handle, "Init");
    DestroySdk_t *destroysdk_fn = (DestroySdk_t *)dlsym(so_handle, "DestroySdk");
    ret = init_fn(sdk, "wwdf65802ca25ec195", "-Ta6WMWxBhfGolWnnlO15nQckj3DRKAowUOdX2fwvzE");
    if (ret != 0)
    {
        // sdk��Ҫ�����ͷ�
        destroysdk_fn(sdk);
        printf("init sdk err ret:%d\n", ret);
        return -1;
    }

    int type = strtoul(argv[1], NULL, 10);
    if (type == 1)
    {
        // ��ȡ�Ự�浵
        uint64_t iSeq = strtoul(argv[2], NULL, 10);
        uint64_t iLimit = strtoul(argv[3], NULL, 10);
        uint64_t timeout = strtoul(argv[6], NULL, 10);

        NewSlice_t *newslice_fn = (NewSlice_t *)dlsym(so_handle, "NewSlice");
        FreeSlice_t *freeslice_fn = (FreeSlice_t *)dlsym(so_handle, "FreeSlice");

        // ÿ��ʹ��GetChatData��ȡ�浵ǰ��Ҫ����NewSlice��ȡһ��chatDatas����ʹ����chatDatas�����ݺ󣬻���Ҫ����FreeSlice�ͷš�
        Slice_t *chatDatas = newslice_fn();
        GetChatData_t *getchatdata_fn = (GetChatData_t *)dlsym(so_handle, "GetChatData");
        ret = getchatdata_fn(sdk, iSeq, iLimit, argv[4], argv[5], timeout, chatDatas);
        if (ret != 0)
        {
            freeslice_fn(chatDatas);
            printf("GetChatData err ret:%d\n", ret);
            return -1;
        }
        printf("GetChatData len:%d data:%s\n", chatDatas->len, chatDatas->buf);
        freeslice_fn(chatDatas);
    }
    else if (type == 2)
    {
        // ��ȡý���ļ�
        std::string index;
        uint64_t timeout = strtoul(argv[5], NULL, 10);
        int isfinish = 0;

        GetMediaData_t *getmediadata_fn = (GetMediaData_t *)dlsym(so_handle, "GetMediaData");
        NewMediaData_t *newmediadata_fn = (NewMediaData_t *)dlsym(so_handle, "NewMediaData");
        FreeMediaData_t *freemediadata_fn = (FreeMediaData_t *)dlsym(so_handle, "FreeMediaData");

        // ý���ļ�ÿ����ȡ�����sizeΪ512k����˳���512k���ļ���Ҫ��Ƭ��ȡ�������ļ�δ��ȡ������mediaData�е�is_finish�᷵��0��ͬʱmediaData�е�outindexbuf�᷵���´���ȡ��Ҫ����GetMediaData��indexbuf��
        // indexbufһ���ʽ���Ҳ���ʾ����Range:bytes=524288-1048575������ʾ�����ȡ���Ǵ�524288��1048575�ķ�Ƭ�������ļ��״���ȡ��д��indexbufΪ���ַ�������ȡ������Ƭʱֱ�������ϴη��ص�indexbuf���ɡ�
        while (isfinish == 0)
        {
            // ÿ��ʹ��GetMediaData��ȡ�浵ǰ��Ҫ����NewMediaData��ȡһ��mediaData����ʹ����mediaData�����ݺ󣬻���Ҫ����FreeMediaData�ͷš�
            printf("index:%s\n", index.c_str());
            MediaData_t *mediaData = newmediadata_fn();
            ret = getmediadata_fn(sdk, index.c_str(), argv[2], argv[3], argv[4], timeout, mediaData);
            if (ret != 0)
            {
                // ������Ƭ��ȡʧ�ܽ���������ȡ�÷�Ƭ�������ͷ��ʼ��ȡ��
                freemediadata_fn(mediaData);
                printf("GetMediaData err ret:%d\n", ret);
                return -1;
            }
            printf("content size:%d isfin:%d outindex:%s\n", mediaData->data_len, mediaData->is_finish, mediaData->outindexbuf);

            // ����512k���ļ����Ƭ��ȡ���˴���Ҫʹ��׷��д���������ķ�Ƭ����֮ǰ�����ݡ�
            char file[200];
            snprintf(file, sizeof(file), "%s", argv[6]);
            FILE *fp = fopen(file, "ab+");
            printf("filename:%s \n", file);
            if (NULL == fp)
            {
                freemediadata_fn(mediaData);
                printf("open file err\n");
                return -1;
            }

            fwrite(mediaData->data, mediaData->data_len, 1, fp);
            fclose(fp);

            // ��ȡ�´���ȡ��Ҫʹ�õ�indexbuf
            index.assign(string(mediaData->outindexbuf));
            isfinish = mediaData->is_finish;
            freemediadata_fn(mediaData);
        }
    }
    else if (type == 3)
    {
        // ���ܻỰ�浵����
        // sdk����Ҫ���û�����rsa˽Կ����֤�û��Ự�浵����ֻ���Լ��ܹ����ܡ�
        // �˴���Ҫ�û�����rsa˽Կ����encrypt_random_key����Ϊencrypt_key��������sdk������encrypt_chat_msg��ȡ�Ự�浵���ġ�
        // ÿ��ʹ��DecryptData���ܻỰ�浵ǰ��Ҫ����NewSlice��ȡһ��Msgs����ʹ����Msgs�����ݺ󣬻���Ҫ����FreeSlice�ͷš�
        NewSlice_t *newslice_fn = (NewSlice_t *)dlsym(so_handle, "NewSlice");
        FreeSlice_t *freeslice_fn = (FreeSlice_t *)dlsym(so_handle, "FreeSlice");

        Slice_t *Msgs = newslice_fn();
        // decryptdata api
        DecryptData_t *decryptdata_fn = (DecryptData_t *)dlsym(so_handle, "DecryptData");
        ret = decryptdata_fn(argv[2], argv[3], Msgs);
        printf("chatdata :%s ret :%d\n", Msgs->buf, ret);

        freeslice_fn(Msgs);
    }

    return ret;
}
