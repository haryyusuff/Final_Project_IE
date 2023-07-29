#import library
import pandas as pd
import plotly.express as px
import streamlit as st

#configuration dashboard
st.set_page_config(
                page_title="Sales Dashboard",
                page_icon=":chart_with_upwards_trend:",
                layout="wide"
            )

#read dataframe
df = pd.read_excel(
        io="Association_Rules.xlsx",
        engine="openpyxl",
        sheet_name="data_clean",
        nrows=999999
    )

dt = pd.read_excel(
        io="Association_Rules.xlsx",
        engine="openpyxl",
        sheet_name="data_transaction",
        nrows=999999
    )

fr = pd.read_excel(
        io="Association_Rules.xlsx",
        engine="openpyxl",
        sheet_name="frequent_items",
        nrows=999999
    )

ar = pd.read_excel(
        io="Association_Rules.xlsx",
        engine="openpyxl",
        sheet_name="association_rules",
        nrows=999999
    )

rl = pd.read_excel(
        io="Association_Rules.xlsx",
        engine="openpyxl",
        sheet_name="rules",
        nrows=999999
    )

best_ar = pd.read_excel(
        io="Association_Rules.xlsx",
        engine="openpyxl",
        sheet_name="best_ar",
        nrows=999999
    )

#sidebar dashboard
st.sidebar.header("Dashboard Analytics")
item = st.sidebar.multiselect(
    "Jenis Item:",
    options=df["Item"].unique(),
    default=df["Item"].unique()
)

#header dashboard
st.header("**Dashboard Penjualan _:blue[Produk Bakery]_ :bread:**")
st.markdown("##")

#key performance indicator
total_trx = int(df["Transaction"].max())
total_items_sold = int(fr["Total"].sum())
best_seller = str("Coffee")

a1, a2, a3 = st.columns(3)
with a1:
    st.subheader("Total Transaksi")
    st.subheader(f":pushpin: :blue[{total_trx:,}]")
with a2:
    st.subheader("Total Item Terjual")
    st.subheader(f":pushpin: :blue[{total_items_sold:,} pcs]")
with a3:
    st.subheader("Item Best Seller")
    st.subheader(f":pushpin: :blue[{best_seller}]")

st.markdown("##")
st.subheader("Total Penjualan per Item")

#total penjualan seluruh items
b = st.container()
with b:
    fig_all_items = px.bar(
        data_frame = fr,
        x = fr["Item"],
        y = fr["Total"],
        color = fr["Item"],
        height = 500
    )
    fig_all_items.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
b.plotly_chart(fig_all_items, use_container_width=True)
st.write("**:green[#Note:]**")
st.write("**-Pencatatan data transaksi dimulai dari tanggal :blue[10/30/2016] sampai :blue[4/9/2017], yang berjumlah :blue[162 hari]**")
st.write("**-Memiliki :blue[86 jenis item] yang dijual**")

#tabel dataset
st.markdown("##")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Tabel Dataset Penjualan")
    st.dataframe(df, use_container_width=True)
with c2:
    st.subheader("Tabel Transaksi")
    st.dataframe(dt, use_container_width=True)

#scatter plot
st.markdown("##")
st.subheader("Scatter Plot Association Rules")
d = st.container()
with d:
    fig_rl = px.scatter(
        data_frame = rl,
        x = 'Support',
        y = 'Confidence',
        # z = 'Lift Ratio',
        color = 'Lift Ratio',
        hover_name = 'Rules'
    )
d.plotly_chart(fig_rl, use_container_width=True)
st.markdown("**:green[#Note:]**")
st.write("**-Nilai minimum :blue[support = 0.02]**")
st.write("**-Nilai minimum :blue[lift ratio = 1]**")
st.write("**-Nilai minimum :blue[confidence = 0.7]**")

#tabel association rules
st.markdown("##")
st.subheader("Tabel Association Rules")
st.dataframe(ar, use_container_width=True)

st.subheader("Tabel Association Rules Terbaik")
st.dataframe(best_ar, use_container_width=True)
st.write("**:green[#Note:]**")
st.write("**-Antecedents = Item A**")
st.write("**-Consequents = Item B**")
st.write("**-Rules = :blue[Jika membeli A, maka akan membeli B]**")