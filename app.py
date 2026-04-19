import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Công cụ So sánh Excel Tốc độ cao", layout="wide")

st.title("🚀 Công cụ So sánh Dữ liệu Excel")
st.markdown("""
Công cụ này giúp bạn so sánh 1 cột của file Gốc với toàn bộ dữ liệu 1 cột của file Đối chiếu. 
Nếu giá trị tồn tại, hệ thống sẽ điền **1** vào cột kết quả. Tối ưu cho dữ liệu lớn.
""")

# --- GIAO DIỆN UPLOAD ---
col1, col2 = st.columns(2)

with col1:
    file_goc = st.file_uploader("Upload File Gốc (File cần thêm cột kết quả)", type=['xlsx', 'csv'])

with col2:
    file_doi_chieu = st.file_uploader("Upload File Đối chiếu (File chứa danh sách mẫu)", type=['xlsx', 'csv'])

if file_goc and file_doi_chieu:
    # Đọc nhanh header để chọn cột
    try:
        df_goc_head = pd.read_excel(file_goc, nrows=1) if file_goc.name.endswith('xlsx') else pd.read_csv(file_goc, nrows=1)
        df_target_head = pd.read_excel(file_doi_chieu, nrows=1) if file_doi_chieu.name.endswith('xlsx') else pd.read_csv(file_doi_chieu, nrows=1)
        
        col_a, col_b = st.columns(2)
        with col_a:
            cot_goc = st.selectbox("Chọn cột ở File Gốc để kiểm tra:", df_goc_head.columns)
        with col_b:
            cot_doi_chieu = st.selectbox("Chọn cột ở File Đối chiếu để dò tìm:", df_target_head.columns)

        ten_cot_moi = st.text_input("Tên cột kết quả mới:", value="Trung_Khop")

        if st.button("Bắt đầu xử lý so sánh"):
            with st.spinner("Đang xử lý dữ liệu lớn... Vui lòng đợi trong giây lát."):
                # Đọc toàn bộ dữ liệu
                if file_goc.name.endswith('xlsx'):
                    df_goc = pd.read_excel(file_goc)
                else:
                    df_goc = pd.read_csv(file_goc)

                if file_doi_chieu.name.endswith('xlsx'):
                    df_target = pd.read_excel(file_doi_chieu, usecols=[cot_doi_chieu])
                else:
                    df_target = pd.read_csv(file_doi_chieu, usecols=[cot_doi_chieu])

                # Thuật toán tối ưu: Sử dụng Set để tìm kiếm O(1)
                # Chuyển cột đối chiếu thành set để tăng tốc độ tối đa
                set_doi_chieu = set(df_target[cot_doi_chieu].dropna().astype(str).unique())

                # So sánh và tạo cột mới
                df_goc[ten_cot_moi] = df_goc[cot_goc].astype(str).apply(
                    lambda x: 1 if x in set_doi_chieu else 0
                )

                st.success(f"Đã xử lý xong {len(df_goc)} dòng!")
                
                # Hiển thị xem trước
                st.write("Xem trước kết quả (5 dòng đầu):")
                st.dataframe(df_goc.head())

                # Tạo nút tải file
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_goc.to_excel(writer, index=False)
                
                st.download_button(
                    label="📥 Tải xuống File kết quả (Excel)",
                    data=output.getvalue(),
                    file_name="ket_qua_so_sanh.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"Có lỗi xảy ra: {e}")

else:
    st.info("Vui lòng upload cả 2 file để bắt đầu.")
