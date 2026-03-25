"""
Football Match Predictor Web Server
Uses only Python standard library (http.server)
"""

import http.server
import socketserver
import urllib.parse
import json
from football_analysis_stdlib import FootballAnalyzer
import threading
import webbrowser

# Initialize analyzer globally
print("Loading football data... Please wait...")
analyzer = FootballAnalyzer("D:\\prject dsa\\Football_Dataset_2015_2025.csv")
analyzer.load_data()
analyzer.build_data_structures()
analyzer.calculate_statistics()

teams = [t['team'] for t in analyzer.team_analysis]
print(f"✅ Server ready with {len(teams)} teams!")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ Football Match Predictor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 30px 0;
            color: white;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .match-selector {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 20px;
            align-items: end;
        }
        
        @media (max-width: 600px) {
            .match-selector {
                grid-template-columns: 1fr;
            }
        }
        
        .team-select {
            text-align: center;
        }
        
        .team-select label {
            display: block;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        
        .team-select select {
            width: 100%;
            padding: 12px;
            font-size: 1em;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }
        
        .team-select select:hover {
            border-color: #2a5298;
        }
        
        .vs {
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
            color: #e74c3c;
            padding-bottom: 12px;
        }
        
        .btn-predict {
            width: 100%;
            padding: 15px;
            font-size: 1.2em;
            font-weight: bold;
            color: white;
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 20px;
        }
        
        .btn-predict:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
        }
        
        .prediction-result {
            display: none;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .winner-display {
            text-align: center;
            padding: 25px;
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
        }
        
        .winner-display h2 {
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        
        .confidence {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .probabilities {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .prob-card {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        
        .prob-card.home { background: linear-gradient(135deg, #27ae60 0%, #219a52 100%); }
        .prob-card.draw { background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%); }
        .prob-card.away { background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); }
        
        .prob-card h3 {
            font-size: 0.9em;
            margin-bottom: 10px;
            opacity: 0.9;
        }
        
        .prob-card .percent {
            font-size: 2em;
            font-weight: bold;
        }
        
        .expected-goals {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .goal-card {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        
        .goal-card h4 {
            color: #666;
            margin-bottom: 10px;
        }
        
        .goal-card .goals {
            font-size: 2.5em;
            font-weight: bold;
            color: #2a5298;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-item .label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .stat-item .value {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 30px;
        }
        
        .loading-spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #2a5298;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .team-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        
        .team-stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        
        .team-stat-card h4 {
            color: #2a5298;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }
        
        .stat-row:last-child {
            border-bottom: none;
        }
        
        footer {
            text-align: center;
            padding: 20px;
            color: white;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚽ Football Match Predictor</h1>
            <p>AI-powered match outcome prediction using Machine Learning</p>
        </header>
        
        <div class="card">
            <div class="match-selector">
                <div class="team-select">
                    <label for="homeTeam">🏠 Home Team</label>
                    <select id="homeTeam">
                        <option value="">Select Team...</option>
                        {team_options}
                    </select>
                </div>
                
                <div class="vs">VS</div>
                
                <div class="team-select">
                    <label for="awayTeam">✈️ Away Team</label>
                    <select id="awayTeam">
                        <option value="">Select Team...</option>
                        {team_options}
                    </select>
                </div>
            </div>
            
            <button class="btn-predict" onclick="predictMatch()">
                🔮 Predict Match Result
            </button>
            
            <div class="loading" id="loading">
                <div class="loading-spinner"></div>
                <p>Analyzing match data...</p>
            </div>
            
            <div class="prediction-result" id="result">
                <!-- Results will be inserted here -->
            </div>
        </div>
        
        <footer>
            <p>Powered by Data Structures & Machine Learning | 3,000 matches analyzed</p>
        </footer>
    </div>
    
    <script>
        async function predictMatch() {
            const homeTeam = document.getElementById('homeTeam').value;
            const awayTeam = document.getElementById('awayTeam').value;
            
            if (!homeTeam || !awayTeam) {
                alert('Please select both teams!');
                return;
            }
            
            if (homeTeam === awayTeam) {
                alert('Please select two different teams!');
                return;
            }
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch(`/predict?home=${encodeURIComponent(homeTeam)}&away=${encodeURIComponent(awayTeam)}`);
                const data = await response.json();
                
                displayResult(data);
            } catch (error) {
                alert('Error making prediction. Please try again.');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function displayResult(data) {
            const resultDiv = document.getElementById('result');
            
            let winnerText = '';
            let winnerClass = '';
            if (data.predicted_winner === 'Home Win') {
                winnerText = `🏆 ${data.home_team} Wins!`;
                winnerClass = 'home';
            } else if (data.predicted_winner === 'Away Win') {
                winnerText = `🏆 ${data.away_team} Wins!`;
                winnerClass = 'away';
            } else {
                winnerText = '🤝 Draw!';
                winnerClass = 'draw';
            }
            
            resultDiv.innerHTML = `
                <div class="winner-display">
                    <h2>${winnerText}</h2>
                    <p class="confidence">Confidence: ${data.confidence}%</p>
                </div>
                
                <h3 style="margin-bottom: 15px; color: #333;">📊 Win Probabilities</h3>
                <div class="probabilities">
                    <div class="prob-card home">
                        <h3>🏠 Home Win</h3>
                        <div class="percent">${data.probabilities['Home Win']}%</div>
                    </div>
                    <div class="prob-card draw">
                        <h3>⚖️ Draw</h3>
                        <div class="percent">${data.probabilities['Draw']}%</div>
                    </div>
                    <div class="prob-card away">
                        <h3>✈️ Away Win</h3>
                        <div class="percent">${data.probabilities['Away Win']}%</div>
                    </div>
                </div>
                
                <h3 style="margin-bottom: 15px; color: #333;">⚽ Expected Goals</h3>
                <div class="expected-goals">
                    <div class="goal-card">
                        <h4>${data.home_team}</h4>
                        <div class="goals">${data.expected_goals_home}</div>
                    </div>
                    <div class="goal-card">
                        <h4>${data.away_team}</h4>
                        <div class="goals">${data.expected_goals_away}</div>
                    </div>
                </div>
                
                <h3 style="margin: 20px 0 15px; color: #333;">📈 Team Statistics</h3>
                <div class="team-stats">
                    <div class="team-stat-card">
                        <h4>${data.home_team}</h4>
                        <div class="stat-row">
                            <span>Win Rate:</span>
                            <strong>${data.home_stats.win_rate}%</strong>
                        </div>
                        <div class="stat-row">
                            <span>Avg Goals:</span>
                            <strong>${data.home_stats.avg_goals}</strong>
                        </div>
                        <div class="stat-row">
                            <span>Goals Conceded:</span>
                            <strong>${data.home_stats.avg_conceded}</strong>
                        </div>
                        <div class="stat-row">
                            <span>Matches Played:</span>
                            <strong>${data.home_stats.matches}</strong>
                        </div>
                    </div>
                    <div class="team-stat-card">
                        <h4>${data.away_team}</h4>
                        <div class="stat-row">
                            <span>Win Rate:</span>
                            <strong>${data.away_stats.win_rate}%</strong>
                        </div>
                        <div class="stat-row">
                            <span>Avg Goals:</span>
                            <strong>${data.away_stats.avg_goals}</strong>
                        </div>
                        <div class="stat-row">
                            <span>Goals Conceded:</span>
                            <strong>${data.away_stats.avg_conceded}</strong>
                        </div>
                        <div class="stat-row">
                            <span>Matches Played:</span>
                            <strong>${data.away_stats.matches}</strong>
                        </div>
                    </div>
                </div>
            `;
            
            resultDiv.style.display = 'block';
        }
    </script>
</body>
</html>
'''

class PredictorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        if path == '/':
            # Serve main page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Generate team options
            team_options = '\n'.join([f'<option value="{team}">{team}</option>' for team in teams])
            html = HTML_TEMPLATE.replace('{team_options}', team_options)
            self.wfile.write(html.encode())
            
        elif path == '/predict':
            # Handle prediction request
            home_team = query.get('home', [''])[0]
            away_team = query.get('away', [''])[0]
            
            if home_team and away_team:
                try:
                    result = analyzer.predict_custom_match(home_team, away_team)
                    
                    # Get team stats
                    home_stats = next((t for t in analyzer.team_analysis if t['team'] == home_team), {})
                    away_stats = next((t for t in analyzer.team_analysis if t['team'] == away_team), {})
                    
                    response = {
                        'home_team': home_team,
                        'away_team': away_team,
                        'predicted_winner': result['predicted_winner'],
                        'probabilities': result['probabilities'],
                        'expected_goals_home': result['expected_goals_home'],
                        'expected_goals_away': result['expected_goals_away'],
                        'confidence': result['confidence'],
                        'home_stats': {
                            'win_rate': home_stats.get('win_rate', 0),
                            'avg_goals': home_stats.get('avg_goals_scored', 0),
                            'avg_conceded': home_stats.get('avg_goals_conceded', 0),
                            'matches': home_stats.get('matches', 0)
                        },
                        'away_stats': {
                            'win_rate': away_stats.get('win_rate', 0),
                            'avg_goals': away_stats.get('avg_goals_scored', 0),
                            'avg_conceded': away_stats.get('avg_goals_conceded', 0),
                            'matches': away_stats.get('matches', 0)
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=8080):
    with socketserver.TCPServer(("", port), PredictorHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"🚀 Server running at: http://localhost:{port}")
        print(f"{'='*60}")
        print("\n📱 Open your browser and go to the URL above")
        print("🛑 Press Ctrl+C to stop the server\n")
        
        # Open browser automatically
        webbrowser.open(f'http://localhost:{port}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped.")

if __name__ == "__main__":
    run_server()
