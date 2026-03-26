"""
Trình quản lý Ảnh cho Hệ Thống Quản Lý Kho Thuốc.

Xử lý thao tác ảnh thuốc:
- Sao chép ảnh vào lưu trữ cục bộ (data/images/)
- Tạo tên file duy nhất dựa trên ID thuốc
- Kiểm tra file ảnh (định dạng, kích thước)
- Xóa ảnh khi thuốc bị loại bỏ
"""
import os
import shutil
from pathlib import Path
from typing import Optional, List

# Các định dạng ảnh được hỗ trợ
SUPPORTED_FORMATS: List[str] = [".png", ".jpg", ".jpeg", ".bmp", ".webp"]

# Kích thước file ảnh tối đa (5MB)
MAX_IMAGE_SIZE: int = 5 * 1024 * 1024

# Thư mục ảnh mặc định
DEFAULT_IMAGES_DIR: str = "data/images"


class ImageManager:
    """
    Quản lý ảnh thuốc trong hệ thống file cục bộ.

    Ảnh được lưu trong thư mục riêng (data/images/) với
    tên file dựa trên ID thuốc để tra cứu dễ dàng.

    Thuộc tính:
        images_dir: Đường dẫn tới thư mục ảnh
    """

    def __init__(self, images_dir: str = DEFAULT_IMAGES_DIR):
        """
        Khởi tạo ImageManager.

        Tham số:
            images_dir: Đường dẫn tới thư mục lưu ảnh
        """
        self.images_dir = images_dir
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Tạo thư mục ảnh nếu chưa tồn tại."""
        Path(self.images_dir).mkdir(parents=True, exist_ok=True)

    def validate_image(self, source_path: str) -> None:
        """
        Kiểm tra file ảnh trước khi nhập.

        Tham số:
            source_path: Đường dẫn tới file ảnh cần kiểm tra

        Ngoại lệ:
            FileNotFoundError: Nếu file không tồn tại
            ValueError: Nếu định dạng file không được hỗ trợ
            ValueError: Nếu kích thước file vượt giới hạn
        """
        path = Path(source_path)

        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy file ảnh: {source_path}")

        # Kiểm tra định dạng
        suffix = path.suffix.lower()
        if suffix not in SUPPORTED_FORMATS:
            formats_str = ", ".join(SUPPORTED_FORMATS)
            raise ValueError(
                f"Định dạng ảnh không được hỗ trợ: '{suffix}'. "
                f"Các định dạng được hỗ trợ: {formats_str}"
            )

        # Kiểm tra kích thước file
        file_size = path.stat().st_size
        if file_size > MAX_IMAGE_SIZE:
            max_mb = MAX_IMAGE_SIZE / (1024 * 1024)
            actual_mb = file_size / (1024 * 1024)
            raise ValueError(
                f"File ảnh quá lớn: {actual_mb:.1f}MB. "
                f"Tối đa cho phép: {max_mb:.0f}MB"
            )

    def save_image(self, source_path: str, medicine_id: str) -> str:
        """
        Sao chép ảnh vào thư mục ảnh với tên dựa trên ID thuốc.

        Tham số:
            source_path: Đường dẫn tới file ảnh nguồn
            medicine_id: ID thuốc dùng làm tên file cơ sở

        Trả về:
            Đường dẫn tương đối tới ảnh đã lưu (tương đối với thư mục cha images_dir)

        Ngoại lệ:
            FileNotFoundError: Nếu file nguồn không tồn tại
            ValueError: Nếu ảnh không hợp lệ (định dạng/kích thước)
            IOError: Nếu thao tác sao chép thất bại
        """
        self.validate_image(source_path)

        source = Path(source_path)
        ext = source.suffix.lower()

        # Tạo tên file: medicine_id + phần mở rộng
        # Làm sạch medicine_id cho an toàn hệ thống file
        safe_id = medicine_id.replace("/", "_").replace("\\", "_")
        filename = f"{safe_id}{ext}"
        dest_path = Path(self.images_dir) / filename

        # Xóa ảnh hiện tại cho thuốc này (có thể khác phần mở rộng)
        self.delete_image(medicine_id)

        try:
            shutil.copy2(str(source), str(dest_path))
        except Exception as e:
            raise IOError(f"Lưu ảnh thất bại: {str(e)}") from e

        # Trả về đường dẫn tương đối từ thư mục cha data/
        return str(Path(self.images_dir).name / Path(filename))

    def delete_image(self, medicine_id: str) -> bool:
        """
        Xóa ảnh liên quan tới ID thuốc.

        Xóa bất kỳ file nào trong images_dir khớp với ID thuốc
        (bất kể phần mở rộng).

        Tham số:
            medicine_id: ID thuốc cần xóa ảnh

        Trả về:
            True nếu đã xóa ảnh, False nếu không tìm thấy
        """
        safe_id = medicine_id.replace("/", "_").replace("\\", "_")
        deleted = False

        for ext in SUPPORTED_FORMATS:
            image_path = Path(self.images_dir) / f"{safe_id}{ext}"
            if image_path.exists():
                try:
                    image_path.unlink()
                    deleted = True
                except OSError:
                    pass

        return deleted

    def get_image_path(self, medicine_id: str) -> Optional[str]:
        """
        Lấy đường dẫn tuyệt đối tới ảnh thuốc nếu tồn tại.

        Tham số:
            medicine_id: ID thuốc cần tra cứu

        Trả về:
            Đường dẫn tuyệt đối tới file ảnh, hoặc None nếu không có ảnh
        """
        safe_id = medicine_id.replace("/", "_").replace("\\", "_")

        for ext in SUPPORTED_FORMATS:
            image_path = Path(self.images_dir) / f"{safe_id}{ext}"
            if image_path.exists():
                return str(image_path.resolve())

        return None

    def get_image_path_from_relative(self, relative_path: str) -> Optional[str]:
        """
        Chuyển đường dẫn ảnh tương đối thành đường dẫn tuyệt đối.

        Tham số:
            relative_path: Đường dẫn tương đối lưu trong Medicine.image_path

        Trả về:
            Đường dẫn tuyệt đối nếu file tồn tại, None nếu không
        """
        if not relative_path:
            return None

        # Thử tương đối với thư mục cha images_dir
        abs_path = Path(self.images_dir).parent / relative_path
        if abs_path.exists():
            return str(abs_path.resolve())

        return None

    def image_exists(self, medicine_id: str) -> bool:
        """
        Kiểm tra thuốc có ảnh liên quan không.

        Tham số:
            medicine_id: ID thuốc cần kiểm tra

        Trả về:
            True nếu ảnh tồn tại, False nếu không
        """
        return self.get_image_path(medicine_id) is not None

    def rename_image(self, old_medicine_id: str, new_medicine_id: str) -> Optional[str]:
        """
        Đổi tên file ảnh thuốc khi ID thay đổi (VD: chuyển kệ).

        Tìm ảnh liên quan tới old_medicine_id, đổi tên để
        khớp new_medicine_id, và trả về đường dẫn tương đối mới.

        Tham số:
            old_medicine_id: ID thuốc cũ
            new_medicine_id: ID thuốc mới

        Trả về:
            Đường dẫn ảnh tương đối mới, hoặc None nếu không tìm thấy ảnh
        """
        old_safe = old_medicine_id.replace("/", "_").replace("\\", "_")
        new_safe = new_medicine_id.replace("/", "_").replace("\\", "_")

        for ext in SUPPORTED_FORMATS:
            old_path = Path(self.images_dir) / f"{old_safe}{ext}"
            if old_path.exists():
                new_path = Path(self.images_dir) / f"{new_safe}{ext}"
                try:
                    old_path.rename(new_path)
                    return str(Path(self.images_dir).name / Path(f"{new_safe}{ext}"))
                except OSError:
                    pass

        return None
