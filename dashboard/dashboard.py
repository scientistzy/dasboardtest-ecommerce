import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Pastikan script berjalan dari direktori yang sesuai
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Fungsi untuk membaca dataset dengan caching agar lebih cepat
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {file_path}")
        return None

# Load dataset
order_items_df = load_data("order_items_dataset.csv")
order_payments_df = load_data("order_payments_dataset.csv")

if order_items_df is not None and order_payments_df is not None:
    # Judul Dashboard
    st.title("📊 Dashboard Analisis Data E-Commerce")
    
    # Sidebar untuk filter
    st.sidebar.header("Filter Data")
    selected_payment = st.sidebar.selectbox("Pilih Metode Pembayaran", order_payments_df["payment_type"].unique())
    
    # Metode Pembayaran Paling Sering Digunakan
    st.subheader("Metode Pembayaran Paling Sering Digunakan")
    payment_counts = order_payments_df["payment_type"].value_counts()
    st.bar_chart(payment_counts)
    
    # Hubungan Jumlah Produk dalam Pesanan dengan Total Pembayaran
    st.subheader("Hubungan Jumlah Produk dalam Pesanan dengan Total Pembayaran")
    order_items_count = order_items_df.groupby("order_id")["order_item_id"].count().reset_index()
    order_items_count.rename(columns={"order_item_id": "total_items"}, inplace=True)
    
    payment_values = order_payments_df.groupby("order_id")["payment_value"].sum().reset_index()
    payment_values.rename(columns={"payment_value": "total_payment"}, inplace=True)
    
    # Gabungkan data
    order_payment_analysis = pd.merge(order_items_count, payment_values, on="order_id", how="inner")
    
    # Scatter Plot
    fig, ax = plt.subplots()
    sns.scatterplot(x=order_payment_analysis["total_items"], y=order_payment_analysis["total_payment"], alpha=0.5, ax=ax)
    ax.set_title("Hubungan Jumlah Produk dalam Pesanan dengan Total Pembayaran")
    ax.set_xlabel("Jumlah Produk")
    ax.set_ylabel("Total Pembayaran")
    st.pyplot(fig)
    
    # Filter berdasarkan metode pembayaran
    st.subheader(f"Total Pembayaran Berdasarkan {selected_payment}")
    filtered_data = order_payments_df[order_payments_df["payment_type"] == selected_payment]
    st.write(filtered_data[["order_id", "payment_value"]].head(10))
    
    st.write("Dashboard ini membantu memahami pola pembayaran dan hubungan jumlah produk dengan total pembayaran.")
else:
    st.error("Gagal memuat data. Pastikan file CSV tersedia di direktori yang benar.")