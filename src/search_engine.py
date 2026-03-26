"""
Công cụ Tìm kiếm cho Hệ Thống Quản Lý Kho Thuốc.

Module này cung cấp chức năng tìm kiếm mờ sử dụng thư viện TheFuzz:
- Đánh chỉ mục tên thuốc để tra cứu nhanh
- Thực hiện khớp mờ với ngưỡng có thể cấu hình
- Trả về kết quả hàng đầu với điểm khớp
"""
from typing import List, Tuple, Dict, Optional

from thefuzz import fuzz

from src.models import Medicine


class SearchEngine:
    """
    Công cụ tìm kiếm mờ cho kho thuốc.
    
    Sử dụng thư viện TheFuzz để khớp chuỗi mờ.
    Duy trì chỉ mục tên thuốc để tìm kiếm lặp lại nhanh.
    
    Thuộc tính:
        medicines: Danh sách đối tượng Medicine đã đánh chỉ mục
        name_index: Dictionary ánh xạ ID thuốc tới tên đã chuẩn hóa
        match_threshold: Điểm tối thiểu (0-100) để đưa vào kết quả
    """
    
    def __init__(self, match_threshold: int = 70):
        """
        Khởi tạo SearchEngine.
        
        Tham số:
            match_threshold: Điểm khớp mờ tối thiểu (0-100) cho kết quả
        """
        self.medicines: List[Medicine] = []
        self.name_index: Dict[str, str] = {}  # id -> tên đã chuẩn hóa
        self.match_threshold = match_threshold
    
    def index_data(self, medicines: List[Medicine]) -> None:
        """
        Xây dựng chỉ mục tìm kiếm từ danh sách thuốc.
        
        Lưu trữ thuốc và tạo chỉ mục tên đã chuẩn hóa.
        
        Tham số:
            medicines: Danh sách thuốc cần đánh chỉ mục
        """
        self.medicines = medicines
        self.name_index = {
            med.id: self._normalize(med.name)
            for med in medicines
        }
    
    def _normalize(self, text: str) -> str:
        """
        Chuẩn hóa văn bản để so sánh.
        
        Tham số:
            text: Văn bản cần chuẩn hóa
            
        Trả về:
            Văn bản viết thường, đã cắt khoảng trắng
        """
        return text.lower().strip()
    
    def _get_medicine_by_id(self, medicine_id: str) -> Optional[Medicine]:
        """
        Lấy đối tượng Medicine theo ID từ danh sách đã đánh chỉ mục.
        
        Tham số:
            medicine_id: ID cần tra cứu
            
        Trả về:
            Đối tượng Medicine nếu tìm thấy, None nếu không
        """
        for med in self.medicines:
            if med.id == medicine_id:
                return med
        return None
    
    def search(
        self,
        query: str,
        limit: int = 5
    ) -> List[Tuple[Medicine, int]]:
        """
        Tìm kiếm thuốc khớp với truy vấn.
        
        Thực hiện khớp mờ với tất cả tên thuốc đã đánh chỉ mục.
        Trả về kết quả sắp xếp theo điểm khớp (giảm dần).
        
        Tham số:
            query: Chuỗi truy vấn tìm kiếm
            limit: Số lượng kết quả tối đa trả về
            
        Trả về:
            Danh sách tuple (Medicine, điểm), sắp xếp theo điểm giảm dần.
            Chỉ bao gồm kết quả có điểm >= match_threshold.
        """
        if not query or not query.strip():
            return []
        
        normalized_query = self._normalize(query)
        results: List[Tuple[Medicine, int]] = []
        
        for med_id, name in self.name_index.items():
            # Tính điểm khớp mờ
            score = fuzz.ratio(normalized_query, name)
            
            # Kiểm tra thêm partial ratio cho khớp chuỗi con
            partial_score = fuzz.partial_ratio(normalized_query, name)
            
            # Sử dụng điểm cao hơn trong hai
            best_score = max(score, partial_score)
            
            if best_score >= self.match_threshold:
                medicine = self._get_medicine_by_id(med_id)
                if medicine:
                    results.append((medicine, best_score))
        
        # Sắp xếp theo điểm (giảm dần)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Trả về 'limit' kết quả đầu
        return results[:limit]
    
    def search_by_name(
        self,
        query: str,
        limit: int = 5
    ) -> List[Tuple[Medicine, int]]:
        """
        Bí danh cho phương thức search().
        
        Duy trì để tương thích API.
        
        Tham số:
            query: Chuỗi truy vấn tìm kiếm
            limit: Số lượng kết quả tối đa trả về
            
        Trả về:
            Danh sách tuple (Medicine, điểm)
        """
        return self.search(query, limit)
    
    def get_suggestions(
        self,
        partial_query: str,
        limit: int = 5
    ) -> List[str]:
        """
        Lấy gợi ý tự hoàn thành cho truy vấn một phần.
        
        Sử dụng partial_ratio để khớp tiền tố tốt hơn.
        
        Tham số:
            partial_query: Truy vấn tìm kiếm một phần
            limit: Số lượng gợi ý tối đa
            
        Trả về:
            Danh sách tên thuốc khớp
        """
        if not partial_query or not partial_query.strip():
            return []
        
        normalized_query = self._normalize(partial_query)
        suggestions: List[Tuple[str, int]] = []
        
        for med_id, name in self.name_index.items():
            # Sử dụng partial ratio cho khớp dạng tiền tố
            score = fuzz.partial_ratio(normalized_query, name)
            
            if score >= self.match_threshold:
                medicine = self._get_medicine_by_id(med_id)
                if medicine:
                    suggestions.append((medicine.name, score))
        
        # Sắp xếp theo điểm giảm dần
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        # Chỉ trả về tên
        return [name for name, _ in suggestions[:limit]]
    
    def clear_index(self) -> None:
        """Xóa chỉ mục tìm kiếm."""
        self.medicines = []
        self.name_index = {}
    
    def update_index(self, medicines: List[Medicine]) -> None:
        """
        Cập nhật chỉ mục tìm kiếm với dữ liệu mới.
        
        Bí danh cho index_data() để khớp API mong đợi.
        
        Tham số:
            medicines: Danh sách thuốc mới cần đánh chỉ mục
        """
        self.index_data(medicines)
