import matplotlib.pyplot as plt 

X1 = [0.25, 1.25, 2.25, 3.25, 4.25]
Y1 = [10,55, 80, 32, 40]

X2= [0.75, 1.75, 2.75, 3.75, 4.75]
Y2 = [42, 26, 10, 29, 66]

plt.scatter(X1,Y1, label ='Datos 1', color='blue')
plt.scatter(X2,Y2, label ='Datos 2', color='green')
plt.title('Graficos de Dispersion')
plt.ylabel('EJE Y')
plt.xlabel('EJE X')

plt.legend()
plt.show()