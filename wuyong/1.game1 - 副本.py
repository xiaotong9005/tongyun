import random
a=random.randint(0,100)
i=0
print('我们已经生成了一个100以内正整数，你能猜出来吗?')
while 1>i:
    guess=int(input("输入你猜测的数字："))
    if guess==a:
        print("牛逼啊兄弟，猜对了")
        i=2
    else:
        if guess>a:
            print('你猜的大了，继续');
        if guess<a:
            print('你猜的小了，继续');
print("游戏结束")   
