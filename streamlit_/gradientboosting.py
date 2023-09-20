import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report,  confusion_matrix

# Carregar o conjunto de dados
def load_data():

    data = pd.read_parquet("C:/Users/wms_1/Desktop/PISI3_DSI/PISI3_2022.2/data/renomeado_mediana_smoteenn.parquet")
   
    return data

data = load_data()

# Definir as características (X) e a coluna alvo (y)
X = data.drop("morte_hospital", axis=1)
y = data["morte_hospital"]

# Dividir o conjunto de dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicializar o modelo Naive Bayes do tipo Bernoulli
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = clf.predict(X_test)

# Gerar e exibir o relatório de classificação
report = classification_report(y_test, y_pred)
print("Relatório de Classificação:")
print(report)

# Visualizar a matriz de confusão
print("Matriz de Confusão:")
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.show()
