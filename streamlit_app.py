from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BookFlow | B2B Dashboard", page_icon="📚", layout="wide")
st.title("📚 BookFlow | B2B Sales Intelligence")
st.caption("ISL 467E · B2B book distributor · 2020 transactions")

DATA_FILE = Path(__file__).resolve().parent / "data" / "B2B_Transaction_Data_.xlsx"

@st.cache_data(show_spinner="Excel verisi okunuyor...")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Category"] = df["Category"].fillna("Unknown").astype(str).str.strip()
    return df

if not DATA_FILE.exists():
    st.error("Excel dosyası bulunamadı. B2B_Transaction_Data_.xlsx dosyasını data/ klasörüne koyun.")
    st.stop()

try:
    df = load_data(str(DATA_FILE))
except Exception as exc:
    st.error(f"Veri okunamadı: {exc}")
    st.stop()

st.sidebar.header("Filters")
categories = sorted(df["Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Category", categories)
if selected_categories:
    df = df.loc[df["Category"].isin(selected_categories)].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transaction rows", f"{len(df):,}")
c2.metric("Invoices", f"{df['InvoiceNo'].nunique():,}")
c3.metric("Customers", f"{df['CustomerID'].nunique():,}")
c4.metric("Products", f"{df['StockCode'].nunique():,}")

st.subheader("Monthly transaction volume")
monthly = (df.dropna(subset=["InvoiceDate"])
           .assign(Month=lambda x: x["InvoiceDate"].dt.to_period("M").dt.to_timestamp())
           .groupby("Month").size().rename("Transaction rows"))
st.line_chart(monthly)

st.subheader("Top 10 categories by transaction rows")
top_categories = df["Category"].value_counts().head(10)
st.bar_chart(top_categories)

with st.expander("Preview data & data quality"):
    st.write("First 20 rows")
    st.dataframe(df.head(20), use_container_width=True)
    st.write("Missing values")
    st.dataframe(df.isna().sum().rename("Missing rows"), use_container_width=True)

st.info("Bu ilk sürüm işlem sayısını gösterir. Ciro ve satış tutarını, NetPrice alanının anlamını doğruladıktan sonra ekleyeceğiz.")
