import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import keras as ks
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

# Загрузка данных
dataset = loadtxt('data2.csv', delimiter=';', skiprows=1)
x = dataset[:, 0:11]
y = dataset[:, 11].astype(int)

print(f"Исходные данные - X shape: {x.shape}, Y shape: {y.shape}")
print(f"Уникальные классы Y: {np.unique(y)}")

# Нормализация меток классов (3-8 → 0-5)
y_normalized = y - y.min()  # 3→0, 4→1, ..., 8→5
num_classes = len(np.unique(y_normalized))

# One-hot encoding для меток
y_categorical = to_categorical(y_normalized, num_classes=num_classes)

# НОРМАЛИЗАЦИЯ ПРИЗНАКОВ (X)
print("\n1. Min-Max нормализация (все признаки в диапазоне 0-1)")
scaler = MinMaxScaler()
x_normalized = scaler.fit_transform(x)

print(f"   До нормализации: min={x.min():.2f}, max={x.max():.2f}, mean={x.mean():.2f}")
print(f"   После нормализации: min={x_normalized.min():.2f}, max={x_normalized.max():.2f}, mean={x_normalized.mean():.2f}")

# Разделение данных
x_train, x_test, y_train, y_test = train_test_split(
    x_normalized, y_categorical,
    test_size=0.2, 
    random_state=42, 
    stratify=y_normalized
)

# Создание модели
model = Sequential([
    Dense(32, activation='relu', input_shape=(11,)),
    Dense(16, activation='relu'),
    Dense(num_classes, activation='softmax')  # Упростил архитектуру
])

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',  # Adam обычно лучше
    metrics=['accuracy']
)

print("\n2. Обучение модели...")
history = model.fit(
    x_train, y_train,
    epochs=150,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

# Предсказание
predictions = model.predict(x_test, verbose=0)
predictions_norm = np.argmax(predictions, axis=1)
predictions_original = predictions_norm + y.min()

# Оценка
y_test_norm = np.argmax(y_test, axis=1)
y_test_original = y_test_norm + y.min()
accuracy = np.mean(predictions_original == y_test_original)

print("\n" + "="*60)
print("3. ОБЩИЕ РЕЗУЛЬТАТЫ:")
print("="*60)
print(f"   Общая точность: {accuracy:.3f} ({accuracy*100:.1f}%)")
print(f"   Правильно предсказано: {np.sum(predictions_original == y_test_original)}/{len(y_test_original)}")

print("\n" + "="*60)
print("4. АНАЛИЗ ПО КЛАССАМ:")
print("="*60)

# 1. Classification Report (самый информативный)
print("\n   Classification Report:")
print("   " + "-"*50)
report = classification_report(y_test_original, predictions_original, output_dict=True)
df_report = pd.DataFrame(report).transpose()

# Выводим только основные метрики
for cls in sorted(np.unique(y_test_original)):
    if str(cls) in df_report.index:
        row = df_report.loc[str(cls)]
        print(f"   Класс {cls}:")
        print(f"     Precision: {row['precision']:.3f} - из всех предсказанных классом {cls}, сколько действительно класс {cls}")
        print(f"     Recall:    {row['recall']:.3f} - из всех реальных класса {cls}, сколько правильно предсказаны")
        print(f"     F1-Score:  {row['f1-score']:.3f} - гармоническое среднее precision и recall")
        print(f"     Support:   {int(row['support'])} примеров в тестовой выборке")
        print()

# 2. Confusion Matrix (матрица ошибок)
print("\n   Confusion Matrix (Матрица ошибок):")
print("   " + "-"*50)
print("   Фактические значения →")
print("   Предсказанные значения ↓")
print()

cm = confusion_matrix(y_test_original, predictions_original)
classes = sorted(np.unique(y_test_original))

# Заголовок
header = "      " + " ".join([f"{cls:5}" for cls in classes])
print(header)
print("   " + "-"*len(header))

# Строки матрицы
for i, cls_true in enumerate(classes):
    row = f"{cls_true:5} "
    for j, cls_pred in enumerate(classes):
        row += f"{cm[i][j]:5}"
    print("   " + row)

print("\n   Как читать матрицу:")
print("   - Диагональ (главная) - правильные предсказания")
print("   - Вне диагонали - ошибки")
print("   - Строка = фактические классы, столбец = предсказанные")

# 3. Точность по каждому классу
print("\n   Точность по каждому классу:")
print("   " + "-"*50)

for cls in classes:
    mask = y_test_original == cls
    if np.sum(mask) > 0:  # Если есть примеры этого класса
        class_accuracy = np.mean(predictions_original[mask] == cls)
        correct = np.sum(predictions_original[mask] == cls)
        total = np.sum(mask)
        
        # Оценка качества
        if class_accuracy >= 0.8:
            rating = "Отлично ✓"
        elif class_accuracy >= 0.6:
            rating = "Хорошо ✓"
        elif class_accuracy >= 0.4:
            rating = "Удовлетворительно ~"
        else:
            rating = "Плохо ✗"
        
        print(f"   Класс {cls}: {class_accuracy:.1%} ({correct}/{total}) - {rating}")

# 4. Анализ ошибок
print("\n   Анализ ошибок (куда ошибается модель):")
print("   " + "-"*50)

errors = predictions_original - y_test_original
unique_errors, error_counts = np.unique(errors, return_counts=True)

print("   Распределение ошибок:")
for err, count in zip(unique_errors, error_counts):
    if err != 0:  # Показываем только ошибки
        percentage = count / len(errors) * 100
        print(f"     Ошибка {err:+d}: {count} примеров ({percentage:.1f}%)")

# 5. Самые частые ошибки
print("\n   Самые частые ошибки (путаница между классами):")
print("   " + "-"*50)

# Находим самые частые ошибки (не по диагонали)
error_pairs = []
for i in range(len(classes)):
    for j in range(len(classes)):
        if i != j and cm[i][j] > 0:  # Только ошибки
            error_pairs.append((classes[i], classes[j], cm[i][j]))

# Сортируем по количеству ошибок
error_pairs.sort(key=lambda x: x[2], reverse=True)

for true_cls, pred_cls, count in error_pairs[:5]:  # Топ-5 ошибок
    percentage = count / len(y_test_original) * 100
    print(f"     {true_cls} → {pred_cls}: {count} раз ({percentage:.1f}%)")

# 6. Статистика по уверенности модели
print("\n   Анализ уверенности модели:")
print("   " + "-"*50)

# Максимальная вероятность для каждого предсказания
max_probs = np.max(predictions, axis=1)

# Разделяем на уверенные и неуверенные предсказания
thresholds = [0.7, 0.8, 0.9]
for threshold in thresholds:
    high_conf_mask = max_probs > threshold
    if np.any(high_conf_mask):
        high_conf_accuracy = np.mean(predictions_original[high_conf_mask] == y_test_original[high_conf_mask])
        high_conf_count = np.sum(high_conf_mask)
        percentage = high_conf_count / len(predictions) * 100
        
        print(f"     При уверенности > {threshold}:")
        print(f"       Точность: {high_conf_accuracy:.1%}")
        print(f"       Количество: {high_conf_count}/{len(predictions)} ({percentage:.1f}%)")
        print()

# 7. Визуализация распределения предсказаний
print("\n   Распределение предсказаний по классам:")
print("   " + "-"*50)

pred_counts = np.bincount(predictions_original - y.min(), minlength=num_classes)
true_counts = np.bincount(y_test_original - y.min(), minlength=num_classes)

print("   Класс | Предсказано | Фактически | Разница")
print("   " + "-"*40)

for cls_norm in range(num_classes):
    cls_orig = cls_norm + y.min()
    pred = pred_counts[cls_norm]
    true = true_counts[cls_norm]
    diff = pred - true
    
    if true > 0:  # Если есть примеры в тесте
        print(f"   {cls_orig:6} | {pred:11} | {true:10} | {diff:+6}")

print("\n" + "="*60)
print("5. ВЫВОДЫ И РЕКОМЕНДАЦИИ:")
print("="*60)

# Автоматический анализ
good_classes = []
bad_classes = []

for cls in classes:
    mask = y_test_original == cls
    if np.sum(mask) > 0:
        class_acc = np.mean(predictions_original[mask] == cls)
        if class_acc >= 0.6:
            good_classes.append((cls, class_acc))
        else:
            bad_classes.append((cls, class_acc))

if good_classes:
    print("\n   ХОРОШО ПРЕДСКАЗЫВАЕМЫЕ КЛАССЫ:")
    for cls, acc in sorted(good_classes, key=lambda x: x[1], reverse=True):
        print(f"     Класс {cls}: {acc:.1%}")

if bad_classes:
    print("\n   ПЛОХО ПРЕДСКАЗЫВАЕМЫЕ КЛАССЫ:")
    for cls, acc in sorted(bad_classes, key=lambda x: x[1]):
        print(f"     Класс {cls}: {acc:.1%}")
    
    print("\n   ПРИЧИНЫ ПЛОХОГО ПРЕДСКАЗАНИЯ:")
    print("     1. Мало данных для обучения (редкие классы)")
    print("     2. Классы похожи друг на друга")
    print("     3. Признаки слабо различают эти классы")

print("\n   РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:")
print("     1. Для редких классов собрать больше данных")
print("     2. Использовать oversampling (SMOTE) для балансировки")
print("     3. Добавить веса классов при обучении")
print("     4. Попробовать другую архитектуру модели")
print("     5. Объединить похожие или редкие классы")

print("\n" + "="*60)
print("6. ПРИМЕРЫ ОШИБОК:")
print("="*60)

# Показываем несколько примеров ошибок
error_indices = np.where(predictions_original != y_test_original)[0]
if len(error_indices) > 0:
    print("\n   Примеры ошибок (первые 5):")
    for i, idx in enumerate(error_indices[:5]):
        true_cls = y_test_original[idx]
        pred_cls = predictions_original[idx]
        confidence = np.max(predictions[idx])
        
        # Получаем топ-3 предсказанных классов
        top3_indices = np.argsort(predictions[idx])[-3:][::-1]
        top3_classes = top3_indices + y.min()
        top3_probs = predictions[idx][top3_indices]
        
        print(f"\n   Пример {i+1}:")
        print(f"     Фактический класс: {true_cls}")
        print(f"     Предсказанный класс: {pred_cls} (уверенность: {confidence:.2%})")
        print(f"     Ошибка: {pred_cls - true_cls:+d}")
        print(f"     Топ-3 предсказания: {list(zip(top3_classes, top3_probs.round(3)))}")
else:
    print("   Нет ошибок в предсказаниях!")
print()