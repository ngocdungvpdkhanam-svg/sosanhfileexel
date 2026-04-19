import pandas as pd

def so_sanh_excel(file_goc, file_doi_chieu, cot_goc, cot_doi_chieu, file_ket_qua):
    print("--- Bắt đầu đọc dữ liệu (có thể mất ít phút nếu file cực lớn) ---")
    
    # Đọc dữ liệu từ 2 file
    # Sử dụng usecols để chỉ load các cột cần thiết, tiết kiệm RAM
    df_goc = pd.read_excel(file_goc)
    df_target = pd.read_excel(file_doi_chieu, usecols=[cot_doi_chieu])

    print(f"Đã tải xong. Đang xử lý so sánh trên {len(df_goc)} dòng...")

    # Chuyển cột đối chiếu thành một 'set' để tăng tốc độ tìm kiếm (O(1) thay vì O(n))
    # Điều này giúp xử lý hàng triệu dòng chỉ trong vài giây
    danh_sach_doi_chieu = set(df_target[cot_doi_chieu].dropna().astype(str))

    # Kiểm tra: Nếu giá trị ở cột gốc nằm trong danh sách đối chiếu thì ghi 1, ngược lại ghi 0
    df_goc['Ket_Qua_So_Sanh'] = df_goc[cot_goc].astype(str).apply(
        lambda x: 1 if x in danh_sach_doi_chieu else 0
    )

    # Lưu kết quả
    print(f"Đang xuất kết quả ra file {file_ket_qua}...")
    df_goc.to_excel(file_ket_qua, index=False)
    print("--- Hoàn thành! ---")

# --- CẤU HÌNH THÔNG TIN Ở ĐÂY ---
config = {
    "file_goc": "file_chinh.xlsx",        # Tên file chứa cột cần kiểm tra
    "cot_goc": "Mã Sản Phẩm",            # Tên cột trong file gốc
    "file_doi_chieu": "file_phu.xlsx",    # Tên file dùng để đối chiếu dữ liệu
    "cot_doi_chieu": "Mã SKU",            # Tên cột trong file đối chiếu
    "file_ket_qua": "ket_qua_so_sanh.xlsx" # Tên file sẽ xuất ra
}

if __name__ == "__main__":
    so_sanh_excel(
        config["file_goc"], 
        config["file_doi_chieu"], 
        config["cot_goc"], 
        config["cot_doi_chieu"], 
        config["file_ket_qua"]
    )
