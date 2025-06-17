import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, mean_squared_error

# Đọc dữ liệu
ratings = pd.read_csv("ratings.dat", sep="::", engine="python", names=["userId", "movieId", "rating", "timestamp"])
users = pd.read_csv("users.dat", sep="::", engine="python", names=["userId", "gender", "age", "occupation", "zipCode"])
movies = pd.read_csv("movies.dat", sep="::", engine="python", names=["movieId", "title", "genres"], encoding="latin1")

# Kiểm tra dữ liệu
print(ratings.head())

# Chuyển timestamp thành datetime
ratings["timestamp"] = pd.to_datetime(ratings["timestamp"], unit="s")

# Trích xuất thông tin thời gian
ratings["year"] = ratings["timestamp"].dt.year
ratings["month"] = ratings["timestamp"].dt.month
ratings["week"] = ratings["timestamp"].dt.isocalendar().week
ratings["day"] = ratings["timestamp"].dt.day
ratings["hour"] = ratings["timestamp"].dt.hour

# Hợp nhất dữ liệu
merged_df = ratings.merge(users, on="userId").merge(movies, on="movieId")

# 1️⃣ **Phân tích dữ liệu**
plt.figure(figsize=(10, 5))
sns.histplot(ratings["userId"].value_counts(), bins=50, kde=True)
plt.xlabel("Số lượng đánh giá")
plt.ylabel("Số lượng người dùng")
plt.title("Phân phối số lượng đánh giá của người dùng")
plt.show()

# Xu hướng đánh giá theo năm
plt.figure(figsize=(10, 5))
sns.lineplot(data=merged_df.groupby("year")["rating"].mean())
plt.xlabel("Năm")
plt.ylabel("Điểm đánh giá trung bình")
plt.title("Xu hướng đánh giá trung bình theo năm")
plt.show()

# Phân tích đánh giá theo độ tuổi và giới tính
plt.figure(figsize=(10, 5))
sns.boxplot(data=merged_df, x="age", y="rating", hue="gender")
plt.xlabel("Nhóm tuổi")
plt.ylabel("Đánh giá trung bình")
plt.title("Sở thích phim theo độ tuổi và giới tính")
plt.show()

# 2️⃣ **Tiền xử lý dữ liệu**
user_behavior = ratings.groupby('userId').agg({
    'movieId': 'count',   # Tổng số phim đã xem
    'rating': 'mean',     # Điểm trung bình đánh giá
    'year': 'max'         # Năm gần nhất xem phim
}).reset_index()

user_behavior.rename(columns={'movieId': 'Total_Movies_Watched', 'rating': 'Avg_Rating'}, inplace=True)

# 3️⃣ **Dự đoán Churn (Classification)**
user_behavior['Churn'] = (2025 - user_behavior['year'] > 2).astype(int)  # Người dùng không xem phim >2 năm bị xem là churn

X_class = user_behavior[['Total_Movies_Watched', 'Avg_Rating']]
y_class = user_behavior['Churn']
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_class, y_class, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_c = scaler.fit_transform(X_train_c)
X_test_c = scaler.transform(X_test_c)

clf = LogisticRegression()
clf.fit(X_train_c, y_train_c)
y_pred_c = clf.predict(X_test_c)

print("Classification Report:")
print(classification_report(y_test_c, y_pred_c))

# 4️⃣ **Dự báo số lần xem phim (Regression)**
X_reg = user_behavior[['Avg_Rating']]  # Sử dụng điểm đánh giá trung bình làm biến độc lập
y_reg = user_behavior['Total_Movies_Watched']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

regressor = LinearRegression()
regressor.fit(X_train_r, y_train_r)
y_pred_r = regressor.predict(X_test_r)

print("Mean Absolute Error:", mean_absolute_error(y_test_r, y_pred_r))
print("Mean Squared Error:", mean_squared_error(y_test_r, y_pred_r))

# 5️⃣ **Hiển thị phân bố churn**
plt.figure(figsize=(8,5))
sns.countplot(x=user_behavior['Churn'])
plt.title("Phân bố người dùng có khả năng rời bỏ")
plt.xlabel("Churn")
plt.ylabel("Số lượng")
plt.show()

