"""
Football Match Analysis using Data Structures and Basic ML
Uses only standard library + numpy for core functionality
"""

import csv
import json
from collections import defaultdict, Counter
from datetime import datetime
import math
import random

class FootballDataStructure:
    """Custom data structure for efficient football data management"""
    
    def __init__(self):
        self.team_stats = defaultdict(lambda: {
            'matches_played': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_scored': 0,
            'goals_conceded': 0,
            'home_matches': 0,
            'away_matches': 0,
            'home_wins': 0,
            'away_wins': 0,
            'possession_total': 0,
            'shots_total': 0,
            'corners_total': 0,
            'fouls_total': 0,
            'goals_per_match': [],
            'conceded_per_match': []
        })
        self.head_to_head = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'draws': 0, 'losses': 0}))
        self.competition_stats = defaultdict(lambda: defaultdict(int))
        self.matches = []
        
    def update_team_stats(self, team, is_home, goals_scored, goals_conceded, 
                         possession, shots, corners, fouls, result):
        """Update statistics for a team"""
        stats = self.team_stats[team]
        stats['matches_played'] += 1
        stats['goals_scored'] += goals_scored
        stats['goals_conceded'] += goals_conceded
        stats['goals_per_match'].append(goals_scored)
        stats['conceded_per_match'].append(goals_conceded)
        stats['possession_total'] += possession
        stats['shots_total'] += shots
        stats['corners_total'] += corners
        stats['fouls_total'] += fouls
        
        if is_home:
            stats['home_matches'] += 1
        else:
            stats['away_matches'] += 1
            
        if result == 'win':
            stats['wins'] += 1
            if is_home:
                stats['home_wins'] += 1
            else:
                stats['away_wins'] += 1
        elif result == 'draw':
            stats['draws'] += 1
        else:
            stats['losses'] += 1
    
    def update_head_to_head(self, team1, team2, result):
        """Update head-to-head statistics"""
        if result == 'win':
            self.head_to_head[team1][team2]['wins'] += 1
            self.head_to_head[team2][team1]['losses'] += 1
        elif result == 'loss':
            self.head_to_head[team1][team2]['losses'] += 1
            self.head_to_head[team2][team1]['wins'] += 1
        else:
            self.head_to_head[team1][team2]['draws'] += 1
            self.head_to_head[team2][team1]['draws'] += 1


class SimpleMLPredictor:
    """Simple machine learning predictor using weighted features"""
    
    def __init__(self):
        self.weights = {}
        self.team_strengths = {}
        
    def calculate_team_strength(self, team_stats):
        """Calculate overall team strength score"""
        if team_stats['matches_played'] == 0:
            return 0.5
        
        win_rate = team_stats['wins'] / team_stats['matches_played']
        goal_diff = (team_stats['goals_scored'] - team_stats['goals_conceded']) / max(team_stats['matches_played'], 1)
        avg_goals = team_stats['goals_scored'] / team_stats['matches_played']
        
        # Normalize goal difference (typically -3 to +3)
        normalized_gd = max(0, min(1, (goal_diff + 3) / 6))
        
        # Normalize average goals (typically 0 to 4)
        normalized_goals = max(0, min(1, avg_goals / 4))
        
        # Weighted combination
        strength = (win_rate * 0.4) + (normalized_gd * 0.35) + (normalized_goals * 0.25)
        return strength
    
    def predict_match(self, home_team, away_team, ds, match_features=None):
        """Predict match outcome with confidence scores"""
        
        # Get team stats
        home_stats = ds.team_stats[home_team]
        away_stats = ds.team_stats[away_team]
        
        # Calculate base strengths
        home_strength = self.calculate_team_strength(home_stats)
        away_strength = self.calculate_team_strength(away_stats)
        
        # Home advantage factor (typically 60% home win rate)
        home_advantage = 1.15
        
        # Head-to-head factor
        h2h = ds.head_to_head[home_team][away_team]
        total_h2h = sum(h2h.values())
        
        if total_h2h > 0:
            h2h_factor = (h2h['wins'] + 0.5 * h2h['draws']) / total_h2h
            # Blend with current form
            home_adjusted = (home_strength * home_advantage * 0.7) + (h2h_factor * 0.3)
        else:
            home_adjusted = home_strength * home_advantage
            h2h_factor = 0.5
        
        away_adjusted = away_strength
        
        # Feature adjustments
        if match_features:
            possession_factor = match_features.get('possession_h', 50) / 100
            shots_factor = min(1, match_features.get('shots_h', 15) / 25)
            home_adjusted *= (1 + (possession_factor - 0.5) * 0.2)
            home_adjusted *= (1 + (shots_factor - 0.5) * 0.15)
        
        # Calculate probabilities
        total_strength = home_adjusted + away_adjusted
        
        # Normalize to probabilities
        if total_strength > 0:
            home_prob = home_adjusted / total_strength * 0.85  # Reserve 15% for draw
            away_prob = away_adjusted / total_strength * 0.85
        else:
            home_prob = away_prob = 0.425
        
        draw_prob = 1 - home_prob - away_prob
        
        # Determine winner
        probs = {'Home Win': home_prob, 'Away Win': away_prob, 'Draw': draw_prob}
        predicted = max(probs, key=probs.get)
        
        # Expected goals
        home_avg = home_stats['goals_scored'] / max(home_stats['matches_played'], 1)
        away_avg = away_stats['goals_scored'] / max(away_stats['matches_played'], 1)
        
        # Adjust for defense
        home_defense = away_stats['goals_conceded'] / max(away_stats['matches_played'], 1)
        away_defense = home_stats['goals_conceded'] / max(home_stats['matches_played'], 1)
        
        expected_home = (home_avg + away_defense) / 2 * 1.1  # Home advantage
        expected_away = (away_avg + home_defense) / 2 * 0.9
        
        return {
            'predicted_winner': predicted,
            'probabilities': {
                'Home Win': round(home_prob * 100, 1),
                'Away Win': round(away_prob * 100, 1),
                'Draw': round(draw_prob * 100, 1)
            },
            'expected_goals_home': round(expected_home, 2),
            'expected_goals_away': round(expected_away, 2),
            'confidence': round(max(probs.values()) * 100, 1)
        }


class FootballAnalyzer:
    """Main analyzer class for football match prediction and statistics"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.ds = FootballDataStructure()
        self.predictor = SimpleMLPredictor()
        self.raw_data = []
        
    def load_data(self):
        """Load dataset from CSV"""
        print("=" * 80)
        print("FOOTBALL MATCH ANALYSIS - DATA STRUCTURES & MACHINE LEARNING")
        print("=" * 80)
        print("\n📊 LOADING DATASET...")
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.raw_data = list(reader)
        
        print(f"✅ Loaded {len(self.raw_data)} matches")
        return self.raw_data
    
    def build_data_structures(self):
        """Build custom data structures"""
        print("\n🔧 BUILDING DATA STRUCTURES...")
        
        for row in self.raw_data:
            home_team = row['Home Team']
            away_team = row['Away Team']
            home_goals = int(row['Home Goals'])
            away_goals = int(row['Away Goals'])
            winner = row['Winner']
            competition = row['Competition']
            
            # Determine results
            if winner == 'Home Team':
                home_result, away_result = 'win', 'loss'
            elif winner == 'Away Team':
                home_result, away_result = 'loss', 'win'
            else:
                home_result = away_result = 'draw'
            
            # Update team stats
            self.ds.update_team_stats(
                home_team, True, home_goals, away_goals,
                int(row['Possession % (Home)']), int(row['Shots (Home)']),
                int(row['Corners (Home)']), int(row['Fouls (Home)']), home_result
            )
            
            self.ds.update_team_stats(
                away_team, False, away_goals, home_goals,
                int(row['Possession % (Away)']), int(row['Shots (Away)']),
                int(row['Corners (Away)']), int(row['Fouls (Away)']), away_result
            )
            
            # Update head-to-head
            self.ds.update_head_to_head(home_team, away_team, home_result)
            
            # Update competition stats
            self.ds.competition_stats[competition][home_team] += 1
            self.ds.competition_stats[competition][away_team] += 1
            
            # Store match
            self.ds.matches.append({
                'date': row['Date'],
                'competition': competition,
                'home_team': home_team,
                'away_team': away_team,
                'home_goals': home_goals,
                'away_goals': away_goals,
                'winner': winner,
                'total_goals': home_goals + away_goals
            })
        
        print(f"✅ Data structures built!")
        print(f"   - Teams: {len(self.ds.team_stats)}")
        print(f"   - Competitions: {len(self.ds.competition_stats)}")
        
    def calculate_statistics(self):
        """Calculate comprehensive statistics"""
        print("\n📈 CALCULATING STATISTICS...")
        
        self.team_analysis = []
        
        for team, stats in self.ds.team_stats.items():
            matches = stats['matches_played']
            if matches == 0:
                continue
            
            # Calculate derived metrics
            win_rate = (stats['wins'] / matches) * 100
            draw_rate = (stats['draws'] / matches) * 100
            loss_rate = (stats['losses'] / matches) * 100
            
            avg_scored = stats['goals_scored'] / matches
            avg_conceded = stats['goals_conceded'] / matches
            goal_diff = stats['goals_scored'] - stats['goals_conceded']
            
            home_win_rate = (stats['home_wins'] / max(stats['home_matches'], 1)) * 100
            away_win_rate = (stats['away_wins'] / max(stats['away_matches'], 1)) * 100
            
            points = stats['wins'] * 3 + stats['draws']
            
            analysis = {
                'team': team,
                'matches': matches,
                'wins': stats['wins'],
                'draws': stats['draws'],
                'losses': stats['losses'],
                'win_rate': round(win_rate, 1),
                'draw_rate': round(draw_rate, 1),
                'loss_rate': round(loss_rate, 1),
                'goals_scored': stats['goals_scored'],
                'goals_conceded': stats['goals_conceded'],
                'goal_difference': goal_diff,
                'avg_goals_scored': round(avg_scored, 2),
                'avg_goals_conceded': round(avg_conceded, 2),
                'home_win_rate': round(home_win_rate, 1),
                'away_win_rate': round(away_win_rate, 1),
                'avg_possession': round(stats['possession_total'] / matches, 1),
                'avg_shots': round(stats['shots_total'] / matches, 1),
                'points': points
            }
            
            self.team_analysis.append(analysis)
        
        # Sort by points
        self.team_analysis.sort(key=lambda x: x['points'], reverse=True)
        
        print(f"✅ Statistics calculated for {len(self.team_analysis)} teams")
        
    def display_team_rankings(self):
        """Display team rankings"""
        print("\n" + "=" * 80)
        print("🏆 TEAM RANKINGS (BY POINTS)")
        print("=" * 80)
        print(f"{'Rank':<5} {'Team':<20} {'MP':<4} {'W':<3} {'D':<3} {'L':<3} {'Win%':<6} {'GF':<4} {'GA':<4} {'GD':<5} {'Pts':<4}")
        print("-" * 80)
        
        for i, team in enumerate(self.team_analysis[:15], 1):
            print(f"{i:<5} {team['team']:<20} {team['matches']:<4} {team['wins']:<3} "
                  f"{team['draws']:<3} {team['losses']:<3} {team['win_rate']:<6} "
                  f"{team['goals_scored']:<4} {team['goals_conceded']:<4} "
                  f"{team['goal_difference']:<5} {team['points']:<4}")
    
    def display_goal_statistics(self):
        """Display goal-related statistics"""
        print("\n" + "=" * 80)
        print("⚽ GOAL STATISTICS")
        print("=" * 80)
        
        # Calculate overall stats
        total_matches = len(self.ds.matches)
        total_goals = sum(m['total_goals'] for m in self.ds.matches)
        avg_goals = total_goals / total_matches
        
        home_goals = sum(m['home_goals'] for m in self.ds.matches)
        away_goals = sum(m['away_goals'] for m in self.ds.matches)
        
        print(f"\n📊 OVERALL GOAL STATS:")
        print(f"   Total Goals: {total_goals}")
        print(f"   Average Goals per Match: {avg_goals:.2f}")
        print(f"   Home Team Goals: {home_goals} ({home_goals/total_goals*100:.1f}%)")
        print(f"   Away Team Goals: {away_goals} ({away_goals/total_goals*100:.1f}%)")
        print(f"   Home Advantage: {(home_goals - away_goals) / total_matches:.2f} goals/match")
        
        # Goal distribution
        goal_counts = Counter(m['total_goals'] for m in self.ds.matches)
        print(f"\n📈 GOAL DISTRIBUTION:")
        for goals in sorted(goal_counts.keys())[:10]:
            count = goal_counts[goals]
            pct = count / total_matches * 100
            bar = "█" * int(pct / 2)
            print(f"   {goals} goals: {count:>3} matches ({pct:>5.1f}%) {bar}")
        
        # Best attacks
        print(f"\n🔥 BEST ATTACKS (Avg Goals Scored):")
        best_attack = sorted(self.team_analysis, key=lambda x: x['avg_goals_scored'], reverse=True)[:5]
        for i, team in enumerate(best_attack, 1):
            print(f"   {i}. {team['team']:<20} {team['avg_goals_scored']:.2f} goals/match")
        
        # Best defenses
        print(f"\n🛡️  BEST DEFENSES (Avg Goals Conceded):")
        best_defense = sorted(self.team_analysis, key=lambda x: x['avg_goals_conceded'])[:5]
        for i, team in enumerate(best_defense, 1):
            print(f"   {i}. {team['team']:<20} {team['avg_goals_conceded']:.2f} goals/match")
    
    def display_match_outcomes(self):
        """Display match outcome analysis"""
        print("\n" + "=" * 80)
        print("📋 MATCH OUTCOME ANALYSIS")
        print("=" * 80)
        
        # Count outcomes
        outcomes = Counter(m['winner'] for m in self.ds.matches)
        total = len(self.ds.matches)
        
        print(f"\n📊 OUTCOME DISTRIBUTION:")
        for outcome, count in outcomes.most_common():
            pct = count / total * 100
            bar = "█" * int(pct / 2)
            print(f"   {outcome:<15}: {count:>4} ({pct:>5.1f}%) {bar}")
        
        # Home advantage
        home_wins = outcomes.get('Home Team', 0)
        away_wins = outcomes.get('Away Team', 0)
        draws = outcomes.get('Draw', 0)
        
        print(f"\n🏠 HOME ADVANTAGE:")
        print(f"   Home Win Rate: {home_wins/total*100:.1f}%")
        print(f"   Away Win Rate: {away_wins/total*100:.1f}%")
        print(f"   Draw Rate: {draws/total*100:.1f}%")
        print(f"   Home/Away Ratio: {home_wins/max(away_wins, 1):.2f}x")
        
    def display_head_to_head(self):
        """Display head-to-head analysis"""
        print("\n" + "=" * 80)
        print("⚔️  HEAD-TO-HEAD ANALYSIS")
        print("=" * 80)
        
        # Find most frequent matchups
        matchups = []
        for team1, opponents in self.ds.head_to_head.items():
            for team2, stats in opponents.items():
                total = sum(stats.values())
                if total >= 3:  # Only show matchups with 3+ games
                    matchups.append((team1, team2, total, stats))
        
        matchups.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\n🔥 MOST FREQUENT MATCHUPS:")
        for team1, team2, total, stats in matchups[:5]:
            wins = stats['wins']
            draws = stats['draws']
            losses = stats['losses']
            print(f"\n   {team1} vs {team2} ({total} matches)")
            print(f"      {team1} wins: {wins} | Draws: {draws} | {team2} wins: {losses}")
    
    def run_predictions(self):
        """Run match predictions for sample matchups"""
        print("\n" + "=" * 80)
        print("🤖 MACHINE LEARNING PREDICTIONS")
        print("=" * 80)
        
        # Get top teams
        top_teams = [t['team'] for t in self.team_analysis[:6]]
        
        # Sample predictions
        predictions = [
            (top_teams[0], top_teams[1], 'Premier League'),
            (top_teams[2], top_teams[3], 'UEFA Champions League'),
            (top_teams[1], top_teams[4], 'La Liga'),
        ]
        
        print(f"\n🔮 SAMPLE MATCH PREDICTIONS:")
        
        for home, away, comp in predictions:
            if home != away:
                result = self.predictor.predict_match(home, away, self.ds)
                
                print(f"\n   {'─' * 60}")
                print(f"   🏟️  {home} (Home) vs {away} (Away)")
                print(f"   🏆 Competition: {comp}")
                print(f"\n   📊 PREDICTED OUTCOME: {result['predicted_winner']}")
                print(f"   🎯 Confidence: {result['confidence']}%")
                print(f"\n   📈 Probabilities:")
                for outcome, prob in result['probabilities'].items():
                    bar = "█" * int(prob / 5)
                    print(f"      {outcome:<12}: {prob:>5.1f}% {bar}")
                print(f"\n   ⚽ Expected Goals:")
                print(f"      {home}: {result['expected_goals_home']}")
                print(f"      {away}: {result['expected_goals_away']}")
    
    def predict_custom_match(self, home_team, away_team, competition="Premier League"):
        """Predict a specific match"""
        print(f"\n{'=' * 80}")
        print(f"🎯 CUSTOM MATCH PREDICTION")
        print(f"{'=' * 80}")
        
        result = self.predictor.predict_match(home_team, away_team, self.ds)
        
        print(f"\n🏟️  {home_team} (Home) vs {away_team} (Away)")
        print(f"🏆 Competition: {competition}")
        print(f"\n📊 PREDICTED OUTCOME: {result['predicted_winner']}")
        print(f"🎯 Confidence: {result['confidence']}%")
        print(f"\n📈 Probabilities:")
        for outcome, prob in result['probabilities'].items():
            bar = "█" * int(prob / 5)
            print(f"   {outcome:<12}: {prob:>5.1f}% {bar}")
        print(f"\n⚽ Expected Goals:")
        print(f"   {home_team}: {result['expected_goals_home']}")
        print(f"   {away_team}: {result['expected_goals_away']}")
        
        return result
    
    def display_competition_stats(self):
        """Display competition-wise statistics"""
        print("\n" + "=" * 80)
        print("🏆 COMPETITION ANALYSIS")
        print("=" * 80)
        
        comp_stats = defaultdict(lambda: {'matches': 0, 'total_goals': 0, 'home_wins': 0})
        
        for match in self.ds.matches:
            comp = match['competition']
            comp_stats[comp]['matches'] += 1
            comp_stats[comp]['total_goals'] += match['total_goals']
            if match['winner'] == 'Home Team':
                comp_stats[comp]['home_wins'] += 1
        
        print(f"\n{'Competition':<25} {'Matches':<10} {'Avg Goals':<12} {'Home Win%':<10}")
        print("-" * 60)
        for comp, stats in sorted(comp_stats.items()):
            avg_goals = stats['total_goals'] / stats['matches']
            home_win_pct = stats['home_wins'] / stats['matches'] * 100
            print(f"{comp:<25} {stats['matches']:<10} {avg_goals:<12.2f} {home_win_pct:<10.1f}")
    
    def generate_full_report(self):
        """Generate complete analysis report"""
        self.load_data()
        self.build_data_structures()
        self.calculate_statistics()
        
        # Display all analyses
        self.display_team_rankings()
        self.display_goal_statistics()
        self.display_match_outcomes()
        self.display_head_to_head()
        self.display_competition_stats()
        self.run_predictions()
        
        # Summary
        print("\n" + "=" * 80)
        print("📋 ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"✅ Total matches analyzed: {len(self.ds.matches)}")
        print(f"✅ Teams in dataset: {len(self.ds.team_stats)}")
        print(f"✅ Competitions: {len(self.ds.competition_stats)}")
        print(f"✅ Top team: {self.team_analysis[0]['team']} ({self.team_analysis[0]['points']} points)")
        print(f"✅ Best attack: {max(self.team_analysis, key=lambda x: x['avg_goals_scored'])['team']}")
        print(f"✅ Best defense: {min(self.team_analysis, key=lambda x: x['avg_goals_conceded'])['team']}")
        print("\n" + "=" * 80)


def main():
    """Main execution"""
    # Initialize analyzer
    analyzer = FootballAnalyzer("D:\\prject dsa\\Football_Dataset_2015_2025.csv")
    
    # Run full analysis
    analyzer.generate_full_report()
    
    # Interactive prediction
    print("\n" + "=" * 80)
    print("💡 You can predict any match using:")
    print("   analyzer.predict_custom_match('Team A', 'Team B', 'Competition')")
    print("=" * 80)
    
    return analyzer


if __name__ == "__main__":
    analyzer = main()
