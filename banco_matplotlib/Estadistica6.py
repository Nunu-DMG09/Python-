import matplotlib.pyplot as plt 

Ciclismo = [7,8,6,11,7]
Maraton = [2,3,4,3,2]
Futbol = [7,8,7,2,2]
Natacion = [8,5,7,8,13]
Divisiones = [7,2,2,13]

Deportes = ['Ciclismo', 'Maraton', 'Futbol', 'Natacion']
Colores = ['red', 'purple', 'blue', 'yellow']

plt.pie(Divisiones, labels= Deportes, colors=Colores, startangle=90, shadow=True, explode=(0.1,0,0,0),
        autopct='%1.1f%%')
plt.title('Grafico Circular')
plt.show()