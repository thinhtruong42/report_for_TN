import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import io


# --- Hàm xử lý dữ liệu TikTok ---
def process_tiktok_data(df_new, ngay_bat_dau, ngay_ket_thuc):
    df_new.columns = df_new.columns.str.strip()  # chuẩn hóa tên cột

    df_new["SKU Category"] = df_new["Seller SKU"]
    df_new["SKU Category"] = df_new["SKU Category"].str.replace(
        r"^(COMBO-SC-ANHDUC|COMBO-SC-NGOCTRINH)", "COMBO-SC", regex=True
    )
    date_columns = [
        "Created Time",
        "Paid Time",
        "RTS Time",
        "Shipped Time",
        "Delivered Time",
        "Cancelled Time",
    ]

    # Ép kiểu về datetime
    df_new[date_columns] = df_new[date_columns].apply(
        lambda col: pd.to_datetime(col, errors="coerce", format="%d/%m/%Y %H:%M:%S")
    )

    # Loại bỏ giờ, giữ lại phần ngày (vẫn là kiểu datetime)
    for col in date_columns:
        df_new[col] = df_new[col].dt.normalize()

    tong_don = df_new[
        (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
    ]

    don_hoan_thanh_tiktok = df_new[
        (df_new["Order Substatus"] == "Completed")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
    ]

    don_hoan_thanh_tiktok_unique = don_hoan_thanh_tiktok["Order ID"].drop_duplicates()
    so_don_hoan_thanh_tiktok = len(don_hoan_thanh_tiktok_unique)
    tong_don_unique = tong_don["Order ID"].drop_duplicates()
    so_luong_tong_don = len(tong_don_unique)

    don_da_huy = df_new[
        (df_new["Order Substatus"] == "Canceled")
        & (df_new["Cancelled Time"] >= ngay_bat_dau)
        & (df_new["Cancelled Time"] <= ngay_ket_thuc)
    ]

    don_da_huy_unique = don_da_huy["Order ID"].drop_duplicates()
    so_don_da_huy = len(don_da_huy_unique)

    don_hoan_tra_tiktok = df_new[
        (df_new["Cancelation/Return Type"] == "Return/Refund")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
    ]
    don_hoan_tra_tiktok_unique = don_hoan_tra_tiktok["Order ID"].drop_duplicates()
    so_don_hoan_tra_tiktok = len(don_hoan_tra_tiktok_unique)

    don_hoan_tra_thuc_su_tiktok = df_new[
        (df_new["Cancelation/Return Type"] == "Return/Refund")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Sku Quantity of return"] != 0)
    ]
    don_hoan_tra_thuc_su_tiktok_unique = don_hoan_tra_thuc_su_tiktok[
        "Order ID"
    ].drop_duplicates()
    so_don_hoan_tra_thuc_su_tiktok = len(don_hoan_tra_thuc_su_tiktok_unique)

    don_da_giao_tiktok = df_new[
        (df_new["Order Substatus"] == "Delivered")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
    ]
    don_da_giao_tiktok_unique = don_da_giao_tiktok["Order ID"].drop_duplicates()
    so_don_da_giao_tiktok = len(don_da_giao_tiktok_unique)

    SCx1_tiktok_hoan_thanh = df_new[
        (df_new["SKU Category"] == "SC-450g")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Order Substatus"] == "Completed")
    ]

    SCx2_tiktok_hoan_thanh = df_new[
        (df_new["SKU Category"] == "SC-x2-450g")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Order Substatus"] == "Completed")
    ]

    SC_Combo_tiktok_hoan_thanh = df_new[
        (df_new["SKU Category"] == "COMBO-SC")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Order Substatus"] == "Completed")
    ]

    so_luong_SCx1_tiktok_hoan_thanh = SCx1_tiktok_hoan_thanh["Quantity"].sum()
    so_luong_SCx2_tiktok_hoan_thanh = SCx2_tiktok_hoan_thanh["Quantity"].sum()
    so_luong_SC_Combo_tiktok_hoan_thanh = SC_Combo_tiktok_hoan_thanh["Quantity"].sum()
    tong_san_pham_tiktok_hoan_thanh = (
        so_luong_SCx1_tiktok_hoan_thanh
        + so_luong_SCx2_tiktok_hoan_thanh
        + so_luong_SC_Combo_tiktok_hoan_thanh * 2
    )

    SCx1_tiktok_da_giao = df_new[
        (df_new["SKU Category"] == "SC-450g")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Order Substatus"] == "Delivered")
    ]

    SCx2_tiktok_da_giao = df_new[
        (df_new["SKU Category"] == "SC-x2-450g")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Order Substatus"] == "Delivered")
    ]

    SC_Combo_tiktok_da_giao = df_new[
        (df_new["SKU Category"] == "COMBO-SC")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Order Substatus"] == "Delivered")
    ]

    so_luong_SCx1_tiktok_da_giao = SCx1_tiktok_da_giao["Quantity"].sum()
    so_luong_SCx2_tiktok_da_giao = SCx2_tiktok_da_giao["Quantity"].sum()
    so_luong_SC_Combo_tiktok_da_giao = SC_Combo_tiktok_da_giao["Quantity"].sum()

    tong_san_pham_tiktok_da_giao = (
        so_luong_SCx1_tiktok_da_giao
        + so_luong_SCx2_tiktok_da_giao
        + so_luong_SC_Combo_tiktok_da_giao * 2
    )

    SCx1_tiktok_hoan_tra = df_new[
        (df_new["SKU Category"] == "SC-450g")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Cancelation/Return Type"] == "Return/Refund")
        & (df_new["Sku Quantity of return"] != 0)
    ]

    SCx2_tiktok_hoan_tra = df_new[
        (df_new["SKU Category"] == "SC-x2-450g")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Cancelation/Return Type"] == "Return/Refund")
        & (df_new["Sku Quantity of return"] != 0)
    ]

    SC_Combo_tiktok_hoan_tra = df_new[
        (df_new["SKU Category"] == "COMBO-SC")
        & (df_new["Delivered Time"] >= ngay_bat_dau)
        & (df_new["Delivered Time"] <= ngay_ket_thuc)
        & (df_new["Cancelation/Return Type"] == "Return/Refund")
        & (df_new["Sku Quantity of return"] != 0)
    ]

    so_luong_SCx1_tiktok_hoan_tra = SCx1_tiktok_hoan_tra["Quantity"].sum()
    so_luong_SCx2_tiktok_hoan_tra = SCx2_tiktok_hoan_tra["Quantity"].sum()
    so_luong_SC_Combo_tiktok_hoan_tra = SC_Combo_tiktok_hoan_tra["Quantity"].sum()

    tong_san_pham_tiktok_hoan_tra = (
        so_luong_SCx1_tiktok_hoan_tra
        + so_luong_SCx2_tiktok_hoan_tra
        + so_luong_SC_Combo_tiktok_hoan_tra * 2
    )

    return (
        tong_san_pham_tiktok_hoan_thanh,
        tong_san_pham_tiktok_da_giao,
        so_luong_SC_Combo_tiktok_hoan_thanh,
        so_luong_SC_Combo_tiktok_da_giao,
        so_luong_SCx1_tiktok_hoan_thanh,
        so_luong_SCx1_tiktok_da_giao,
        so_luong_SCx2_tiktok_hoan_thanh,
        so_luong_SCx2_tiktok_da_giao,
        so_don_da_giao_tiktok,
        so_don_hoan_thanh_tiktok,
        so_luong_SCx1_tiktok_hoan_tra,
        so_luong_SCx2_tiktok_hoan_tra,
        so_luong_SC_Combo_tiktok_hoan_tra,
        tong_san_pham_tiktok_hoan_tra,
        so_don_hoan_tra_tiktok,
        so_don_hoan_tra_thuc_su_tiktok,
    )


# --- Hàm xử lý dữ liệu Shopee ---
def process_shopee_data(df_shopee, ngay_bat_dau, ngay_ket_thuc):
    df_shopee.columns = df_shopee.columns.str.strip()

    df_shopee["Acctually type"] = df_shopee["Trạng Thái Đơn Hàng"]

    df_shopee["Acctually type"] = df_shopee["Acctually type"].apply(
        lambda x: (
            "Đơn hàng đã đến User"
            if isinstance(x, str) and "Người mua xác nhận đã nhận được hàng" in x
            else x
        )
    )

    date_columns_shopee = [
        "Ngày đặt hàng",
        "Ngày giao hàng dự kiến",
        "Ngày gửi hàng",
        "Thời gian giao hàng",
    ]

    # Ép kiểu về datetime với định dạng đúng
    df_shopee[date_columns_shopee] = df_shopee[date_columns_shopee].apply(
        lambda col: pd.to_datetime(col, errors="coerce", format="%Y-%m-%d %H:%M")
    )

    # Loại bỏ giờ, giữ lại phần ngày
    for col in date_columns_shopee:
        df_shopee[col] = df_shopee[col].dt.normalize()

    tong_don_shopee = df_shopee[
        (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
    ]
    tong_don_shopee_unique = tong_don_shopee["Mã đơn hàng"].drop_duplicates()
    so_luong_tong_don_shopee = len(tong_don_shopee_unique)

    don_hoan_thanh_shopee = df_shopee[
        (df_shopee["Acctually type"].isin(["Hoàn thành"]))
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
    ]
    don_hoan_thanh_shopee_unique = don_hoan_thanh_shopee[
        "Mã đơn hàng"
    ].drop_duplicates()
    so_don_hoan_thanh_shopee = len(don_hoan_thanh_shopee_unique)

    don_da_giao_shopee = df_shopee[
        (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"].isin(["Đã giao", "Đơn hàng đã đến User"]))
    ]

    don_da_giao_shopee_unique = don_da_giao_shopee["Mã đơn hàng"].drop_duplicates()
    so_don_da_giao_shopee = len(don_da_giao_shopee_unique)

    don_dang_giao_shopee = df_shopee[
        (df_shopee["Acctually type"] == "Đang giao")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
    ]
    don_dang_giao_shopee_unique = don_dang_giao_shopee["Mã đơn hàng"].drop_duplicates()
    so_don_dang_giao_shopee = len(don_dang_giao_shopee_unique)

    don_hoan_tra_shopee = df_shopee[
        (df_shopee["Trạng thái Trả hàng/Hoàn tiền"] == "Đã Chấp Thuận Yêu Cầu")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
    ]
    don_hoan_tra_shopee_unique = don_hoan_tra_shopee["Mã đơn hàng"].drop_duplicates()
    so_don_hoan_tra_shopee = len(don_hoan_tra_shopee_unique)

    SCx1_sp_hoanh_thanh = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"] == "Hoàn thành")
    ]

    SCx2_sp_hoanh_thanh = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-x2-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"] == "Hoàn thành")
    ]

    SC_Combo_sp_hoanh_thanh = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "COMBO-SC")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"] == "Hoàn thành")
    ]

    so_luong_SCx1_sp_hoanh_thanh = SCx1_sp_hoanh_thanh["Số lượng"].sum()
    so_luong_SCx2_sp_hoanh_thanh = SCx2_sp_hoanh_thanh["Số lượng"].sum()
    so_luong_SC_Combo_sp_hoanh_thanh = SC_Combo_sp_hoanh_thanh["Số lượng"].sum()

    tong_san_pham_sp_hoanh_thanh = (
        so_luong_SCx1_sp_hoanh_thanh
        + so_luong_SCx2_sp_hoanh_thanh
        + so_luong_SC_Combo_sp_hoanh_thanh * 2
    )

    SCx1_sp_da_giao = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"].isin(["Đã giao", "Đơn hàng đã đến User"]))
    ]

    SCx2_sp_da_giao = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-x2-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"].isin(["Đã giao", "Đơn hàng đã đến User"]))
    ]

    SC_Combo_sp_da_giao = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "COMBO-SC")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"].isin(["Đã giao", "Đơn hàng đã đến User"]))
    ]

    so_luong_SCx1_sp_da_giao = SCx1_sp_da_giao["Số lượng"].sum()
    so_luong_SCx2_sp_da_giao = SCx2_sp_da_giao["Số lượng"].sum()
    so_luong_SC_Combo_sp_da_giao = SC_Combo_sp_da_giao["Số lượng"].sum()
    tong_san_pham_sp_da_giao = (
        so_luong_SCx1_sp_da_giao
        + so_luong_SCx2_sp_da_giao
        + so_luong_SC_Combo_sp_da_giao * 2
    )

    SCx1_sp_da_huy = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"] == "Đã hủy")
    ]

    SCx2_sp_da_huy = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-x2-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"] == "Đã hủy")
    ]

    SC_Combo_sp_da_huy = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "COMBO-SC")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Acctually type"] == "Đã hủy")
    ]

    so_luong_SCx1_sp_da_huy = SCx1_sp_da_huy["Số lượng"].sum()
    so_luong_SCx2_sp_da_huy = SCx2_sp_da_huy["Số lượng"].sum()
    so_luong_SC_Combo_sp_da_huy = SC_Combo_sp_da_huy["Số lượng"].sum()
    tong_san_pham_sp_da_huy = (
        so_luong_SCx1_sp_da_huy
        + so_luong_SCx2_sp_da_huy
        + so_luong_SC_Combo_sp_da_huy * 2
    )

    SCx1_sp_hoan_tra = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Trạng thái Trả hàng/Hoàn tiền"] == "Đã Chấp Thuận Yêu Cầu")
    ]

    SCx2_sp_hoan_tra = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "SC-x2-450g")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Trạng thái Trả hàng/Hoàn tiền"] == "Đã Chấp Thuận Yêu Cầu")
    ]

    SC_Combo_sp_hoan_tra = df_shopee[
        (df_shopee["SKU phân loại hàng"] == "COMBO-SC")
        & (df_shopee["Thời gian giao hàng"] >= ngay_bat_dau)
        & (df_shopee["Thời gian giao hàng"] <= ngay_ket_thuc)
        & (df_shopee["Trạng thái Trả hàng/Hoàn tiền"] == "Đã Chấp Thuận Yêu Cầu")
    ]

    so_luong_SCx1_sp_hoan_tra = SCx1_sp_hoan_tra["Số lượng"].sum()
    so_luong_SCx2_sp_hoan_tra = SCx2_sp_hoan_tra["Số lượng"].sum()
    so_luong_SC_Combo_sp_hoan = SC_Combo_sp_hoan_tra["Số lượng"].sum()
    tong_san_pham_sp_hoan_tra = (
        so_luong_SCx1_sp_hoan_tra
        + so_luong_SCx2_sp_hoan_tra
        + so_luong_SC_Combo_sp_hoan * 2
    )

    return (
        tong_san_pham_sp_hoanh_thanh,
        tong_san_pham_sp_da_giao,
        so_luong_SC_Combo_sp_hoanh_thanh,
        so_luong_SC_Combo_sp_da_giao,
        so_luong_SCx1_sp_hoanh_thanh,
        so_luong_SCx1_sp_da_giao,
        so_luong_SCx2_sp_hoanh_thanh,
        so_luong_SCx2_sp_da_giao,
        so_don_dang_giao_shopee,
        so_don_hoan_thanh_shopee,
        so_don_hoan_tra_shopee,
        tong_san_pham_sp_hoan_tra,
        so_don_da_giao_shopee,
    )


# --- Giao diện Streamlit ---
st.set_page_config(page_title="Báo Cáo Đơn Hàng", layout="wide")
st.markdown(
    "<h1 style='text-align: center;'>📦 Báo Cáo Số Lượng Đơn Hàng Và Sản Phẩm TikTok & Shopee</h1>",
    unsafe_allow_html=True,
)

st.markdown("<br><br>", unsafe_allow_html=True)  # Tạo khoảng cách sau tiêu đề

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<h3 style='text-align: center;'>📥 Upload file TikTok</h3>",
        unsafe_allow_html=True,
    )
    file_tiktok = st.file_uploader("", type=["xlsx", "xls"], key="tiktok_file")

with col2:
    st.markdown(
        "<h3 style='text-align: center;'>📥 Upload file Shopee</h3>",
        unsafe_allow_html=True,
    )
    file_shopee = st.file_uploader("", type=["xlsx", "xls"], key="shopee_file")


ngay_bat_dau = st.date_input("📅 Ngày bắt đầu", value=datetime.now().date())
ngay_ket_thuc = st.date_input("📅 Ngày kết thúc", value=datetime.now().date())

ngay_bat_dau = pd.to_datetime(ngay_bat_dau)
ngay_ket_thuc = pd.to_datetime(ngay_ket_thuc)

# Khởi tạo trạng thái nếu chưa có
if "processing" not in st.session_state:
    st.session_state.processing = False

# Nút xử lý
process_btn = st.button("🔍 Xử lý dữ liệu", disabled=st.session_state.processing)

if process_btn:
    if not file_tiktok or not file_shopee:
        st.warning("Vui lòng upload cả 2 file!")
    else:
        with st.spinner("⏳ Đang xử lý dữ liệu, vui lòng chờ..."):
            df_tiktok = pd.read_excel(file_tiktok)
            df_shopee = pd.read_excel(file_shopee)

            (
                tong_san_pham_tiktok_hoan_thanh,
                tong_san_pham_tiktok_da_giao,
                so_luong_SC_Combo_tiktok_hoan_thanh,
                so_luong_SC_Combo_tiktok_da_giao,
                so_luong_SCx1_tiktok_hoan_thanh,
                so_luong_SCx1_tiktok_da_giao,
                so_luong_SCx2_tiktok_hoan_thanh,
                so_luong_SCx2_tiktok_da_giao,
                so_don_da_giao_tiktok,
                so_don_hoan_thanh_tiktok,
                so_luong_SCx1_tiktok_hoan_tra,
                so_luong_SCx2_tiktok_hoan_tra,
                so_luong_SC_Combo_tiktok_hoan_tra,
                tong_san_pham_tiktok_hoan_tra,
                so_don_hoan_tra_tiktok,
                so_don_hoan_tra_thuc_su_tiktok,
            ) = process_tiktok_data(df_tiktok, ngay_bat_dau, ngay_ket_thuc)

            (
                tong_san_pham_sp_hoanh_thanh,
                tong_san_pham_sp_da_giao,
                so_luong_SC_Combo_sp_hoanh_thanh,
                so_luong_SC_Combo_sp_da_giao,
                so_luong_SCx1_sp_hoanh_thanh,
                so_luong_SCx1_sp_da_giao,
                so_luong_SCx2_sp_hoanh_thanh,
                so_luong_SCx2_sp_da_giao,
                so_don_dang_giao_shopee,
                so_don_hoan_thanh_shopee,
                so_don_hoan_tra_shopee,
                tong_san_pham_sp_hoan_tra,
                so_don_da_giao_shopee,
            ) = process_shopee_data(df_shopee, ngay_bat_dau, ngay_ket_thuc)

            bang_thong_ke_don_hang_tiktok = pd.DataFrame(
                {
                    "TỔNG SỐ LƯỢNG SP": [
                        tong_san_pham_tiktok_hoan_thanh + tong_san_pham_tiktok_da_giao
                    ],
                    "SL SP HOÀN THÀNH": [tong_san_pham_tiktok_hoan_thanh],
                    "SL SP ĐÃ GIAO": [tong_san_pham_tiktok_da_giao],
                },
                index=["Tiktok"],
            )

            bang_thong_ke_so_luong_tiktok = pd.DataFrame(
                {
                    "SC_Combo": [
                        (
                            so_luong_SC_Combo_tiktok_hoan_thanh
                            + so_luong_SC_Combo_tiktok_da_giao
                        )
                        * 2
                    ],
                    "SCx1": [
                        so_luong_SCx1_tiktok_hoan_thanh + so_luong_SCx1_tiktok_da_giao
                    ],
                    "SCx2": [
                        so_luong_SCx2_tiktok_hoan_thanh + so_luong_SCx2_tiktok_da_giao
                    ],
                    "TỔNG": [
                        tong_san_pham_tiktok_hoan_thanh + tong_san_pham_tiktok_da_giao
                    ],
                    "ĐƠN ĐÃ GIAO": [so_don_da_giao_tiktok],
                    "ĐƠN HOÀN THÀNH": [so_don_hoan_thanh_tiktok],
                },
                index=["Tiktok"],
            )

            bang_thong_ke_don_hang_shopee = pd.DataFrame(
                {
                    "TỔNG SỐ LƯỢNG SP": [
                        tong_san_pham_sp_hoanh_thanh + tong_san_pham_sp_da_giao
                    ],
                    "SL SP HOÀN THÀNH": [tong_san_pham_sp_hoanh_thanh],
                    "SL SP ĐÃ GIAO": [tong_san_pham_sp_da_giao],
                },
                index=["Shopee"],
            )

            bang_thong_ke_so_luong_shopee = pd.DataFrame(
                {
                    "SC_Combo": [
                        (
                            so_luong_SC_Combo_sp_hoanh_thanh
                            + so_luong_SC_Combo_sp_da_giao
                        )
                        * 2
                    ],
                    "SCx1": [so_luong_SCx1_sp_hoanh_thanh + so_luong_SCx1_sp_da_giao],
                    "SCx2": [so_luong_SCx2_sp_hoanh_thanh + so_luong_SCx2_sp_da_giao],
                    "TỔNG": [tong_san_pham_sp_hoanh_thanh + tong_san_pham_sp_da_giao],
                    "ĐƠN ĐÃ GIAO": [so_don_da_giao_shopee],
                    "ĐƠN HOÀN THÀNH": [so_don_hoan_thanh_shopee],
                },
                index=["Shopee"],
            )

            bang_thong_ke_hoan_tra_shopee = pd.DataFrame(
                {
                    "SỐ ĐƠN HOÀN TRẢ": [so_don_hoan_tra_shopee],
                    "SỐ LƯỢNG SẢN PHẨM": [tong_san_pham_sp_hoan_tra],
                },
                index=["Shopee"],
            )
            bang_thong_ke_hoan_tra_tiktok = pd.DataFrame(
                {
                    "SỐ ĐƠN HOÀN TRẢ": [so_don_hoan_tra_thuc_su_tiktok],
                    "SỐ LƯỢNG SẢN PHẨM": [tong_san_pham_tiktok_hoan_tra],
                },
                index=["Tiktok"],
            )

            bang_thong_ke_so_luong = pd.concat(
                [bang_thong_ke_so_luong_tiktok, bang_thong_ke_so_luong_shopee]
            )

            bang_thong_ke_don_hang = pd.concat(
                [bang_thong_ke_don_hang_tiktok, bang_thong_ke_don_hang_shopee]
            )

            bang_thong_ke_hoan_tra = pd.concat(
                [bang_thong_ke_hoan_tra_tiktok, bang_thong_ke_hoan_tra_shopee]
            )
            labels = ["SC_Combo", "SCx1", "SCx2"]

            # TikTok Pie Chart
            tiktok_values = bang_thong_ke_so_luong.loc["Tiktok", labels].values
            fig_pie_tiktok = px.pie(
                names=labels,
                values=tiktok_values,
                title="Tỉ lệ loại sản phẩm TikTok",
                hole=0.4,
            )

            # Shopee Pie Chart
            shopee_values = bang_thong_ke_so_luong.loc["Shopee", labels].values
            fig_pie_shopee = px.pie(
                names=labels,
                values=shopee_values,
                title="Tỉ lệ loại sản phẩm Shopee",
                hole=0.4,
            )

            df_don_hang = bang_thong_ke_don_hang.reset_index().rename(
                columns={"index": "Nền tảng"}
            )

            # Vẽ biểu đồ cột
            # Vẽ biểu đồ cột Tổng Quan Đơn Hàng TikTok & Shopee
            fig_bar_don_hang = px.bar(
                df_don_hang,
                x="Nền tảng",
                y=["SL SP HOÀN THÀNH", "SL SP ĐÃ GIAO"],
                barmode="group",
                title="📊 Tổng Quan Đơn Hàng Theo Nền Tảng",
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_bar_don_hang.update_yaxes(tickformat=",.0f")

            df_hoan_tra = bang_thong_ke_hoan_tra.reset_index().rename(
                columns={"index": "Nền tảng"}
            )

            fig_bar_hoan_tra = px.bar(
                df_hoan_tra,
                x="Nền tảng",
                y=["SỐ ĐƠN HOÀN TRẢ", "SỐ LƯỢNG SẢN PHẨM"],
                barmode="group",
                title="📊 Thống Kê Đơn Hoàn Trả Theo Nền Tảng",
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Set2,
            )

            # Hiển thị bảng thống kê đơn hàng

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### 📋 Bảng Thống Kê")
                st.markdown("#### 📦 Thống Kê Theo Loại Sản Phẩm")
                st.dataframe(bang_thong_ke_so_luong)

            with col2:
                st.markdown("#### 📈 Biểu Đồ")
                st.plotly_chart(fig_pie_tiktok, use_container_width=True)

            with col3:
                st.markdown("#### 📈 Biểu Đồ")
                st.plotly_chart(fig_pie_shopee, use_container_width=True)

            # --- Gộp Bảng và Biểu đồ Đơn Hàng Hoàn Trả ---
            st.markdown("### 📊 Đơn Hàng Hoàn Trả Tiktok & Shopee")
            col4, col5 = st.columns(2)

            with col4:
                st.markdown("#### 📋 Bảng Thống Kê")
                st.dataframe(bang_thong_ke_hoan_tra)

            with col5:
                st.markdown("#### 📈 Biểu Đồ")
                st.plotly_chart(fig_bar_hoan_tra, use_container_width=True)

            # --- Gộp Bảng và Biểu đồ Đơn Hàng Hoàn Thành / Đã Giao ---
            st.markdown("### 📊 Tổng Quan Đơn Hàng Tiktok & Shopee")
            col6, col7 = st.columns(2)

            with col6:
                st.markdown("#### 📋 Bảng Thống Kê")
                st.dataframe(bang_thong_ke_don_hang)

            with col7:
                st.markdown("#### 📈 Biểu Đồ")
                st.plotly_chart(fig_bar_don_hang, use_container_width=True)

        st.success("✅ Xử lý dữ liệu thành công!")
