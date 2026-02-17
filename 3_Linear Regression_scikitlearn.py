import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn import linear_model

# random data
A = np.array([[2,5,7,9,11,16,19,23,22,29,29,35,37,40,46]]).T
b = np.array([[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]]).T

# creat model
lr = linear_model.LinearRegression()

# train model
lr.fit(A,b)

# y = ax+b, a: coefficent, b intercept
print(lr.coef_)
print(lr.intercept_)

# visualize data
plt.plot(A,b,'ro')

# draw line
x0 = np.array([[1,46]]).T
y0 = x0*lr.coef_ + lr.intercept_

plt.plot(x0,y0)

# test predicting data
x_test = np.array([[12]])
y_test = lr.predict(x_test)

print(y_test)

plt.show()

