from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)

y_true = [0,0,0,0,0,0,0,0,1,1]
y_pred = [0,0,0,0,0,0,0,0,0,1]

matriz = confusion_matrix(y_true, y_pred)

acuracia = accuracy_score(y_true, y_pred)
precisao = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("Matriz de confusão:")
print(matriz)

print(f"\nAcurácia: {acuracia:.2f}")
print(f"Precisão: {precisao:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1: {f1:.2f}")

print(
    "\na acurácia de 0.90 é enganosa porque "
    "o conjunto está desbalanceado. Apesar de acertar 90% dos casos, "
    "o modelo detectou apenas metade dos ataques (recall = 0.50)."
)