from cal_pkg import operator as op

result = op.diff(10,20)
print(result)


from cal_pkg import review as rv
rv.review_result(10)

#import MyModule as MM

#MM.database_connection("http:www.naver.com")



# 남이 만든 라이브러리를 설치하는 법 : 라이브러리의 이름을 알아야 설치한다.
import matplotlib.pyplot as plt

x = [1,2,3]
y = [1,2,3]

plt.figure(figsize=(5,7))
plt.plot(x,y)
plt.show()