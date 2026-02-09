"""
Search Engine for Pharmacy Management System.

This module provides fuzzy search functionality using TheFuzz library:
- Indexes medicine names for fast lookup
- Performs fuzzy matching with configurable threshold
- Returns top results with match scores
"""
from typing import List, Tuple, Dict, Optional

from thefuzz import fuzz

from src.models import Medicine


class SearchEngine:
    """
    Fuzzy search engine for medicine inventory.
    
    Uses TheFuzz library for fuzzy string matching.
    Maintains an index of medicine names for fast repeated searches.
    
    Attributes:
        medicines: List of indexed Medicine objects
        name_index: Dictionary mapping medicine ID to normalized name
        match_threshold: Minimum score (0-100) to include in results
    """
    
    def __init__(self, match_threshold: int = 70):
        """
        Initialize SearchEngine.
        
        Args:
            match_threshold: Minimum fuzzy match score (0-100) for results
        """
        self.medicines: List[Medicine] = []
        self.name_index: Dict[str, str] = {}  # id -> normalized name
        self.match_threshold = match_threshold
    
    def index_data(self, medicines: List[Medicine]) -> None:
        """
        Build search index from medicines list.
        
        Stores medicines and creates normalized name index.
        
        Args:
            medicines: List of medicines to index
        """
        self.medicines = medicines
        self.name_index = {
            med.id: self._normalize(med.name)
            for med in medicines
        }
    
    def _normalize(self, text: str) -> str:
        """
        Normalize text for comparison.
        
        Args:
            text: Text to normalize
            
        Returns:
            Lowercase, stripped text
        """
        return text.lower().strip()
    
    def _get_medicine_by_id(self, medicine_id: str) -> Optional[Medicine]:
        """
        Get Medicine object by ID from indexed medicines.
        
        Args:
            medicine_id: ID to look up
            
        Returns:
            Medicine object if found, None otherwise
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
        Search for medicines matching query.
        
        Performs fuzzy matching against all indexed medicine names.
        Returns results sorted by match score (descending).
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of (Medicine, score) tuples, sorted by score descending.
            Only includes results with score >= match_threshold.
        """
        if not query or not query.strip():
            return []
        
        normalized_query = self._normalize(query)
        results: List[Tuple[Medicine, int]] = []
        
        for med_id, name in self.name_index.items():
            # Calculate fuzzy match score
            score = fuzz.ratio(normalized_query, name)
            
            # Also check partial ratio for substring matches
            partial_score = fuzz.partial_ratio(normalized_query, name)
            
            # Use the higher of the two scores
            best_score = max(score, partial_score)
            
            if best_score >= self.match_threshold:
                medicine = self._get_medicine_by_id(med_id)
                if medicine:
                    results.append((medicine, best_score))
        
        # Sort by score (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 'limit' results
        return results[:limit]
    
    def search_by_name(
        self,
        query: str,
        limit: int = 5
    ) -> List[Tuple[Medicine, int]]:
        """
        Alias for search() method.
        
        Maintained for API compatibility.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of (Medicine, score) tuples
        """
        return self.search(query, limit)
    
    def get_suggestions(
        self,
        partial_query: str,
        limit: int = 5
    ) -> List[str]:
        """
        Get autocomplete suggestions for partial query.
        
        Uses partial_ratio for better prefix matching.
        
        Args:
            partial_query: Partial search query
            limit: Maximum number of suggestions
            
        Returns:
            List of medicine names that match
        """
        if not partial_query or not partial_query.strip():
            return []
        
        normalized_query = self._normalize(partial_query)
        suggestions: List[Tuple[str, int]] = []
        
        for med_id, name in self.name_index.items():
            # Use partial ratio for prefix-like matching
            score = fuzz.partial_ratio(normalized_query, name)
            
            if score >= self.match_threshold:
                medicine = self._get_medicine_by_id(med_id)
                if medicine:
                    suggestions.append((medicine.name, score))
        
        # Sort by score descending
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        # Return just the names
        return [name for name, _ in suggestions[:limit]]
    
    def clear_index(self) -> None:
        """Clear the search index."""
        self.medicines = []
        self.name_index = {}
    
    def update_index(self, medicines: List[Medicine]) -> None:
        """
        Update the search index with new data.
        
        Alias for index_data() to match expected API.
        
        Args:
            medicines: New list of medicines to index
        """
        self.index_data(medicines)
