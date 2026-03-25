"""
Interactive Match Predictor
Usage: python predict_match.py "Team A" "Team B"
"""

import sys
from football_analysis_stdlib import FootballAnalyzer, SimpleMLPredictor, FootballDataStructure

def main():
    # Initialize and load data
    print("Loading football data...")
    analyzer = FootballAnalyzer("D:\\prject dsa\\Football_Dataset_2015_2025.csv")
    analyzer.load_data()
    analyzer.build_data_structures()
    analyzer.calculate_statistics()
    
    # Show available teams
    print("\n" + "=" * 60)
    print("AVAILABLE TEAMS:")
    print("=" * 60)
    teams = [t['team'] for t in analyzer.team_analysis]
    for i, team in enumerate(teams, 1):
        print(f"{i:2}. {team}")
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("MATCH PREDICTOR")
    print("=" * 60)
    
    while True:
        print("\nEnter match details (or 'quit' to exit):")
        
        home = input("Home Team: ").strip()
        if home.lower() == 'quit':
            break
            
        away = input("Away Team: ").strip()
        if away.lower() == 'quit':
            break
        
        comp = input("Competition (default: Premier League): ").strip() or "Premier League"
        
        # Validate teams
        if home not in teams:
            print(f"❌ Team '{home}' not found. Please choose from the list above.")
            continue
        if away not in teams:
            print(f"❌ Team '{away}' not found. Please choose from the list above.")
            continue
        
        # Make prediction
        result = analyzer.predict_custom_match(home, away, comp)
        
        print("\n" + "-" * 60)

if __name__ == "__main__":
    main()
