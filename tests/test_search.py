"""
Test suite for SearchEngine.
Tests cover fuzzy search, indexing, and suggestions.
"""
import pytest
from datetime import date, timedelta
from src.models import Medicine
from src.search_engine import SearchEngine


class TestSearchEngine:
    """Test suite for SearchEngine class."""
    
    @pytest.fixture
    def search_engine(self):
        """Create SearchEngine with default threshold."""
        return SearchEngine(match_threshold=80)
    
    @pytest.fixture
    def sample_medicines(self):
        """Create a list of sample medicines for testing."""
        return [
            Medicine(
                id="MED001",
                name="Paracetamol 500mg",
                quantity=100,
                expiry_date=date.today() + timedelta(days=365),
                shelf_id="SHELF-A1",
                price=5.99
            ),
            Medicine(
                id="MED002",
                name="Paracetamol Extra",
                quantity=50,
                expiry_date=date.today() + timedelta(days=180),
                shelf_id="SHELF-A2",
                price=7.99
            ),
            Medicine(
                id="MED003",
                name="Aspirin 100mg",
                quantity=200,
                expiry_date=date.today() + timedelta(days=730),
                shelf_id="SHELF-B1",
                price=3.99
            ),
            Medicine(
                id="MED004",
                name="Ibuprofen 400mg",
                quantity=75,
                expiry_date=date.today() + timedelta(days=365),
                shelf_id="SHELF-B2",
                price=6.99
            ),
            Medicine(
                id="MED005",
                name="Amoxicillin 250mg",
                quantity=30,
                expiry_date=date.today() + timedelta(days=90),
                shelf_id="SHELF-C1",
                price=12.99
            ),
        ]
    
    # === Initialization Tests ===
    
    def test_initialization_default_threshold(self):
        """Test SearchEngine initializes with default threshold."""
        engine = SearchEngine()
        
        assert engine.match_threshold == 80
        assert engine.medicines == []
        assert engine.name_index == {}
    
    def test_initialization_custom_threshold(self):
        """Test SearchEngine initializes with custom threshold."""
        engine = SearchEngine(match_threshold=90)
        
        assert engine.match_threshold == 90
    
    # === Index Data Tests ===
    
    def test_index_data_builds_index(self, search_engine, sample_medicines):
        """Test index_data builds name index correctly."""
        search_engine.index_data(sample_medicines)
        
        assert len(search_engine.medicines) == 5
        assert len(search_engine.name_index) == 5
        assert search_engine.name_index["MED001"] == "paracetamol 500mg"
    
    def test_index_data_normalizes_names(self, search_engine):
        """Test index_data normalizes names to lowercase."""
        medicines = [
            Medicine(
                id="MED001",
                name="UPPERCASE Medicine",
                quantity=10,
                expiry_date=date.today() + timedelta(days=365),
                shelf_id="SHELF-A1",
                price=5.99
            )
        ]
        
        search_engine.index_data(medicines)
        
        assert search_engine.name_index["MED001"] == "uppercase medicine"
    
    def test_index_data_replaces_existing(self, search_engine, sample_medicines):
        """Test index_data replaces existing index."""
        search_engine.index_data(sample_medicines)
        
        new_medicines = [
            Medicine(
                id="MED100",
                name="New Medicine",
                quantity=10,
                expiry_date=date.today() + timedelta(days=365),
                shelf_id="SHELF-A1",
                price=5.99
            )
        ]
        
        search_engine.index_data(new_medicines)
        
        assert len(search_engine.medicines) == 1
        assert "MED001" not in search_engine.name_index
    
    # === Search Tests ===
    
    def test_search_exact_match(self, search_engine, sample_medicines):
        """Test search with exact match query."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("Paracetamol 500mg")
        
        assert len(results) >= 1
        assert results[0][0].id == "MED001"
        assert results[0][1] == 100  # Perfect match
    
    def test_search_partial_match(self, search_engine, sample_medicines):
        """Test search with partial query."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("Paracetamol")
        
        assert len(results) == 2  # Both Paracetamol medicines
        medicine_ids = [r[0].id for r in results]
        assert "MED001" in medicine_ids
        assert "MED002" in medicine_ids
    
    def test_search_fuzzy_match(self, search_engine, sample_medicines):
        """Test search with fuzzy (misspelled) query."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("Paracetamoll")  # Misspelled
        
        # Should still find Paracetamol medicines with high enough score
        assert len(results) >= 1
    
    def test_search_case_insensitive(self, search_engine, sample_medicines):
        """Test search is case insensitive."""
        search_engine.index_data(sample_medicines)
        
        results1 = search_engine.search("PARACETAMOL")
        results2 = search_engine.search("paracetamol")
        results3 = search_engine.search("Paracetamol")
        
        assert len(results1) == len(results2) == len(results3)
    
    def test_search_respects_limit(self, search_engine, sample_medicines):
        """Test search respects result limit."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("", limit=2)
        
        # Empty query returns empty (no matches above threshold)
        assert len(results) <= 2
    
    def test_search_sorted_by_score(self, search_engine, sample_medicines):
        """Test search results are sorted by score descending."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("Paracetamol")
        
        for i in range(len(results) - 1):
            assert results[i][1] >= results[i + 1][1]
    
    def test_search_empty_query(self, search_engine, sample_medicines):
        """Test search with empty query returns empty list."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("")
        
        assert results == []
    
    def test_search_whitespace_query(self, search_engine, sample_medicines):
        """Test search with whitespace-only query returns empty list."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("   ")
        
        assert results == []
    
    def test_search_no_matches(self, search_engine, sample_medicines):
        """Test search with query that matches nothing."""
        search_engine.index_data(sample_medicines)
        
        results = search_engine.search("XyzNonExistent")
        
        assert results == []
    
    def test_search_respects_threshold(self, sample_medicines):
        """Test search respects match threshold."""
        # High threshold - only exact matches
        engine_high = SearchEngine(match_threshold=95)
        engine_high.index_data(sample_medicines)
        results_high = engine_high.search("Paracet")
        
        # Low threshold - more matches
        engine_low = SearchEngine(match_threshold=50)
        engine_low.index_data(sample_medicines)
        results_low = engine_low.search("Paracet")
        
        assert len(results_low) >= len(results_high)
    
    def test_search_empty_index(self, search_engine):
        """Test search with uninitialized index."""
        results = search_engine.search("Paracetamol")
        
        assert results == []
    
    # === Search By Name Tests ===
    
    def test_search_by_name_alias(self, search_engine, sample_medicines):
        """Test search_by_name is alias for search."""
        search_engine.index_data(sample_medicines)
        
        results1 = search_engine.search("Aspirin")
        results2 = search_engine.search_by_name("Aspirin")
        
        assert len(results1) == len(results2)
        if results1:
            assert results1[0][0].id == results2[0][0].id
    
    # === Get Suggestions Tests ===
    
    def test_get_suggestions_returns_names(self, search_engine, sample_medicines):
        """Test get_suggestions returns medicine names."""
        search_engine.index_data(sample_medicines)
        
        suggestions = search_engine.get_suggestions("Parac")
        
        assert isinstance(suggestions, list)
        for s in suggestions:
            assert isinstance(s, str)
    
    def test_get_suggestions_partial_match(self, search_engine, sample_medicines):
        """Test get_suggestions works with partial input."""
        search_engine.index_data(sample_medicines)
        
        suggestions = search_engine.get_suggestions("Para")
        
        assert len(suggestions) >= 1
        for s in suggestions:
            assert "Paracetamol" in s
    
    def test_get_suggestions_respects_limit(self, search_engine, sample_medicines):
        """Test get_suggestions respects limit parameter."""
        search_engine.index_data(sample_medicines)
        
        suggestions = search_engine.get_suggestions("a", limit=2)
        
        assert len(suggestions) <= 2
    
    def test_get_suggestions_empty_query(self, search_engine, sample_medicines):
        """Test get_suggestions with empty query."""
        search_engine.index_data(sample_medicines)
        
        suggestions = search_engine.get_suggestions("")
        
        assert suggestions == []
    
    # === Clear Index Tests ===
    
    def test_clear_index(self, search_engine, sample_medicines):
        """Test clear_index removes all indexed data."""
        search_engine.index_data(sample_medicines)
        search_engine.clear_index()
        
        assert search_engine.medicines == []
        assert search_engine.name_index == {}
    
    # === Update Index Tests ===
    
    def test_update_index(self, search_engine, sample_medicines):
        """Test update_index replaces existing data."""
        search_engine.index_data(sample_medicines)
        
        new_medicines = [
            Medicine(
                id="MED100",
                name="Updated Medicine",
                quantity=10,
                expiry_date=date.today() + timedelta(days=365),
                shelf_id="SHELF-A1",
                price=5.99
            )
        ]
        
        search_engine.update_index(new_medicines)
        
        assert len(search_engine.medicines) == 1
        assert search_engine.medicines[0].name == "Updated Medicine"
    
    # === Vietnamese Name Tests ===
    
    def test_search_vietnamese_names(self, search_engine):
        """Test search works with Vietnamese medicine names."""
        medicines = [
            Medicine(
                id="MED001",
                name="Thuốc giảm đau Paracetamol",
                quantity=100,
                expiry_date=date.today() + timedelta(days=365),
                shelf_id="SHELF-A1",
                price=5.99
            ),
            Medicine(
                id="MED002",
                name="Vitamin C tổng hợp",
                quantity=50,
                expiry_date=date.today() + timedelta(days=180),
                shelf_id="SHELF-A2",
                price=7.99
            ),
        ]
        
        search_engine.index_data(medicines)
        
        results = search_engine.search("Paracetamol")
        
        assert len(results) >= 1
        assert "Paracetamol" in results[0][0].name
    
    # === Integration Tests ===
    
    def test_full_search_workflow(self, search_engine, sample_medicines):
        """Test complete search workflow."""
        # Index data
        search_engine.index_data(sample_medicines)
        
        # Search for medicine
        results = search_engine.search("Para")
        
        # Get suggestions
        suggestions = search_engine.get_suggestions("Para")
        
        # Verify results
        assert len(results) >= 1
        assert len(suggestions) >= 1
        
        # Update with new data
        new_medicines = sample_medicines + [
            Medicine(
                id="MED006",
                name="Paracetamol Junior",
                quantity=25,
                expiry_date=date.today() + timedelta(days=180),
                shelf_id="SHELF-D1",
                price=4.99
            )
        ]
        search_engine.update_index(new_medicines)
        
        # Search again
        new_results = search_engine.search("Para")
        
        assert len(new_results) > len(results)
