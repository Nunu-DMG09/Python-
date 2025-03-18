import matplotlib.pyplot as plt

X1 = [3,4,5,6]
Y1 = [5,6,3,4]

X2 = [2,5,8]
Y2 = [3,4,3]

plt.plot(X1,Y1, label ='linea 1', linewidth = 4, color ='blue')
plt.plot(X2,Y2, label ='linea 2', linewidth = 4, color ='green')
plt.title('Diagrama de lineas')
plt.ylabel('Eje Y')
plt.xlabel('Eje X')

plt.legend
plt.grid()
plt.show()