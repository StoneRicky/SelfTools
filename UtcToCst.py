import datetime
from datetime import timedelta


# #现在时刻 北京时转世界时
# """python中datetime.now()：读取的时间是系统的本地时间"""
# t_bj = datetime.datetime.now().strftime("%Y%m%d%H%M")
# t_bj2utc = (datetime.datetime.now()- datetime.timedelta(hours=8)).strftime("%Y%m%d%H%M")
# print('北京时间：',t_bj)
# print('世界时间：',t_bj2utc)

# #现在时刻 世界时转北京时：
# """python中datetime.utcnow()：读取的时间一直都是系统的“世界标准时间”，"""
# t_utc = datetime.datetime.utcnow().strftime("%Y%m%d%H%M")
# t_utc2bj = (datetime.datetime.utcnow()+ datetime.timedelta(hours=8)).strftime("%Y%m%d%H%M")
# print('世界时间：',t_utc)
# print('北京时间：',t_utc2bj)


# #指定时刻 北京时转世界时
# time='2022102009'
# t_bj= datetime.datetime.strptime(time,'%Y%m%d%H') #字符串转换为时间戳
# t_utc = t_bj-timedelta(hours=8) #将北京时转换为世界时
# print('北京时：',t_bj,'\n世界时：',t_utc)

#指定时刻 世界时转北京时
time='2024062116'
t_utc= datetime.datetime.strptime(time,'%Y%m%d%H') #字符串转换为时间戳
t_bj = t_utc+timedelta(hours=8) #将世界时转换为北京时
print('世界时：',t_utc,'\n北京时：',t_bj)