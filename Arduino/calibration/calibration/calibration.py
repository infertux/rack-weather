import pandas
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import seaborn
seaborn.set()


def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.figure(figsize=(16, 9))
    plt.scatter(x, y, color="m", marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1] * x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()


dataset = pandas.read_csv('calibration/calibration.csv')

x = dataset['indicated'].to_numpy()
y = dataset['real'].to_numpy()

correlation = dataset['indicated'].corr(dataset['real'])
print('sklearn correlation =', correlation)
print('numpy correlation =', np.corrcoef(x, y)[0][1])

#print('x =', x)
#print('y =', y)

model = LinearRegression()
model.fit(x.reshape(-1, 1), y)

b = model.intercept_
a = model.coef_

print()
print('sklearn: LINEAR REGRESSION')
print(a[0], 'x +', b)

plot_regression_line(x, y, [b, a[0]])

print()
print('numpy: LINEAR REGRESSION')
x = dataset['indicated']
y = dataset['real']

model = np.poly1d(np.polyfit(x, y, 1))

# add fitted polynomial line to scatterplot
polyline = np.linspace(22, 28, 50)
plt.scatter(x, y)
plt.plot(polyline, model(polyline))
plt.show()

print(model)

print()
print('numpy: POLYNOMIAL REGRESSION')
# polynomial fit with degree = 2
model = np.poly1d(np.polyfit(x, y, 2))

# add fitted polynomial line to scatterplot
polyline = np.linspace(22, 28, 50)
plt.scatter(x, y)
plt.plot(polyline, model(polyline))
#plt.show()

print(model)
