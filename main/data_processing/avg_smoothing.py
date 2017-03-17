# -*- coding: utf-8 -*-
'''
如果这一天的数据为0，则将该天用前三个星期对应天的平均值替换
从最后last_days开始计算，这里用后123天
'''
def cal_avg(filename,fileto,last_days):
    fr=open(filename)
    fr_to=open(fileto,"w")
    flag=0
    for line in fr.readlines():
        if flag==0:
            fr_to.write(line)
            flag=1
            continue
        data=line.strip().split(",")
        for i in range(len(data)-last_days,len(data)):
            if float(data[i])==0:
                data[i]=str((float(data[i-7])+float(data[i-14])+float(data[i-21]))/3.0)
        fr_to.write(",".join(data)+"\n")
    fr_to.close()

if __name__ == '__main__':
    filename="../../data/statistics/count_user_pay.csv"
    fileto="../../data/statistics/count_user_pay_avg.csv"
    cal_avg(filename,fileto,123)