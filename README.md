# wine-spider

### todo list

1. vivino跳转下一页
2. 生成CSV文件
3. 图片下载
4. 注意等待延时，别让封IP
5. 断点续传
6. 并发处理

1、选中就换位置了
2、增加不选择的一项
3、排序

### startup

```
cd /home/ubuntu/wine-spider-combine-breed-area_breed_100
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &
setsid python3 wine-spider-combine-breed-area_breed_100/vivino_zh.py &>> out.log 2>&1 &
```