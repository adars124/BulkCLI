"""
Capital lookup utility for helping users find their capital information
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from difflib import SequenceMatcher


class CapitalLookup:
    """Utility class for looking up capital information"""

    def __init__(self, capitals_file: str = "capitals.json"):
        """
        Initialize the capital lookup with capitals data
        
        Args:
            capitals_file: Path to the capitals JSON file
        """
        self.capitals_file = Path(capitals_file)
        self.capitals = self._load_capitals()

    def _load_capitals(self) -> List[Dict]:
        """Load capitals data from JSON file"""
        if not self.capitals_file.exists():
            raise FileNotFoundError(f"Capitals file not found: {self.capitals_file}")
        
        with open(self.capitals_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search_by_name(self, search_term: str, exact_match: bool = False) -> List[Dict]:
        """
        Search capitals by name
        
        Args:
            search_term: The search term to look for
            exact_match: If True, search for exact matches only
            
        Returns:
            List of matching capital dictionaries
        """
        search_term = search_term.lower().strip()
        results = []
        
        for capital in self.capitals:
            capital_name = capital['name'].lower()
            
            if exact_match:
                if search_term == capital_name:
                    results.append(capital)
            else:
                if search_term in capital_name:
                    results.append(capital)
        
        return results

    def search_by_code(self, code: str) -> Optional[Dict]:
        """
        Search capital by code
        
        Args:
            code: The capital code to search for
            
        Returns:
            Capital dictionary if found, None otherwise
        """
        code = code.strip()
        for capital in self.capitals:
            if capital['code'] == code:
                return capital
        return None

    def search_by_id(self, capital_id: int) -> Optional[Dict]:
        """
        Search capital by ID
        
        Args:
            capital_id: The capital ID to search for
            
        Returns:
            Capital dictionary if found, None otherwise
        """
        for capital in self.capitals:
            if capital['id'] == capital_id:
                return capital
        return None

    def fuzzy_search(self, search_term: str, threshold: float = 0.6) -> List[Dict]:
        """
        Perform fuzzy search on capital names
        
        Args:
            search_term: The search term to look for
            threshold: Minimum similarity ratio (0.0 to 1.0)
            
        Returns:
            List of matching capital dictionaries with similarity scores
        """
        search_term = search_term.lower().strip()
        results = []
        
        for capital in self.capitals:
            capital_name = capital['name'].lower()
            similarity = SequenceMatcher(None, search_term, capital_name).ratio()
            
            if similarity >= threshold:
                capital_with_score = capital.copy()
                capital_with_score['similarity'] = similarity
                results.append(capital_with_score)
        
        # Sort by similarity score (highest first)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results

    def get_all_capitals(self) -> List[Dict]:
        """Get all capitals"""
        return self.capitals.copy()

    def search_interactive(self, search_term: str) -> List[Dict]:
        """
        Interactive search that combines multiple search methods
        
        Args:
            search_term: The search term to look for
            
        Returns:
            List of matching capital dictionaries
        """
        # First, try exact code search
        if search_term.isdigit() and len(search_term) == 5:
            code_result = self.search_by_code(search_term)
            if code_result:
                return [code_result]
        
        # Try exact name search
        name_results = self.search_by_name(search_term, exact_match=True)
        if name_results:
            return name_results
        
        # Try partial name search
        partial_results = self.search_by_name(search_term, exact_match=False)
        if partial_results:
            return partial_results
        
        # Try fuzzy search as last resort
        fuzzy_results = self.fuzzy_search(search_term, threshold=0.4)
        return fuzzy_results

    def format_capital_info(self, capital: Dict) -> str:
        """
        Format capital information for display
        
        Args:
            capital: Capital dictionary
            
        Returns:
            Formatted string representation
        """
        similarity_info = ""
        if 'similarity' in capital:
            similarity_info = f" (Match: {capital['similarity']:.1%})"
        
        return (
            f"🏢 {capital['name']}\n"
            f"   🆔 ID: {capital['id']} (Use this as client_id in accounts.txt)\n"
            f"   📋 Code: {capital['code']}{similarity_info}"
        )

    def print_search_results(self, results: List[Dict], max_results: int = 10):
        """
        Print search results in a formatted way
        
        Args:
            results: List of capital dictionaries
            max_results: Maximum number of results to display
        """
        if not results:
            print("❌ No capitals found matching your search.")
            return
        
        print(f"🔍 Found {len(results)} matching capital(s):")
        print("=" * 60)
        
        for i, capital in enumerate(results[:max_results], 1):
            print(f"{i}. {self.format_capital_info(capital)}")
            print()
        
        if len(results) > max_results:
            print(f"... and {len(results) - max_results} more results.")
            print("🔍 Try a more specific search term to narrow down results.") 