"""
Modern Football Match Predictor Web Server
Premium dark futuristic sports analytics theme
"""

import http.server
import socketserver
import urllib.parse
import json
from football_analysis_stdlib import FootballAnalyzer
import webbrowser

# Initialize analyzer globally
print("Loading football data... Please wait...")
analyzer = FootballAnalyzer("D:\\prject dsa\\Football_Dataset_2015_2025.csv")
analyzer.load_data()
analyzer.build_data_structures()
analyzer.calculate_statistics()

teams = [t['team'] for t in analyzer.team_analysis]
print(f"✅ Server ready with {len(teams)} teams!")

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ Football Match Predictor | AI Analytics</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #0a0e27;
            --deep-blue: #050811;
            --neon-purple: #b829dd;
            --electric-cyan: #00d4ff;
            --accent-pink: #ff006e;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glow-purple: 0 0 30px rgba(184, 41, 221, 0.3);
            --glow-cyan: 0 0 30px rgba(0, 212, 255, 0.3);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--deep-blue);
            min-height: 100vh;
            overflow-x: hidden;
            color: #fff;
        }

        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(184, 41, 221, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(0, 212, 255, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(255, 0, 110, 0.05) 0%, transparent 70%),
                var(--deep-blue);
        }

        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: var(--electric-cyan);
            border-radius: 50%;
            opacity: 0;
            animation: float 15s infinite;
            box-shadow: 0 0 10px var(--electric-cyan);
        }

        @keyframes float {
            0%, 100% { 
                opacity: 0; 
                transform: translateY(100vh) scale(0);
            }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { 
                opacity: 0; 
                transform: translateY(-100vh) scale(1.5);
            }
        }

        /* Grid Overlay */
        .grid-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-image: 
                linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
        }

        @keyframes gridMove {
            0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
            100% { transform: perspective(500px) rotateX(60deg) translateY(50px); }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Header */
        header {
            text-align: center;
            padding: 40px 0;
            animation: slideDown 0.8s ease-out;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .logo {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }

        .logo-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--neon-purple), var(--electric-cyan));
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            box-shadow: var(--glow-purple);
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        h1 {
            font-family: 'Poppins', sans-serif;
            font-size: 3em;
            font-weight: 800;
            background: linear-gradient(135deg, #fff 0%, var(--electric-cyan) 50%, var(--neon-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 40px rgba(0, 212, 255, 0.3);
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.6);
            font-size: 1.1em;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* Glass Card */
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            animation: slideUp 0.8s ease-out 0.2s both;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        }

        /* Match Selector */
        .match-selector {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 30px;
            align-items: end;
            position: relative;
        }

        @media (max-width: 768px) {
            .match-selector {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            .vs-divider {
                transform: rotate(90deg);
                margin: 10px 0;
            }
        }

        .team-section {
            text-align: center;
        }

        .team-label {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .team-select-wrapper {
            position: relative;
        }

        select {
            width: 100%;
            padding: 18px 50px 18px 20px;
            font-size: 1.1em;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            color: #fff;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid var(--glass-border);
            border-radius: 16px;
            cursor: pointer;
            appearance: none;
            transition: all 0.3s ease;
        }

        select:hover {
            border-color: var(--electric-cyan);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
        }

        select:focus {
            outline: none;
            border-color: var(--neon-purple);
            box-shadow: var(--glow-purple);
        }

        .select-arrow {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
            color: var(--electric-cyan);
            font-size: 12px;
        }

        .vs-divider {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }

        .vs-text {
            font-family: 'Poppins', sans-serif;
            font-size: 1.5em;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-pink), var(--neon-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .vs-line {
            width: 2px;
            height: 40px;
            background: linear-gradient(180deg, transparent, var(--neon-purple), transparent);
        }

        /* Predict Button */
        .predict-btn {
            width: 100%;
            margin-top: 30px;
            padding: 20px 40px;
            font-family: 'Poppins', sans-serif;
            font-size: 1.2em;
            font-weight: 700;
            color: #fff;
            background: linear-gradient(135deg, var(--neon-purple), var(--accent-pink));
            border: none;
            border-radius: 16px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(184, 41, 221, 0.3);
        }

        .predict-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }

        .predict-btn:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 15px 40px rgba(184, 41, 221, 0.4);
        }

        .predict-btn:hover::before {
            left: 100%;
        }

        .predict-btn:active {
            transform: translateY(-1px) scale(0.98);
        }

        /* Loading State */
        .loading-container {
            display: none;
            text-align: center;
            padding: 60px 20px;
        }

        .loading-container.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .spinner {
            width: 80px;
            height: 80px;
            margin: 0 auto 30px;
            position: relative;
        }

        .spinner-ring {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 4px solid transparent;
            border-top-color: var(--electric-cyan);
            animation: spin 1s linear infinite;
        }

        .spinner-ring:nth-child(2) {
            width: 70%;
            height: 70%;
            top: 15%;
            left: 15%;
            border-top-color: var(--neon-purple);
            animation: spin 1.5s linear infinite reverse;
        }

        .spinner-ring:nth-child(3) {
            width: 40%;
            height: 40%;
            top: 30%;
            left: 30%;
            border-top-color: var(--accent-pink);
            animation: spin 2s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-text {
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.8);
            animation: pulse 1.5s ease-in-out infinite;
        }

        /* Results Section */
        .results-container {
            display: none;
            animation: resultPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .results-container.active {
            display: block;
        }

        @keyframes resultPop {
            from { 
                opacity: 0; 
                transform: scale(0.8) translateY(30px);
            }
            to { 
                opacity: 1; 
                transform: scale(1) translateY(0);
            }
        }

        /* Winner Banner */
        .winner-banner {
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, rgba(184, 41, 221, 0.2), rgba(0, 212, 255, 0.2));
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }

        .winner-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255, 255, 255, 0.1) 50%,
                transparent 70%
            );
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }

        .winner-trophy {
            font-size: 4em;
            margin-bottom: 15px;
            animation: bounce 1s ease infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .winner-text {
            font-family: 'Poppins', sans-serif;
            font-size: 2em;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, var(--electric-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            z-index: 1;
        }

        .confidence-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
            padding: 10px 25px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 50px;
            font-size: 0.95em;
            color: rgba(255, 255, 255, 0.9);
        }

        .confidence-value {
            font-weight: 700;
            color: var(--electric-cyan);
        }

        /* Probability Bars */
        .probabilities-section {
            margin-bottom: 30px;
        }

        .section-title {
            font-family: 'Poppins', sans-serif;
            font-size: 1.1em;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .prob-bar-container {
            margin-bottom: 20px;
        }

        .prob-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.95em;
        }

        .prob-name {
            display: flex;
            align-items: center;
            gap: 8px;
            color: rgba(255, 255, 255, 0.9);
        }

        .prob-value {
            font-weight: 700;
            font-family: 'Poppins', sans-serif;
        }

        .prob-bar-bg {
            height: 12px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }

        .prob-bar-fill {
            height: 100%;
            border-radius: 10px;
            position: relative;
            width: 0;
            transition: width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .prob-bar-fill.home {
            background: linear-gradient(90deg, #27ae60, #2ecc71);
            box-shadow: 0 0 20px rgba(46, 204, 113, 0.4);
        }

        .prob-bar-fill.draw {
            background: linear-gradient(90deg, #95a5a6, #bdc3c7);
            box-shadow: 0 0 20px rgba(189, 195, 199, 0.4);
        }

        .prob-bar-fill.away {
            background: linear-gradient(90deg, #e74c3c, #ff6b6b);
            box-shadow: 0 0 20px rgba(231, 76, 60, 0.4);
        }

        .prob-bar-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: barShine 2s infinite;
        }

        @keyframes barShine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* Expected Goals */
        .goals-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        @media (max-width: 600px) {
            .goals-section {
                grid-template-columns: 1fr;
            }
        }

        .goal-card {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            border: 1px solid var(--glass-border);
            position: relative;
            overflow: hidden;
        }

        .goal-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--neon-purple), var(--electric-cyan));
        }

        .goal-team {
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .goal-number {
            font-family: 'Poppins', sans-serif;
            font-size: 4em;
            font-weight: 800;
            background: linear-gradient(135deg, var(--electric-cyan), var(--neon-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
        }

        .goal-label {
            font-size: 0.85em;
            color: rgba(255, 255, 255, 0.5);
            margin-top: 5px;
        }

        /* Team Stats */
        .stats-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        @media (max-width: 600px) {
            .stats-section {
                grid-template-columns: 1fr;
            }
        }

        .stats-card {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid var(--glass-border);
        }

        .stats-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--glass-border);
        }

        .stats-team-icon {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, var(--neon-purple), var(--electric-cyan));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .stats-team-name {
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 1.1em;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .stat-row:last-child {
            border-bottom: none;
        }

        .stat-name {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9em;
        }

        .stat-value {
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            color: var(--electric-cyan);
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 30px;
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.9em;
        }

        footer span {
            color: var(--electric-cyan);
        }

        /* Intensity Meter */
        .intensity-section {
            margin-bottom: 30px;
        }

        .intensity-meter {
            height: 30px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }

        .intensity-fill {
            height: 100%;
            background: linear-gradient(90deg, #27ae60, #f1c40f, #e74c3c);
            border-radius: 15px;
            width: 0;
            transition: width 1.5s ease;
            position: relative;
        }

        .intensity-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }

        .intensity-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 8px;
            font-size: 0.8em;
            color: rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    <div class="grid-overlay"></div>
    <div class="particles" id="particles"></div>

    <div class="container">
        <header>
            <div class="logo">
                <div class="logo-icon">⚽</div>
                <div>
                    <h1>Match Predictor</h1>
                    <p class="subtitle">AI-Powered Football Analytics</p>
                </div>
            </div>
        </header>

        <div class="glass-card">
            <div class="match-selector">
                <div class="team-section">
                    <div class="team-label">
                        <span>🏠</span> Home Team
                    </div>
                    <div class="team-select-wrapper">
                        <select id="homeTeam">
                            <option value="">Select Team</option>
                            {team_options}
                        </select>
                        <span class="select-arrow">▼</span>
                    </div>
                </div>

                <div class="vs-divider">
                    <div class="vs-line"></div>
                    <span class="vs-text">VS</span>
                    <div class="vs-line"></div>
                </div>

                <div class="team-section">
                    <div class="team-label">
                        <span>✈️</span> Away Team
                    </div>
                    <div class="team-select-wrapper">
                        <select id="awayTeam">
                            <option value="">Select Team</option>
                            {team_options}
                        </select>
                        <span class="select-arrow">▼</span>
                    </div>
                </div>
            </div>

            <button class="predict-btn" onclick="predictMatch()">
                🔮 Predict Match Result
            </button>

            <div class="loading-container" id="loading">
                <div class="spinner">
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                </div>
                <p class="loading-text">Analyzing match data with AI...</p>
            </div>

            <div class="results-container" id="results"></div>
        </div>

        <footer>
            <p>Powered by <span>Machine Learning</span> & <span>Data Structures</span> | 3,000+ Matches Analyzed</p>
        </footer>
    </div>

    <script>
        // Create floating particles
        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 30; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = (10 + Math.random() * 10) + 's';
                container.appendChild(particle);
            }
        }
        createParticles();

        // Animate number counting
        function animateNumber(element, target, duration = 1500, suffix = '') {
            let start = 0;
            const increment = target / (duration / 16);
            const timer = setInterval(() => {
                start += increment;
                if (start >= target) {
                    element.textContent = target + suffix;
                    clearInterval(timer);
                } else {
                    element.textContent = start.toFixed(1) + suffix;
                }
            }, 16);
        }

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
            document.getElementById('loading').classList.add('active');
            document.getElementById('results').classList.remove('active');

            try {
                const response = await fetch(`/predict?home=${encodeURIComponent(homeTeam)}&away=${encodeURIComponent(awayTeam)}`);
                const data = await response.json();

                setTimeout(() => {
                    displayResults(data);
                    document.getElementById('loading').classList.remove('active');
                }, 1500);
            } catch (error) {
                alert('Error making prediction. Please try again.');
                document.getElementById('loading').classList.remove('active');
            }
        }

        function displayResults(data) {
            const resultsDiv = document.getElementById('results');

            let winnerEmoji = '';
            let winnerText = '';
            if (data.predicted_winner === 'Home Win') {
                winnerEmoji = '🏆';
                winnerText = data.home_team + ' Wins!';
            } else if (data.predicted_winner === 'Away Win') {
                winnerEmoji = '🏆';
                winnerText = data.away_team + ' Wins!';
            } else {
                winnerEmoji = '🤝';
                winnerText = 'Match Draw!';
            }

            // Calculate intensity (based on close probabilities)
            const probs = data.probabilities;
            const maxProb = Math.max(probs['Home Win'], probs['Away Win'], probs['Draw']);
            const intensity = Math.round((100 - Math.abs(probs['Home Win'] - probs['Away Win'])) * 0.8 + 20);

            resultsDiv.innerHTML = `
                <div class="winner-banner">
                    <div class="winner-trophy">${winnerEmoji}</div>
                    <h2 class="winner-text">${winnerText}</h2>
                    <div class="confidence-badge">
                        <span>🎯</span>
                        <span>AI Confidence: <span class="confidence-value">${data.confidence}%</span></span>
                    </div>
                </div>

                <div class="intensity-section">
                    <div class="section-title">
                        <span>🔥</span> Match Intensity Meter
                    </div>
                    <div class="intensity-meter">
                        <div class="intensity-fill" id="intensityFill"></div>
                    </div>
                    <div class="intensity-labels">
                        <span>Friendly</span>
                        <span>Competitive</span>
                        <span>Intense</span>
                    </div>
                </div>

                <div class="probabilities-section">
                    <div class="section-title">
                        <span>📊</span> Win Probabilities
                    </div>

                    <div class="prob-bar-container">
                        <div class="prob-label">
                            <span class="prob-name">🏠 Home Win</span>
                            <span class="prob-value" id="homeProb">0%</span>
                        </div>
                        <div class="prob-bar-bg">
                            <div class="prob-bar-fill home" id="homeBar"></div>
                        </div>
                    </div>

                    <div class="prob-bar-container">
                        <div class="prob-label">
                            <span class="prob-name">⚖️ Draw</span>
                            <span class="prob-value" id="drawProb">0%</span>
                        </div>
                        <div class="prob-bar-bg">
                            <div class="prob-bar-fill draw" id="drawBar"></div>
                        </div>
                    </div>

                    <div class="prob-bar-container">
                        <div class="prob-label">
                            <span class="prob-name">✈️ Away Win</span>
                            <span class="prob-value" id="awayProb">0%</span>
                        </div>
                        <div class="prob-bar-bg">
                            <div class="prob-bar-fill away" id="awayBar"></div>
                        </div>
                    </div>
                </div>

                <div class="goals-section">
                    <div class="goal-card">
                        <div class="goal-team">${data.home_team}</div>
                        <div class="goal-number" id="homeGoals">0</div>
                        <div class="goal-label">Expected Goals</div>
                    </div>
                    <div class="goal-card">
                        <div class="goal-team">${data.away_team}</div>
                        <div class="goal-number" id="awayGoals">0</div>
                        <div class="goal-label">Expected Goals</div>
                    </div>
                </div>

                <div class="section-title">
                    <span>📈</span> Team Statistics
                </div>
                <div class="stats-section">
                    <div class="stats-card">
                        <div class="stats-header">
                            <div class="stats-team-icon">🏠</div>
                            <span class="stats-team-name">${data.home_team}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Win Rate</span>
                            <span class="stat-value">${data.home_stats.win_rate}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Avg Goals</span>
                            <span class="stat-value">${data.home_stats.avg_goals}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Goals Conceded</span>
                            <span class="stat-value">${data.home_stats.avg_conceded}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Matches</span>
                            <span class="stat-value">${data.home_stats.matches}</span>
                        </div>
                    </div>
                    <div class="stats-card">
                        <div class="stats-header">
                            <div class="stats-team-icon">✈️</div>
                            <span class="stats-team-name">${data.away_team}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Win Rate</span>
                            <span class="stat-value">${data.away_stats.win_rate}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Avg Goals</span>
                            <span class="stat-value">${data.away_stats.avg_goals}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Goals Conceded</span>
                            <span class="stat-value">${data.away_stats.avg_conceded}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Matches</span>
                            <span class="stat-value">${data.away_stats.matches}</span>
                        </div>
                    </div>
                </div>
            `;

            resultsDiv.classList.add('active');

            // Animate bars and numbers
            setTimeout(() => {
                document.getElementById('intensityFill').style.width = intensity + '%';

                document.getElementById('homeBar').style.width = data.probabilities['Home Win'] + '%';
                document.getElementById('drawBar').style.width = data.probabilities['Draw'] + '%';
                document.getElementById('awayBar').style.width = data.probabilities['Away Win'] + '%';

                animateNumber(document.getElementById('homeProb'), data.probabilities['Home Win'], 1500, '%');
                animateNumber(document.getElementById('drawProb'), data.probabilities['Draw'], 1500, '%');
                animateNumber(document.getElementById('awayProb'), data.probabilities['Away Win'], 1500, '%');

                animateNumber(document.getElementById('homeGoals'), data.expected_goals_home, 1500);
                animateNumber(document.getElementById('awayGoals'), data.expected_goals_away, 1500);
            }, 100);
        }
    </script>
</body>
</html>'''

class PredictorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            team_options = '\n'.join([f'<option value="{team}">{team}</option>' for team in teams])
            html = HTML_TEMPLATE.replace('{team_options}', team_options)
            self.wfile.write(html.encode())

        elif path == '/predict':
            home_team = query.get('home', [''])[0]
            away_team = query.get('away', [''])[0]

            if home_team and away_team:
                try:
                    result = analyzer.predict_custom_match(home_team, away_team)

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
        pass

def run_server(port=8080):
    with socketserver.TCPServer(("", port), PredictorHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"🚀 MODERN FOOTBALL PREDICTOR RUNNING")
        print(f"{'='*60}")
        print(f"\n✨ Open: http://localhost:{port}")
        print("🛑 Press Ctrl+C to stop\n")

        webbrowser.open(f'http://localhost:{port}')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped.")

if __name__ == "__main__":
    run_server()
