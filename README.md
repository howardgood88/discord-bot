# discord-bot
## 運行
1. 修改RC_info.txt內的JSON格式之Key值，改為想紀錄之成員ID，value值改為各自之初始時數  
2.		python bot.py

## 功能
紀錄成員上線時間

online bot用法：  
onilne bot的前導符號為"!"，任何指令前面都須加上才能執行。

online bot的功能：  
紀錄成員上線時間。只要成員上線後進入任意語音頻道，  
online bot會偵測到並回應"I see you, xxx"，這時上線時間已開始累計，  
並於下線時(離開此群組也算)結算時數

online bot提供之指令列表：
1. !timer：查看成員累計上線時間
2. !rc：查看RC舊群組資訊
