import streamlit as st
import pandas as pd
import io
import string

# Hàm chuyển đổi số thứ tự cột thành chữ cái Excel (0 -> A, 1 -> B, ...)
def column_index_to_letter(n):
    result = ""
    while n >= 0:
        result = chr(n % 26 + 65) + result
        n = n // 26 - 1
    return result

st.set_page_config(page_title="So sánh Excel chuyên nghiệp", layout="wide")

st.title("🚀 Công cụ So sánh Excel (Tọa độ A, B, C)")
st.markdown("So sánh một ô ở cột file Gốc với **toàn bộ cột** ở file Đối chiếu. Kết quả trả về 1 nếu tìm thấy.")

# Cấu hình thanh bên để tùy chỉnh hàng bắt đầu
with st.sidebar:
    st.header("Cấu hình dòng")
    skip_rows_goc = st.number_input("File Gốc: Bỏ qua bao nhiêu dòng đầu?", min_value=0, value=0)
    skip_rows_doi_chieu = st.number_input("File Đối chiếu: Bỏ qua bao nhiêu dòng đầu?", min_value=0, value=0)

col1, col2 = st.columns(2)

with col1:
    file_goc = st.file_uploader("Upload File Gốc (File chính)", type=['xlsx', 'csv'])

with col2:
    file_doi_chieu = st.file_uploader("Upload File Đối chiếu (File danh mục)", type=['xlsx', 'csv'])

if file_goc and file_doi_chieu:
    try:
        # Đọc dữ liệu tạm để lấy số lượng cột
        if file_goc.name.endswith('xlsx'):
            df_goc_preview = pd.read_excel(file_goc, nrows=1, skiprows=skip_rows_goc, header=None)
        else:
            df_goc_preview = pd.read_csv(file_goc, nrows=1, skiprows=skip_rows_goc, header=None)
            
        if file_doi_chieu.name.endswith('xlsx'):
            df_target_preview = pd.read_excel(file_doi_chieu, nrows=1, skiprows=skip_rows_doi_chieu, header=None)
        else:
            df_target_preview = pd.read_csv(file_doi_chieu, nrows=1, skiprows=skip_rows_doi_chieu, header=None)

        # Tạo danh sách tên cột dạng: Cột A, Cột B, Cột C...
        cols_goc = [f"Cột {column_index_to_letter(i)}" for i in range(len(df_goc_preview.columns))]
        cols_doi_chieu = [f"Cột {column_index_to_letter(i)}" for i in range(len(df_target_preview.columns))]

        c_a, c_b = st.columns(2)
        with c_a:
            chon_cot_goc = st.selectbox("Chọn cột so sánh (File Gốc):", options=range(len(cols_goc)), format_func=lambda x: cols_goc[x])
        with c_b:
            chon_cot_doi_chieu = st.selectbox("Chọn cột đối chiếu (File Đối chiếu):", options=range(len(cols_doi_chieu)), format_func=lambda x: cols_doi_chieu[x])

        if st.button("⚡ Chạy so sánh dữ liệu"):
            with st.spinner("Đang tải dữ liệu và so sánh..."):
                # Đọc dữ liệu thật
                if file_goc.name.endswith('xlsx'):
                    df_goc = pd.read_excel(file_goc, skiprows=skip_rows_goc, header=None)
                else:
                    df_goc = pd.read_csv(file_goc, skiprows=skip_rows_goc, header=None)

                if file_doi_chieu.name.endswith('xlsx'):
                    df_target = pd.read_excel(file_doi_chieu, usecols=[chon_cot_doi_chieu], skiprows=skip_rows_doi_chieu, header=None)
                else:
                    df_target = pd.read_csv(file_doi_chieu, usecols=[chon_cot_doi_chieu], skiprows=skip_rows_doi_chieu, header=None)

                # Chuyển cột đối chiếu thành set để tối ưu tốc độ (O(1))
                # Lấy cột theo index (vị trí)
                danh_sach_mau = set(df_target.iloc[:, 0].dropna().astype(str).unique())
                
                # So sánh: lấy giá trị tại cột đã chọn, ép kiểu string, kiểm tra trong set
                df_goc['Ket_Qua'] = df_goc.iloc[:, chon_cot_goc].astype(str).apply(
                    lambda x: 1 if x in danh_sach_mau else 0
                )

                # Đổi tên các cột lại thành A, B, C cho người dùng dễ nhìn
                df_goc.columns = [column_index_to_letter(i) if i < len(df_goc.columns)-1 else "KẾT QUẢ" for i in range(len(df_goc.columns))]

                st.success("Đã so sánh xong!")
                st.dataframe(df_goc.head(10)) # Hiển thị 10 dòng đầu

                # Xuất file
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_goc.to_excel(writer, index=False)
                
                st.download_button(
                    label="📥 Tải file kết quả về máy",
                    data=output.getvalue(),
                    file_name="ket_qua_doi_soat.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"Lỗi: {e}. Vui lòng kiểm tra lại định dạng file.")
