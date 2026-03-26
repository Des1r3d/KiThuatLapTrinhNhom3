"""
Công cụ lưu trữ cho thao tác file JSON nguyên tử.

Module này xử lý đọc và ghi file JSON với:
- Ghi nguyên tử (file tạm -> đổi tên) để tránh hỏng dữ liệu
- Cơ chế sao lưu/phục hồi để bảo vệ dữ liệu
- Xử lý lỗi cho file bị hỏng
"""
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any


class StorageEngine:
    """
    Xử lý thao tác đọc/ghi JSON nguyên tử với cơ chế sao lưu.

    Luồng write_json():
        1. Tạo bản sao lưu file hiện tại (nếu có)
        2. Ghi dữ liệu vào file tạm (.tmp)
        3. Đổi tên file tạm thành tên file đích (thao tác nguyên tử)
        4. Giữ bản sao lưu để phục hồi

    Luồng read_json():
        1. Kiểm tra file tồn tại
        2. Thử tải JSON từ file
        3. Nếu bị hỏng, cố gắng phục hồi từ bản sao lưu
        4. Trả về dữ liệu đã phân tích hoặc ném lỗi phù hợp
    """

    def write_json(self, filepath: str, data: Dict[str, Any]) -> None:
        """
        Ghi dữ liệu vào file JSON bằng thao tác ghi nguyên tử.

        Tham số:
            filepath: Đường dẫn tới file JSON
            data: Dictionary để tuần tự hóa

        Ngoại lệ:
            IOError: Nếu thao tác ghi thất bại
            OSError: Nếu thao tác file thất bại
        """
        filepath_obj = Path(filepath)
        backup_path = Path(f"{filepath}.backup")
        temp_path = Path(f"{filepath}.tmp")

        # Tạo thư mục cha nếu chưa tồn tại
        filepath_obj.parent.mkdir(parents=True, exist_ok=True)

        # Bước 1: Tạo bản sao lưu file hiện tại
        if filepath_obj.exists():
            shutil.copy2(filepath_obj, backup_path)

        try:
            # Bước 2: Ghi vào file tạm
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Bước 3: Đổi tên nguyên tử
            # Trên Windows, cần xóa file đích trước nếu tồn tại
            if os.name == 'nt' and filepath_obj.exists():
                filepath_obj.unlink()

            temp_path.rename(filepath_obj)

        except Exception as e:
            # Phục hồi từ bản sao lưu nếu ghi thất bại
            if backup_path.exists() and not filepath_obj.exists():
                shutil.copy2(backup_path, filepath_obj)

            # Dọn dẹp file tạm nếu tồn tại
            if temp_path.exists():
                temp_path.unlink()

            raise IOError(f"Ghi file JSON thất bại {filepath}: {str(e)}") from e

    def read_json(self, filepath: str) -> Dict[str, Any]:
        """
        Đọc dữ liệu từ file JSON với phục hồi tự động từ bản sao lưu.

        Nếu file chính bị hỏng, cố gắng phục hồi từ bản sao lưu.

        Tham số:
            filepath: Đường dẫn tới file JSON

        Trả về:
            Dictionary với dữ liệu đã tải

        Ngoại lệ:
            FileNotFoundError: Nếu file không tồn tại và không có bản sao lưu
            json.JSONDecodeError: Nếu JSON bị lỗi và không có bản sao lưu
        """
        filepath_obj = Path(filepath)
        backup_path = Path(f"{filepath}.backup")

        # Kiểm tra file tồn tại
        if not filepath_obj.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {filepath}")

        try:
            # Thử đọc file chính
            with open(filepath_obj, 'r', encoding='utf-8') as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            # File chính bị hỏng, thử bản sao lưu
            if backup_path.exists():
                try:
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Phục hồi từ bản sao lưu
                    shutil.copy2(backup_path, filepath_obj)
                    return data

                except json.JSONDecodeError:
                    # Bản sao lưu cũng bị hỏng
                    raise json.JSONDecodeError(
                        f"Cả file chính và bản sao lưu đều bị hỏng: {filepath}",
                        e.doc,
                        e.pos
                    ) from e
            else:
                # Không có bản sao lưu
                raise
