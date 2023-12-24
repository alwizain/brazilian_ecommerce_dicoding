# Import Library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur judul web
st.markdown("<h1 style='text-align: center;'>Brazilian E-Commerce Insights</h1>", unsafe_allow_html=True)

# Membaca file dataset
df_orderitems = pd.read_csv("\Lenovo Ideapad Gaming\IDCamp\Dashboard\orderitems.csv")
df_orders = pd.read_csv("\Lenovo Ideapad Gaming\IDCamp\Dashboard\orders.csv")

# VISUALISASI 1 #
st.subheader("Perbandingan Penjualan Setiap Bulan pada Tahun 2017 dengan 2018")
fig = plt.figure(figsize=[15, 8])

# Mendefinisikan total penjualan berdasarkan setiap bulannya
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
df_orders['monthx'] = df_orders['order_purchase_timestamp'].dt.strftime('%m')
df_orders['year'] = df_orders['order_purchase_timestamp'].dt.year
df_month_orders = df_orders.groupby(by=["monthx","year"])['order_id'].nunique().reset_index()
df_month_orders["monthx"] = df_month_orders["monthx"].astype(int)
df_month_orders = df_month_orders[df_month_orders["monthx"] < 9]

# Mendefinisikan nama bulan
month_names = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August'
}

df_month_orders['month_names'] = df_month_orders['monthx'].map(month_names)

# Mendefinisikan warna visualisasi
custom_palette = ["#2D9596", "#265073"]
sns.set(style="whitegrid")

# Mendefinisikan visualisasi yang akan dibuat
sns.barplot(x='month_names', y='order_id', hue='year', data=df_month_orders, palette = custom_palette)

# Mendefinisikan judul pada label x dan y
plt.ylabel("Total Order")
plt.xlabel("Month")

# Menampilkan plot visualisasi
st.pyplot(fig)



# VISUALISASI 2 #
st.subheader("Kenaikan Penjualan Setiap Bulan")

# Mengatur ukuran visualisasi
fig = plt.figure(figsize=(20, 6))

# Mengelompokkan bulan dan tahun berdasarkan total order
df_month =  df_orders.groupby(by=["month","year"]).order_id.nunique().reset_index()
df_month["month"] = pd.to_datetime(df_month["month"], format='%m-%Y')

# Mendefinisikan visualisasi yang akan dibuat
ax = sns.lineplot(x='month', y='order_id', data=df_month, estimator=None, linewidth=3)
ax.set(xticks=df_month.month.values)

# Mendefinisikan judul visualisasi
plt.title("Orders Rate Every Month", loc="center", fontsize=18)

# Mendefinisikan judul pada label x dan y
plt.ylabel("Total Orders")
plt.xlabel(None)

# Mengatur grid (garis bantu)
ax.grid(True)

# Mengatur label x agar tidak menyatu
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

# Menambahkan tanda nilai tertinggi
max_order = df_month['order_id'].max()
max_month = df_month.loc[df_month['order_id'].idxmax(), 'month']
plt.axvline(x=max_month, color='r', linestyle='--', label=f'Max Order: {max_order}')
plt.legend()

# Menampilkan plot visualisasi
sns.despine()
st.pyplot(fig)



# VISUALISASI 3 #
st.subheader("Distribusi Tipe Payment")
fig = plt.figure(figsize=[14, 7])

# Mengelompokkan payment type berdasarkan jumlah order
df_payment_type = df_orders.groupby(by="payment_type")["order_id"].nunique().reset_index()

# Mendefinisikan warna visualisasi
color = sns.color_palette('Paired') 

# Mendefinisikan visualisasi yang akan dibuat
plt.pie(df_payment_type["order_id"], labels=df_payment_type["payment_type"], colors=color, autopct='%.0f%%')

# Mendefinisikan judul visualisasi
plt.title("Payment Type Distribution")

# Menampilkan plot visualisasi
sns.despine()
st.pyplot(fig)



# VISUALISASI 4 #
st.subheader("Rata-Rata Payment Value pada Bulan November Berdasarkan Tipe Payment")
fig = plt.figure(figsize=[10, 5])

df_payment_value = df_orders[df_orders.order_purchase_timestamp.dt.month == 11].groupby(by="payment_type")["payment_value"].mean().reset_index()

# Mendefinisikan varna bar
colors = ["#E3F4F4", "#7286D3", "#E3F4F4", "#E3F4F4"]

# Mendefinisikan sumbu x dan y
sns.barplot(x='payment_type', y='payment_value', data=df_payment_value, palette=colors)

# Mendefinisikan judul visualisasi
plt.title('Average Payment Value in November by Payment Type')

# Mendefinisikan label pada sumbu X
plt.xlabel('Payment Type')

# Mendefinisikan label pada sumbu Y
plt.ylabel('Average Payment Value')

# Menampilkan plot visualisasi
sns.despine()
st.pyplot(fig)



# VISUALISASI 5 #
st.subheader("Kategori Barang yang Sering dan Sedikit Dibeli")

df_category = df_orderitems.groupby(by="product_category_name_english")["product_id"].count().reset_index()
df_category = df_category.rename(columns={"product_category_name_english": "category_name", "product_id": "total_orders"})

# Mendefinisikan tata letak
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))

# Mendefinisikan warna bar
colors = ["#7286D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Mendefinisikan penjualan yang paling sedikit dibeli
sns.barplot(x="total_orders", y="category_name", data=df_category.sort_values(by="total_orders", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel('Category Name')
ax[0].set_xlabel('Total Orders')
ax[0].set_title("Least Purchased Categories", loc="center", fontsize=30)
ax[0].tick_params(axis ='y', labelsize=20)

# Mendefinisikan penjualan yang paling sering dibeli
sns.barplot(x="total_orders", y="category_name", data=df_category.sort_values(by="total_orders", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel('Category Name')
ax[1].set_xlabel('Total Orders')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Frequently Purchased Category", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=20)

# Mendefinisikan judul visualisasi
plt.suptitle("Most and Last Purchased Item Categories", fontsize=40)

# Menampilkan plot visualisasi
sns.despine()
st.pyplot(fig)


# KESIMPULAN #
st.markdown("<br><br><h3>Kesimpulan</h3>", unsafe_allow_html=True)
st.markdown("<h4>1. Bagaimana perbandingan penjualan setiap bulan pada tahun 2017 dengan 2018?</h4>", unsafe_allow_html=True) 
st.markdown("<h4>Perbandingan penjualan setiap bulan antara 2017 dengan 2018 memiliki kenaikan yang signifikan yaitu sebesar 135%.</h4>", unsafe_allow_html=True)
st.markdown("<h4>2. Pada bulan apa yang memiliki tingkat penjualan tertinggi?</h4>", unsafe_allow_html=True)
st.markdown("<h4>Pada bulan November 2017 merupakan tingkat penjualan tertinggi yang diperoleh perusahaan dengan total sebanyak 7544 penjualan.</h4>", unsafe_allow_html=True)
st.markdown("<h4>3. Tipe transaksi apa yang sering digunakan?</h4>", unsafe_allow_html=True)
st.markdown("<h4>Tipe transaksi yang sering digunakan adalah credit card dengan penggunaan sebesar 75% dari total tipe transaksi yang digunakan.</h4>", unsafe_allow_html=True)
st.markdown("<h4>4. Berapa rata-rata payment value pada bulan yang memiliki tingkat penjualan tertinggi?</h4>", unsafe_allow_html=True)
st.markdown("<h4>Rata-rata payment value pada bulan yang memiliki tingkat penjualan tertinggi yaitu terdapat pada tipe transaksi credit card dengan rata-rata sebesar 159.887514.</h4>", unsafe_allow_html=True)
st.markdown("<h4>5. Kategori barang apa yang paling sering dan sedikit dibeli?</h4>", unsafe_allow_html=True)
st.markdown("<h4>Kategori yang paling sering dibeli adalah bed_bath_table, sedangkan untuk kategori yang sedikit dibeli adalah security_and_services.</h4>", unsafe_allow_html=True)
