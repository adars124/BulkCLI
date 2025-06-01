#!/usr/bin/env python3
"""
Capital Finder - Help users find their capital ID for accounts.txt

This script helps users search for their capital/broker information
from the capitals.json file to find the correct client_id for their accounts.txt file.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.utils.capital_lookup import CapitalLookup


def print_header():
    """Print the application header"""
    print("\n🔍 Capital Finder - MeroShare Broker/Capital Lookup")
    print("=" * 60)
    print("This tool helps you find your capital/broker ID for the accounts.txt file.")
    print("The ID you find here should be used as 'client_id' in accounts.txt.\n")


def print_help():
    """Print help information"""
    print("💡 Search Tips:")
    print("  • Enter your broker/capital name (e.g., 'NABIL', 'Kumari')")
    print("  • Enter the 5-digit broker code if you know it")
    print("  • Use partial names for broader searches")
    print("  • Type 'list' to see all available capitals")
    print("  • Type 'help' for this help message")
    print("  • Type 'quit' or 'exit' to exit\n")


def list_all_capitals(lookup: CapitalLookup, page_size: int = 20):
    """List all capitals with pagination"""
    capitals = lookup.get_all_capitals()
    total = len(capitals)
    
    print(f"📋 All Available Capitals ({total} total):")
    print("=" * 60)
    
    page = 0
    while page * page_size < total:
        start_idx = page * page_size
        end_idx = min((page + 1) * page_size, total)
        
        for i, capital in enumerate(capitals[start_idx:end_idx], start_idx + 1):
            print(f"{i:3d}. {lookup.format_capital_info(capital)}")
            print()
        
        if end_idx < total:
            user_input = input(f"Showing {end_idx}/{total} capitals. Press Enter for more, or 'q' to stop: ").strip().lower()
            if user_input == 'q':
                break
            page += 1
        else:
            break


def search_capitals(lookup: CapitalLookup):
    """Interactive capital search"""
    print_help()
    
    while True:
        try:
            search_term = input("🔍 Enter search term (or 'help', 'list', 'quit'): ").strip()
            
            if not search_term:
                continue
            
            search_lower = search_term.lower()
            
            if search_lower in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif search_lower == 'help':
                print_help()
                continue
            elif search_lower == 'list':
                list_all_capitals(lookup)
                continue
            
            # Perform search
            results = lookup.search_interactive(search_term)
            
            if not results:
                print("❌ No capitals found matching your search.")
                print("💡 Try using partial names or check the spelling.")
                print()
                continue
            
            lookup.print_search_results(results)
            
            # If multiple results, ask user to select one
            if len(results) > 1:
                print("💡 Multiple results found. You can:")
                print("  • Refine your search with a more specific term")
                print("  • Use the ID from the result that matches your broker\n")
            else:
                print("✅ Perfect match found!")
                capital = results[0]
                print(f"📝 Your accounts.txt line should start with: {capital['id']},username,password,crn,pin\n")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.\n")


def validate_accounts_file():
    """Validate and provide guidance on accounts.txt format"""
    accounts_file = Path("accounts.txt")
    
    if accounts_file.exists():
        print("✅ Found accounts.txt file.")
        print("📝 Current accounts.txt format should be:")
        print("   client_id,username,password,crn,pin")
        print("   Example: 129,your_username,your_password,your_crn,1234\n")
    else:
        print("⚠️  accounts.txt file not found.")
        print("📝 Create accounts.txt file with format:")
        print("   client_id,username,password,crn,pin")
        print("   Example: 129,your_username,your_password,your_crn,1234\n")


def main():
    """Main application entry point"""
    try:
        print_header()
        
        # Initialize capital lookup
        try:
            lookup = CapitalLookup("capitals.json")
        except FileNotFoundError:
            print("❌ Error: capitals.json file not found!")
            print("Please ensure the capitals.json file is in the same directory as this script.")
            return
        except Exception as e:
            print(f"❌ Error loading capitals data: {e}")
            return
        
        print(f"✅ Loaded {len(lookup.get_all_capitals())} capitals from capitals.json")
        
        # Validate accounts file
        validate_accounts_file()
        
        # Start interactive search
        search_capitals(lookup)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 