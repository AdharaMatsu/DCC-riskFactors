import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("BCSC-data.csv")

atributos = ['age_group_5_years', 'race_eth', 'first_degree_hx', 'age_menarche',
             'age_first_birth', 'BIRADS_breast_density', 'current_hrt',
             'menopaus', 'bmi_group', 'biophx']
target = 'breast_cancer_history'

# Construye la lista de instancias: [[vector de atributos], clase]
instancia = [[list(map(int, row[atributos])), str(int(row[target]))] for _, row in df.iterrows()]

def Euclidiana(A, B):
    distancia = 0
    for i in range(len(A)):
        distancia += (A[i] - B[i]) ** 2
    distancia = distancia ** 0.5
    return round(distancia, 2)

K = 3
index = []
n = random.randrange(0, len(instancia))
index.append(n)
temp = K - 1
while temp > 0:
    n = random.randrange(0, len(instancia))
    if n not in index:
        index.append(n)
        temp -= 1

centroides = [instancia[i].copy() for i in index]
for centroide in centroides:
    centroide[1] = "---"


for _ in range(10):
    grupos = [[] for _ in range(K)]
    for registro in instancia:
        indexasignado = -1
        distanciaMin = float('inf')
        for i, centroide in enumerate(centroides):
            distancia = Euclidiana(centroide[0], registro[0])
            if distancia < distanciaMin:
                distanciaMin = distancia
                indexasignado = i
        grupos[indexasignado].append(registro)

    for idx, grupo in enumerate(grupos):
        if not grupo:
            continue
        nuevo_centroide = []
        for i in range(len(grupo[0][0])):
            suma = sum(reg[0][i] for reg in grupo)
            nuevo_centroide.append(suma / len(grupo))
        centroides[idx][0] = nuevo_centroide
        centroides[idx][1] = "---"

distribucion = {
    f"Grupo {i+1}": {
        "Con cáncer": sum(1 for x in grupo if x[1] == '1'),
        "Sin cáncer": sum(1 for x in grupo if x[1] == '0')
    } for i, grupo in enumerate(grupos)
}

data_grafica = []
for grupo, conteo in distribucion.items():
    for clase, cantidad in conteo.items():
        data_grafica.append({'Grupo': grupo, 'Clase': clase, 'Cantidad': cantidad})

df_grafica = pd.DataFrame(data_grafica)

plt.figure(figsize=(8, 5))
sns.barplot(data=df_grafica, x="Grupo", y="Cantidad", hue="Clase")
plt.title("Distribución de cáncer de mama por grupo (KMeans)")
plt.ylabel("Cantidad de registros")
plt.tight_layout()
plt.grid(True)
plt.show()
