import matplotlib.pyplot as plt
A = [1,2,3,4]
B = [11,22,33,44]

plt.plot (A,B, label ='linea1', linewidth = 4, color = 'blue')
plt.title('Diagrama de lineas')
plt.legend()
plt.show()