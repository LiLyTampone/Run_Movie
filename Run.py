import pandas as pd

# Đọc file CSV
df = pd.read_csv("movie_lens_1m.csv")

# Hiển thị 5 dòng đầu tiên
print(df.head())

df = df.drop(columns=["zip_code"])
print(df.head())  # Kiểm tra lại DataFrame sau khi loại bỏ cột

df["gender"] = df["gender"].map({"M": 1, "F": 0})
print(df.head())  # Kiểm tra kết quả sau khi chuyển đổi

# Xử lý thể loại phim (One-Hot Encoding)
df["genres"] = df["genres"].str.split("|")  # Tách thể loại
unique_genres = set(g for genre_list in df["genres"].dropna() for g in genre_list)
for genre in unique_genres:
    df[genre] = df["genres"].apply(lambda x: 1 if genre in x else 0)

df = df.sort_values(by="timestamp", ascending=True)  # Sắp xếp tăng dần
print(df.head()) 

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")  

# Tạo các cột mới từ timestamp
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["week"] = df["timestamp"].dt.isocalendar().week
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour
df["minute"] = df["timestamp"].dt.minute
df["second"] = df["timestamp"].dt.second

# Hiển thị DataFrame sau khi thêm cột
print(df.head())




