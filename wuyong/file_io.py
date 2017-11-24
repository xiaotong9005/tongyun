f=open('F:\\securities\\000016cons.txt')
f.readline() 
for i_f in f:
    strlist=i_f.split('	',i_f.count('	'))
    print('1:'+strlist[0])
    print('2:'+strlist[1])
    print('3:'+strlist[2])
    print('4:'+strlist[3])
    print('5:'+strlist[4])
    '''c=1
    for i in strlist:
        print(str(c)+':'+i)
        c+=1'''
