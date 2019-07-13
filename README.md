# care_for_the_elderly

## 智慧养老平台

前端： Vue.js & ElementUI
后端： python + Django
模型： 百度AI（network） & pytorch(local)

维护相关人员增删改查、查看实时监控视频、监测老人摔倒情况、情绪状况、交互情况、陌生人状况、入侵状况，并查看实时可视化报表。

live-streaming 为摄像头服务器，在两台电脑分别部署并在conf.json修改相应上传ip

backend 为web后端，在conf.json可修改ip、摔倒角度阈值、神经网络模型方案（'local' or 'network')

使用前先迁移数据库（makemigrations & migrate）