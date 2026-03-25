"""
Football Match Analysis using Data Structures and Machine Learning
Analyzes match data to predict winners and calculate team statistics
"""

import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Machine Learning imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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
            'fouls_total': 0
        })
        self.head_to_head = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'draws': 0, 'losses': 0}))
        self.competition_stats = defaultdict(lambda: defaultdict(int))
        
    def update_team_stats(self, team, is_home, goals_scored, goals_conceded, 
                         possession, shots, corners, fouls, result):
        """Update statistics for a team"""
        stats = self.team_stats[team]
        stats['matches_played'] += 1
        stats['goals_scored'] += goals_scored
        stats['goals_conceded'] += goals_conceded
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


class FootballAnalyzer:
    """Main analyzer class for football match prediction and statistics"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.ds = FootballDataStructure()
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        
    def load_data(self):
        """Load and preprocess the dataset"""
        print("=" * 80)
        print("LOADING FOOTBALL DATASET")
        print("=" * 80)
        
        self.df = pd.read_csv(self.filepath)
        print(f"Total matches loaded: {len(self.df)}")
        print(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        print(f"Competitions: {self.df['Competition'].unique()}")
        print(f"\nDataset shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        return self.df
    
    def clean_and_preprocess(self):
        """Clean and preprocess the data"""
        print("\n" + "=" * 80)
        print("DATA CLEANING & PREPROCESSING")
        print("=" * 80)
        
        # Convert date
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Create result encoding
        self.df['Result_Code'] = self.df['Winner'].map({
            'Home Team': 1,
            'Away Team': 0,
            'Draw': 2
        })
        
        # Calculate goal difference
        self.df['Goal_Difference'] = self.df['Home Goals'] - self.df['Away Goals']
        
        # Create binary outcome (win/loss/draw)
        self.df['Home_Win'] = (self.df['Winner'] == 'Home Team').astype(int)
        self.df['Away_Win'] = (self.df['Winner'] == 'Away Team').astype(int)
        self.df['Is_Draw'] = (self.df['Winner'] == 'Draw').astype(int)
        
        # Calculate total goals
        self.df['Total_Goals'] = self.df['Home Goals'] + self.df['Away Goals']
        
        print(f"Missing values per column:")
        print(self.df.isnull().sum())
        print(f"\nData types:")
        print(self.df.dtypes)
        
        return self.df
    
    def build_data_structures(self):
        """Build custom data structures for analysis"""
        print("\n" + "=" * 80)
        print("BUILDING DATA STRUCTURES")
        print("=" * 80)
        
        for _, row in self.df.iterrows():
            home_team = row['Home Team']
            away_team = row['Away Team']
            home_goals = row['Home Goals']
            away_goals = row['Away Goals']
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
                row['Possession % (Home)'], row['Shots (Home)'],
                row['Corners (Home)'], row['Fouls (Home)'], home_result
            )
            
            self.ds.update_team_stats(
                away_team, False, away_goals, home_goals,
                row['Possession % (Away)'], row['Shots (Away)'],
                row['Corners (Away)'], row['Fouls (Away)'], away_result
            )
            
            # Update head-to-head
            self.ds.update_head_to_head(home_team, away_team, home_result)
            
            # Update competition stats
            self.ds.competition_stats[competition][home_team] += 1
            self.ds.competition_stats[competition][away_team] += 1
        
        print(f"Data structures built successfully!")
        print(f"Total unique teams: {len(self.ds.team_stats)}")
        
    def calculate_team_statistics(self):
        """Calculate comprehensive team statistics"""
        print("\n" + "=" * 80)
        print("TEAM STATISTICS ANALYSIS")
        print("=" * 80)
        
        team_analysis = []
        
        for team, stats in self.ds.team_stats.items():
            matches = stats['matches_played']
            if matches == 0:
                continue
                
            analysis = {
                'Team': team,
                'Matches_Played': matches,
                'Wins': stats['wins'],
                'Draws': stats['draws'],
                'Losses': stats['losses'],
                'Win_Rate_%': round((stats['wins'] / matches) * 100, 2),
                'Draw_Rate_%': round((stats['draws'] / matches) * 100, 2),
                'Loss_Rate_%': round((stats['losses'] / matches) * 100, 2),
                'Goals_Scored': stats['goals_scored'],
                'Goals_Conceded': stats['goals_conceded'],
                'Goal_Difference': stats['goals_scored'] - stats['goals_conceded'],
                'Avg_Goals_Scored': round(stats['goals_scored'] / matches, 2),
                'Avg_Goals_Conceded': round(stats['goals_conceded'] / matches, 2),
                'Home_Matches': stats['home_matches'],
                'Away_Matches': stats['away_matches'],
                'Home_Win_Rate_%': round((stats['home_wins'] / max(stats['home_matches'], 1)) * 100, 2),
                'Away_Win_Rate_%': round((stats['away_wins'] / max(stats['away_matches'], 1)) * 100, 2),
                'Avg_Possession_%': round(stats['possession_total'] / matches, 2),
                'Avg_Shots': round(stats['shots_total'] / matches, 2),
                'Avg_Corners': round(stats['corners_total'] / matches, 2),
                'Avg_Fouls': round(stats['fouls_total'] / matches, 2),
                'Points': stats['wins'] * 3 + stats['draws']
            }
            team_analysis.append(analysis)
        
        self.team_stats_df = pd.DataFrame(team_analysis)
        self.team_stats_df = self.team_stats_df.sort_values('Points', ascending=False)
        
        print("\n--- TOP 10 TEAMS BY POINTS ---")
        print(self.team_stats_df.head(10)[['Team', 'Matches_Played', 'Wins', 'Draws', 'Losses', 
                                            'Win_Rate_%', 'Avg_Goals_Scored', 'Points']].to_string(index=False))
        
        return self.team_stats_df
    
    def analyze_goal_patterns(self):
        """Analyze goal scoring patterns"""
        print("\n" + "=" * 80)
        print("GOAL PATTERN ANALYSIS")
        print("=" * 80)
        
        # Overall goal statistics
        total_goals = self.df['Total_Goals'].sum()
        avg_goals_per_match = self.df['Total_Goals'].mean()
        
        print(f"\n--- OVERALL GOAL STATISTICS ---")
        print(f"Total goals scored: {total_goals}")
        print(f"Average goals per match: {avg_goals_per_match:.2f}")
        print(f"Home team average goals: {self.df['Home Goals'].mean():.2f}")
        print(f"Away team average goals: {self.df['Away Goals'].mean():.2f}")
        
        # Goal distribution
        print(f"\n--- GOAL DISTRIBUTION ---")
        goal_dist = self.df['Total_Goals'].value_counts().sort_index()
        for goals, count in goal_dist.head(10).items():
            percentage = (count / len(self.df)) * 100
            print(f"{goals} goals: {count} matches ({percentage:.1f}%)")
        
        # Clean sheets
        home_clean_sheets = (self.df['Away Goals'] == 0).sum()
        away_clean_sheets = (self.df['Home Goals'] == 0).sum()
        
        print(f"\n--- CLEAN SHEETS ---")
        print(f"Home teams kept clean sheet: {home_clean_sheets} times")
        print(f"Away teams kept clean sheet: {away_clean_sheets} times")
        
        # High scoring matches
        high_scoring = self.df[self.df['Total_Goals'] >= 7]
        print(f"\n--- HIGH SCORING MATCHES (7+ goals) ---")
        print(f"Count: {len(high_scoring)} matches")
        if len(high_scoring) > 0:
            print(f"Highest scoring match: {high_scoring['Total_Goals'].max()} goals")
        
        return {
            'total_goals': total_goals,
            'avg_goals_per_match': avg_goals_per_match,
            'home_advantage': self.df['Home Goals'].mean() - self.df['Away Goals'].mean()
        }
    
    def analyze_match_outcomes(self):
        """Analyze match outcome patterns"""
        print("\n" + "=" * 80)
        print("MATCH OUTCOME ANALYSIS")
        print("=" * 80)
        
        # Overall outcome distribution
        outcomes = self.df['Winner'].value_counts()
        total = len(self.df)
        
        print(f"\n--- OUTCOME DISTRIBUTION ---")
        for outcome, count in outcomes.items():
            percentage = (count / total) * 100
            print(f"{outcome}: {count} ({percentage:.1f}%)")
        
        # Home advantage analysis
        home_win_rate = (self.df['Winner'] == 'Home Team').mean() * 100
        away_win_rate = (self.df['Winner'] == 'Away Team').mean() * 100
        draw_rate = (self.df['Winner'] == 'Draw').mean() * 100
        
        print(f"\n--- HOME ADVANTAGE ANALYSIS ---")
        print(f"Home win rate: {home_win_rate:.1f}%")
        print(f"Away win rate: {away_win_rate:.1f}%")
        print(f"Draw rate: {draw_rate:.1f}%")
        print(f"Home advantage factor: {home_win_rate / away_win_rate:.2f}x")
        
        # By competition
        print(f"\n--- OUTCOMES BY COMPETITION ---")
        competition_outcomes = pd.crosstab(self.df['Competition'], self.df['Winner'], normalize='index') * 100
        print(competition_outcomes.round(1).to_string())
        
        return {
            'home_win_rate': home_win_rate,
            'away_win_rate': away_win_rate,
            'draw_rate': draw_rate
        }
    
    def head_to_head_analysis(self, team1=None, team2=None):
        """Analyze head-to-head matchups"""
        print("\n" + "=" * 80)
        print("HEAD-TO-HEAD ANALYSIS")
        print("=" * 80)
        
        if team1 and team2:
            # Specific matchup
            h2h = self.ds.head_to_head[team1][team2]
            total = sum(h2h.values())
            if total > 0:
                print(f"\n{team1} vs {team2}")
                print(f"  {team1} wins: {h2h['wins']} ({h2h['wins']/total*100:.1f}%)")
                print(f"  Draws: {h2h['draws']} ({h2h['draws']/total*100:.1f}%)")
                print(f"  {team2} wins: {h2h['losses']} ({h2h['losses']/total*100:.1f}%)")
        else:
            # Show top rivalries
            print("\n--- TOP 5 MOST FREQUENT MATCHUPS ---")
            matchups = []
            for team1, opponents in self.ds.head_to_head.items():
                for team2, stats in opponents.items():
                    total = sum(stats.values())
                    if total > 0:
                        matchups.append((team1, team2, total, stats))
            
            matchups.sort(key=lambda x: x[2], reverse=True)
            for team1, team2, total, stats in matchups[:5]:
                print(f"\n{team1} vs {team2}: {total} matches")
                print(f"  {team1} wins: {stats['wins']}, Draws: {stats['draws']}, {team2} wins: {stats['losses']}")
    
    def prepare_ml_features(self):
        """Prepare features for machine learning"""
        print("\n" + "=" * 80)
        print("PREPARING MACHINE LEARNING FEATURES")
        print("=" * 80)
        
        # Create feature dataframe
        features_df = self.df.copy()
        
        # Encode categorical variables
        le_comp = LabelEncoder()
        le_home = LabelEncoder()
        le_away = LabelEncoder()
        
        features_df['Competition_Encoded'] = le_comp.fit_transform(features_df['Competition'])
        features_df['Home_Team_Encoded'] = le_home.fit_transform(features_df['Home Team'])
        features_df['Away_Team_Encoded'] = le_away.fit_transform(features_df['Away Team'])
        
        self.label_encoders['competition'] = le_comp
        self.label_encoders['home_team'] = le_home
        self.label_encoders['away_team'] = le_away
        
        # Feature engineering
        # Add team form (recent performance)
        features_df['Home_Team_Strength'] = features_df['Home Team'].map(
            lambda x: self.ds.team_stats[x]['wins'] / max(self.ds.team_stats[x]['matches_played'], 1)
            if x in self.ds.team_stats else 0.5
        )
        
        features_df['Away_Team_Strength'] = features_df['Away Team'].map(
            lambda x: self.ds.team_stats[x]['wins'] / max(self.ds.team_stats[x]['matches_played'], 1)
            if x in self.ds.team_stats else 0.5
        )
        
        # Historical H2H win rate
        def get_h2h_win_rate(row):
            home = row['Home Team']
            away = row['Away Team']
            h2h = self.ds.head_to_head[home][away]
            total = sum(h2h.values())
            if total > 0:
                return h2h['wins'] / total
            return 0.33  # Neutral if no history
        
        features_df['H2H_Home_Win_Rate'] = features_df.apply(get_h2h_win_rate, axis=1)
        
        # Select features for modeling
        self.feature_columns = [
            'Possession % (Home)', 'Possession % (Away)',
            'Shots (Home)', 'Shots (Away)',
            'Corners (Home)', 'Corners (Away)',
            'Fouls (Home)', 'Fouls (Away)',
            'Competition_Encoded',
            'Home_Team_Encoded', 'Away_Team_Encoded',
            'Home_Team_Strength', 'Away_Team_Strength',
            'H2H_Home_Win_Rate'
        ]
        
        self.X = features_df[self.feature_columns]
        self.y = features_df['Result_Code']
        
        print(f"Features selected: {len(self.feature_columns)}")
        print(f"Feature names: {self.feature_columns}")
        print(f"Dataset shape: {self.X.shape}")
        
        return self.X, self.y
    
    def train_prediction_models(self):
        """Train machine learning models for match prediction"""
        print("\n" + "=" * 80)
        print("TRAINING MACHINE LEARNING MODELS")
        print("=" * 80)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\n--- Training {name} ---")
            
            # Train
            if name == 'Logistic Regression':
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            
            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'predictions': y_pred
            }
            
            print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Select best model
        best_model_name = max(results, key=lambda x: results[x]['accuracy'])
        self.best_model = results[best_model_name]['model']
        
        print(f"\n--- BEST MODEL: {best_model_name} ---")
        print(f"Accuracy: {results[best_model_name]['accuracy']:.4f}")
        
        # Feature importance (for tree-based models)
        if hasattr(self.best_model, 'feature_importances_'):
            print(f"\n--- FEATURE IMPORTANCE ---")
            importances = pd.DataFrame({
                'Feature': self.feature_columns,
                'Importance': self.best_model.feature_importances_
            }).sort_values('Importance', ascending=False)
            print(importances.to_string(index=False))
        
        self.models = results
        return results
    
    def predict_match(self, home_team, away_team, competition, 
                     possession_h=50, possession_a=50, shots_h=15, shots_a=15,
                     corners_h=5, corners_a=5, fouls_h=10, fouls_a=10):
        """Predict outcome of a specific match"""
        print("\n" + "=" * 80)
        print("MATCH PREDICTION")
        print("=" * 80)
        
        print(f"\n{home_team} (Home) vs {away_team} (Away)")
        print(f"Competition: {competition}")
        
        # Prepare input
        try:
            comp_encoded = self.label_encoders['competition'].transform([competition])[0]
        except:
            comp_encoded = 0
            
        try:
            home_encoded = self.label_encoders['home_team'].transform([home_team])[0]
        except:
            home_encoded = 0
            
        try:
            away_encoded = self.label_encoders['away_team'].transform([away_team])[0]
        except:
            away_encoded = 0
        
        # Get team strengths
        home_strength = self.ds.team_stats[home_team]['wins'] / max(self.ds.team_stats[home_team]['matches_played'], 1) if home_team in self.ds.team_stats else 0.5
        away_strength = self.ds.team_stats[away_team]['wins'] / max(self.ds.team_stats[away_team]['matches_played'], 1) if away_team in self.ds.team_stats else 0.5
        
        # H2H
        h2h = self.ds.head_to_head[home_team][away_team]
        total_h2h = sum(h2h.values())
        h2h_rate = h2h['wins'] / total_h2h if total_h2h > 0 else 0.33
        
        input_data = pd.DataFrame([{
            'Possession % (Home)': possession_h,
            'Possession % (Away)': possession_a,
            'Shots (Home)': shots_h,
            'Shots (Away)': shots_a,
            'Corners (Home)': corners_h,
            'Corners (Away)': corners_a,
            'Fouls (Home)': fouls_h,
            'Fouls (Away)': fouls_a,
            'Competition_Encoded': comp_encoded,
            'Home_Team_Encoded': home_encoded,
            'Away_Team_Encoded': away_encoded,
            'Home_Team_Strength': home_strength,
            'Away_Team_Strength': away_strength,
            'H2H_Home_Win_Rate': h2h_rate
        }])
        
        # Predict
        prediction = self.best_model.predict(input_data[self.feature_columns])[0]
        probabilities = self.best_model.predict_proba(input_data[self.feature_columns])[0]
        
        outcome_map = {0: 'Away Team Win', 1: 'Home Team Win', 2: 'Draw'}
        predicted_outcome = outcome_map[prediction]
        
        print(f"\n--- PREDICTION RESULT ---")
        print(f"Predicted Winner: {predicted_outcome}")
        print(f"\nConfidence Probabilities:")
        print(f"  Home Win: {probabilities[1]*100:.1f}%")
        print(f"  Away Win: {probabilities[0]*100:.1f}%")
        print(f"  Draw: {probabilities[2]*100:.1f}%")
        
        # Expected goals estimation based on historical data
        home_avg = self.ds.team_stats[home_team]['Avg_Goals_Scored'] if home_team in self.ds.team_stats else 1.5
        away_avg = self.ds.team_stats[away_team]['Avg_Goals_Scored'] if away_team in self.ds.team_stats else 1.2
        
        print(f"\n--- EXPECTED GOALS ---")
        print(f"{home_team}: {home_avg:.2f} goals")
        print(f"{away_team}: {away_avg:.2f} goals")
        print(f"Total expected: {home_avg + away_avg:.2f} goals")
        
        return {
            'predicted_winner': predicted_outcome,
            'probabilities': probabilities,
            'expected_goals_home': home_avg,
            'expected_goals_away': away_avg
        }
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 80)
        
        # 1. Dataset Overview
        print("\n" + "-" * 40)
        print("1. DATASET OVERVIEW")
        print("-" * 40)
        print(f"Total Matches: {len(self.df)}")
        print(f"Date Range: {self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}")
        print(f"Teams: {len(self.ds.team_stats)}")
        print(f"Competitions: {', '.join(self.df['Competition'].unique())}")
        
        # 2. Team Rankings
        print("\n" + "-" * 40)
        print("2. TEAM RANKINGS (BY POINTS)")
        print("-" * 40)
        rankings = self.team_stats_df[['Team', 'Matches_Played', 'Wins', 'Draws', 'Losses', 
                                        'Win_Rate_%', 'Avg_Goals_Scored', 'Goal_Difference', 'Points']].head(10)
        print(rankings.to_string(index=False))
        
        # 3. Best Attack
        print("\n" + "-" * 40)
        print("3. BEST ATTACK (Avg Goals Scored)")
        print("-" * 40)
        best_attack = self.team_stats_df.nlargest(5, 'Avg_Goals_Scored')[['Team', 'Avg_Goals_Scored', 'Goals_Scored', 'Matches_Played']]
        print(best_attack.to_string(index=False))
        
        # 4. Best Defense
        print("\n" + "-" * 40)
        print("4. BEST DEFENSE (Avg Goals Conceded)")
        print("-" * 40)
        best_defense = self.team_stats_df.nsmallest(5, 'Avg_Goals_Conceded')[['Team', 'Avg_Goals_Conceded', 'Goals_Conceded', 'Matches_Played']]
        print(best_defense.to_string(index=False))
        
        # 5. Home vs Away Performance
        print("\n" + "-" * 40)
        print("5. HOME VS AWAY PERFORMANCE")
        print("-" * 40)
        home_away = self.team_stats_df[['Team', 'Home_Win_Rate_%', 'Away_Win_Rate_%']].head(10)
        home_away['Difference'] = home_away['Home_Win_Rate_%'] - home_away['Away_Win_Rate_%']
        print(home_away.to_string(index=False))
        
        # 6. Competition Analysis
        print("\n" + "-" * 40)
        print("6. COMPETITION ANALYSIS")
        print("-" * 40)
        comp_analysis = self.df.groupby('Competition').agg({
            'Total_Goals': 'mean',
            'Home Goals': 'mean',
            'Away Goals': 'mean'
        }).round(2)
        print(comp_analysis.to_string())
        
        # 7. Model Performance
        print("\n" + "-" * 40)
        print("7. PREDICTION MODEL PERFORMANCE")
        print("-" * 40)
        for name, result in self.models.items():
            print(f"{name}: {result['accuracy']*100:.2f}% accuracy")
        
        print("\n" + "=" * 80)
        print("END OF REPORT")
        print("=" * 80)


def main():
    """Main execution function"""
    # Initialize analyzer
    analyzer = FootballAnalyzer("D:\\prject dsa\\Football_Dataset_2015_2025.csv")
    
    # Run complete analysis pipeline
    analyzer.load_data()
    analyzer.clean_and_preprocess()
    analyzer.build_data_structures()
    analyzer.calculate_team_statistics()
    analyzer.analyze_goal_patterns()
    analyzer.analyze_match_outcomes()
    analyzer.head_to_head_analysis()
    analyzer.prepare_ml_features()
    analyzer.train_prediction_models()
    
    # Generate comprehensive report
    analyzer.generate_comprehensive_report()
    
    # Example predictions
    print("\n" + "=" * 80)
    print("SAMPLE MATCH PREDICTIONS")
    print("=" * 80)
    
    # Get top teams for prediction examples
    top_teams = analyzer.team_stats_df.head(4)['Team'].tolist()
    
    if len(top_teams) >= 2:
        analyzer.predict_match(
            top_teams[0], top_teams[1], 'Premier League',
            possession_h=55, possession_a=45, shots_h=18, shots_a=12
        )
        
        analyzer.predict_match(
            top_teams[2], top_teams[3], 'UEFA Champions League',
            possession_h=50, possession_a=50, shots_h=15, shots_a=15
        )
    
    return analyzer


if __name__ == "__main__":
    analyzer = main()
