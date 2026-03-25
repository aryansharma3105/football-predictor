"""
Football Match Predictor Web Server
Stadium theme with solid colors and spinning football loader
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
    <title>⚽ Football Match Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --sky-blue: #87CEEB;
            --grass-green: #2d5a27;
            --light-grass: #4a7c43;
            --white: #ffffff;
            --dark: #1a1a1a;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(180deg, var(--sky-blue) 0%, var(--sky-blue) 50%, var(--grass-green) 50%, var(--light-grass) 100%);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        /* Stadium Background */
        .stadium-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }

        /* Sky */
        .sky {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 50%;
            background: linear-gradient(180deg, #4FC3F7 0%, #87CEEB 100%);
        }

        /* Clouds */
        .cloud {
            position: absolute;
            background: white;
            border-radius: 100px;
            opacity: 0.9;
            animation: float-cloud 25s infinite linear;
        }

        .cloud::before {
            content: '';
            position: absolute;
            background: white;
            border-radius: 100px;
        }

        .cloud1 {
            width: 80px;
            height: 30px;
            top: 15%;
            left: -100px;
        }

        .cloud1::before {
            width: 40px;
            height: 40px;
            top: -20px;
            left: 8px;
        }

        .cloud2 {
            width: 60px;
            height: 25px;
            top: 8%;
            left: -80px;
            animation-delay: -10s;
        }

        .cloud2::before {
            width: 45px;
            height: 30px;
            top: -15px;
            right: 10px;
        }

        @keyframes float-cloud {
            0% { transform: translateX(0); }
            100% { transform: translateX(calc(100vw + 200px)); }
        }

        /* Stadium Lights */
        .stadium-lights {
            position: absolute;
            top: 3%;
            width: 100%;
            display: flex;
            justify-content: space-around;
            padding: 0 15%;
        }

        .light-pole {
            width: 6px;
            height: 60px;
            background: linear-gradient(180deg, #666, #333);
            border-radius: 3px;
            position: relative;
        }

        .light-head {
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 45px;
            height: 20px;
            background: linear-gradient(180deg, #888, #555);
            border-radius: 8px 8px 0 0;
        }

        .light-beam {
            position: absolute;
            top: 3px;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 40px;
            background: radial-gradient(ellipse, rgba(255,255,200,0.6) 0%, rgba(255,255,200,0.2) 40%, transparent 70%);
            animation: flicker 4s infinite;
        }

        @keyframes flicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
            75% { opacity: 0.9; }
        }

        /* Crowd */
        .crowd {
            position: absolute;
            bottom: 50%;
            left: 0;
            width: 100%;
            height: 40px;
            background: repeating-linear-gradient(90deg, #1a1a2e 0px, #16213e 4px, #1a1a2e 8px);
            opacity: 0.8;
        }

        .crowd::before {
            content: '👥👥👥👥👥👥👥👥👥👥';
            position: absolute;
            top: -8px;
            left: 0;
            font-size: 16px;
            letter-spacing: -4px;
            animation: crowd-wave 2.5s infinite ease-in-out;
            white-space: nowrap;
            width: 200%;
        }

        @keyframes crowd-wave {
            0%, 100% { transform: translateX(0) translateY(0); }
            25% { transform: translateX(-1%) translateY(-2px); }
            50% { transform: translateX(-2%) translateY(0); }
            75% { transform: translateX(-1%) translateY(-2px); }
        }

        /* Field */
        .field {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 50%;
            background: repeating-linear-gradient(0deg, var(--grass-green) 0px, var(--light-grass) 30px, var(--grass-green) 60px);
        }

        /* Field Lines */
        .field-lines {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 50%;
        }

        .center-circle {
            position: absolute;
            top: 5%;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 100px;
            border: 3px solid rgba(255,255,255,0.5);
            border-radius: 50%;
        }

        .center-dot {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 8px;
            height: 8px;
            background: rgba(255,255,255,0.7);
            border-radius: 50%;
        }

        .half-line {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 3px;
            height: 100%;
            background: rgba(255,255,255,0.5);
        }

        /* Container */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 10;
        }

        /* Header */
        header {
            text-align: center;
            padding: 30px 0;
            animation: slideDown 0.8s ease-out;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .logo-container {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 35px;
            border-radius: 50px;
            border: 3px solid var(--dark);
            box-shadow: 0 8px 0 rgba(0,0,0,0.2), 0 15px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .logo-container:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 12px 0 rgba(0,0,0,0.2), 0 20px 40px rgba(0,0,0,0.3);
        }

        .logo-ball {
            font-size: 45px;
            animation: spin-ball 4s linear infinite;
        }

        @keyframes spin-ball {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        h1 {
            font-family: 'Poppins', sans-serif;
            font-size: 2.2em;
            font-weight: 800;
            color: var(--dark);
            text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
        }

        .subtitle {
            font-size: 1em;
            color: #666;
            font-weight: 500;
        }

        /* Card */
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 35px;
            margin-bottom: 20px;
            border: 3px solid var(--dark);
            box-shadow: 0 8px 0 rgba(0,0,0,0.2), 0 15px 30px rgba(0,0,0,0.2);
            animation: slideUp 0.8s ease-out 0.2s both;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Match Selector */
        .match-selector {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 25px;
            align-items: end;
        }

        @media (max-width: 768px) {
            .match-selector {
                grid-template-columns: 1fr;
            }
            .vs-section {
                margin: 10px 0;
            }
        }

        .team-box {
            text-align: center;
        }

        .team-label {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-size: 1em;
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 10px;
        }

        .select-wrapper {
            position: relative;
        }

        select {
            width: 100%;
            padding: 16px 45px 16px 18px;
            font-family: 'Poppins', sans-serif;
            font-size: 1em;
            font-weight: 600;
            color: var(--dark);
            background: linear-gradient(180deg, #f8f9fa, #e9ecef);
            border: 3px solid var(--dark);
            border-radius: 15px;
            cursor: pointer;
            appearance: none;
            transition: all 0.3s;
            box-shadow: 0 4px 0 rgba(0,0,0,0.2);
        }

        select:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 0 rgba(0,0,0,0.2);
            border-color: var(--grass-green);
        }

        select:focus {
            outline: none;
            border-color: #4a7c43;
            box-shadow: 0 0 0 4px rgba(74, 124, 67, 0.2), 0 4px 0 rgba(0,0,0,0.2);
        }

        .select-arrow {
            position: absolute;
            right: 18px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 12px;
            pointer-events: none;
            color: var(--dark);
        }

        .vs-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }

        .vs-badge {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            font-size: 1.3em;
            font-weight: 800;
            padding: 12px 22px;
            border-radius: 50%;
            border: 3px solid var(--dark);
            box-shadow: 0 4px 0 rgba(0,0,0,0.2);
            animation: vs-pulse 1.5s ease-in-out infinite;
        }

        @keyframes vs-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.08); }
        }

        /* Predict Button */
        .predict-btn {
            width: 100%;
            margin-top: 25px;
            padding: 18px 40px;
            font-family: 'Poppins', sans-serif;
            font-size: 1.2em;
            font-weight: 700;
            color: var(--dark);
            background: linear-gradient(180deg, #FFD700, #FFA500);
            border: 3px solid var(--dark);
            border-radius: 50px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.1s;
            box-shadow: 0 6px 0 rgba(0,0,0,0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .predict-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 9px 0 rgba(0,0,0,0.2);
        }

        .predict-btn:active {
            transform: translateY(3px);
            box-shadow: 0 3px 0 rgba(0,0,0,0.2);
        }

        /* Loading with Football Buffer */
        .loading-container {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .loading-container.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .football-buffer {
            width: 100px;
            height: 100px;
            margin: 0 auto 25px;
            position: relative;
        }

        .buffer-ball {
            font-size: 80px;
            display: block;
            animation: buffer-spin 0.8s linear infinite;
            filter: drop-shadow(0 8px 10px rgba(0,0,0,0.3));
        }

        @keyframes buffer-spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .buffer-shadow {
            width: 60px;
            height: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 50%;
            margin: 15px auto 0;
        }

        .loading-text {
            font-size: 1.2em;
            font-weight: 600;
            color: var(--dark);
        }

        .loading-dots::after {
            content: '';
            animation: dots 1.5s infinite;
        }

        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60%, 100% { content: '...'; }
        }

        /* Results */
        .results-container {
            display: none;
        }

        .results-container.active {
            display: block;
            animation: resultPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        @keyframes resultPop {
            0% { opacity: 0; transform: scale(0.8) translateY(30px); }
            70% { transform: scale(1.02); }
            100% { opacity: 1; transform: scale(1) translateY(0); }
        }

        /* Confetti */
        .confetti-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 100;
            overflow: hidden;
        }

        .confetti {
            position: absolute;
            width: 10px;
            height: 10px;
            animation: confetti-fall 3s ease-out forwards;
        }

        @keyframes confetti-fall {
            0% { opacity: 1; transform: translateY(-100px) rotate(0deg); }
            100% { opacity: 0; transform: translateY(100vh) rotate(720deg); }
        }

        /* Winner Banner */
        .winner-banner {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            border-radius: 20px;
            border: 3px solid var(--dark);
            margin-bottom: 25px;
            box-shadow: 0 6px 0 rgba(0,0,0,0.2);
            animation: winner-glow 2s ease-in-out infinite;
        }

        @keyframes winner-glow {
            0%, 100% { box-shadow: 0 6px 0 rgba(0,0,0,0.2), 0 0 20px rgba(255, 215, 0, 0.4); }
            50% { box-shadow: 0 6px 0 rgba(0,0,0,0.2), 0 0 40px rgba(255, 215, 0, 0.6); }
        }

        .winner-text {
            font-size: 2em;
            font-weight: 800;
            color: var(--dark);
            margin-bottom: 10px;
        }

        .confidence-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 25px;
            background: var(--dark);
            color: white;
            border-radius: 50px;
            font-weight: 600;
        }

        /* Probability Bars */
        .prob-section {
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 1.1em;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .prob-bar-container {
            margin-bottom: 15px;
        }

        .prob-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            font-weight: 600;
        }

        .prob-name {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .prob-value {
            font-weight: 700;
            font-size: 1.1em;
        }

        .prob-track {
            height: 28px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            border: 2px solid var(--dark);
        }

        .prob-fill {
            height: 100%;
            border-radius: 13px;
            width: 0;
            transition: width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
        }

        .prob-fill.home {
            background: linear-gradient(90deg, #27ae60, #2ecc71);
        }

        .prob-fill.draw {
            background: linear-gradient(90deg, #95a5a6, #bdc3c7);
        }

        .prob-fill.away {
            background: linear-gradient(90deg, #e74c3c, #ff6b6b);
        }

        .mini-ball {
            font-size: 16px;
            animation: ball-roll 1.5s linear infinite;
        }

        @keyframes ball-roll {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        /* Expected Goals */
        .goals-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }

        @media (max-width: 600px) {
            .goals-section {
                grid-template-columns: 1fr;
            }
        }

        .goal-card {
            background: linear-gradient(180deg, #f8f9fa, #e9ecef);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            border: 3px solid var(--dark);
            box-shadow: 0 5px 0 rgba(0,0,0,0.2);
        }

        .goal-team {
            font-size: 0.95em;
            font-weight: 600;
            color: #666;
            margin-bottom: 10px;
        }

        .goal-number {
            font-size: 3.5em;
            font-weight: 800;
            color: #e74c3c;
            line-height: 1;
        }

        .goal-label {
            font-size: 0.9em;
            color: #888;
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
            background: linear-gradient(180deg, #fff, #f5f5f5);
            border-radius: 20px;
            padding: 25px;
            border: 3px solid var(--dark);
            box-shadow: 0 5px 0 rgba(0,0,0,0.2);
        }

        .stats-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 2px dashed #ddd;
        }

        .stats-icon {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            border: 2px solid var(--dark);
        }

        .stats-team {
            font-weight: 700;
            font-size: 1.1em;
            color: var(--dark);
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }

        .stat-row:last-child {
            border-bottom: none;
        }

        .stat-name {
            font-weight: 500;
            color: #666;
            font-size: 0.95em;
        }

        .stat-value {
            font-weight: 700;
            font-size: 1.05em;
            color: #667eea;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 20px;
            color: white;
            font-weight: 600;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        }

        footer span {
            color: #FFD700;
        }

        /* Intensity Meter */
        .intensity-section {
            margin-bottom: 25px;
        }

        .intensity-track {
            height: 35px;
            background: linear-gradient(90deg, #27ae60, #f1c40f, #e74c3c);
            border-radius: 18px;
            border: 3px solid var(--dark);
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);
        }

        .intensity-marker {
            position: absolute;
            top: -8px;
            width: 4px;
            height: 51px;
            background: var(--dark);
            border-radius: 2px;
            transition: left 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            left: 0;
        }

        .intensity-marker::after {
            content: '🔥';
            position: absolute;
            top: -28px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 22px;
            animation: fire-shake 0.5s ease-in-out infinite;
        }

        @keyframes fire-shake {
            0%, 100% { transform: translateX(-50%) rotate(-5deg); }
            50% { transform: translateX(-50%) rotate(5deg); }
        }

        .intensity-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 8px;
            font-size: 0.85em;
            font-weight: 600;
            color: var(--dark);
        }
    </style>
</head>
<body>
    <div class="stadium-bg">
        <div class="sky">
            <div class="cloud cloud1"></div>
            <div class="cloud cloud2"></div>
        </div>
        <div class="stadium-lights">
            <div class="light-pole"><div class="light-head"><div class="light-beam"></div></div></div>
            <div class="light-pole"><div class="light-head"><div class="light-beam"></div></div></div>
            <div class="light-pole"><div class="light-head"><div class="light-beam"></div></div></div>
            <div class="light-pole"><div class="light-head"><div class="light-beam"></div></div></div>
        </div>
        <div class="crowd"></div>
        <div class="field">
            <div class="field-lines">
                <div class="center-circle"><div class="center-dot"></div></div>
                <div class="half-line"></div>
            </div>
        </div>
    </div>

    <div class="confetti-container" id="confetti"></div>

    <div class="container">
        <header>
            <div class="logo-container">
                <span class="logo-ball">⚽</span>
                <div>
                    <h1>Match Predictor</h1>
                    <p class="subtitle">AI-Powered Football Analytics</p>
                </div>
            </div>
        </header>

        <div class="card">
            <div class="match-selector">
                <div class="team-box">
                    <div class="team-label">
                        <span>🏠</span> Home Team
                    </div>
                    <div class="select-wrapper">
                        <select id="homeTeam">
                            <option value="">Select Team</option>
                            {team_options}
                        </select>
                        <span class="select-arrow">▼</span>
                    </div>
                </div>

                <div class="vs-section">
                    <div class="vs-badge">VS</div>
                </div>

                <div class="team-box">
                    <div class="team-label">
                        <span>✈️</span> Away Team
                    </div>
                    <div class="select-wrapper">
                        <select id="awayTeam">
                            <option value="">Select Team</option>
                            {team_options}
                        </select>
                        <span class="select-arrow">▼</span>
                    </div>
                </div>
            </div>

            <button class="predict-btn" onclick="predictMatch()">
                🔮 Predict Match
            </button>

            <div class="loading-container" id="loading">
                <div class="football-buffer">
                    <span class="buffer-ball">⚽</span>
                    <div class="buffer-shadow"></div>
                </div>
                <p class="loading-text">Analyzing Match<span class="loading-dots"></span></p>
            </div>

            <div class="results-container" id="results"></div>
        </div>

        <footer>
            <p>⚡ Powered by <span>Machine Learning</span> & <span>Data Analytics</span> ⚡</p>
        </footer>
    </div>

    <script>
        // Create confetti
        function createConfetti() {
            const container = document.getElementById('confetti');
            container.innerHTML = '';
            const colors = ['#FFD700', '#FFA500', '#FF6B6B', '#4ECDC4', '#95E1D3', '#27ae60'];
            
            for (let i = 0; i < 50; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 0.5 + 's';
                confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
                container.appendChild(confetti);
            }

            setTimeout(() => {
                container.innerHTML = '';
            }, 3000);
        }

        // Animate number counting
        function animateNumber(element, target, duration = 1500, decimals = 1) {
            let start = 0;
            const increment = target / (duration / 16);
            const timer = setInterval(() => {
                start += increment;
                if (start >= target) {
                    element.textContent = target.toFixed(decimals);
                    clearInterval(timer);
                } else {
                    element.textContent = start.toFixed(decimals);
                }
            }, 16);
        }

        async function predictMatch() {
            const homeTeam = document.getElementById('homeTeam').value;
            const awayTeam = document.getElementById('awayTeam').value;

            if (!homeTeam || !awayTeam) {
                alert('⚠️ Please select both teams!');
                return;
            }

            if (homeTeam === awayTeam) {
                alert('⚠️ Please select two different teams!');
                return;
            }

            // Show loading with spinning football buffer
            document.getElementById('loading').classList.add('active');
            document.getElementById('results').classList.remove('active');

            try {
                const response = await fetch(`/predict?home=${encodeURIComponent(homeTeam)}&away=${encodeURIComponent(awayTeam)}`);
                const data = await response.json();

                setTimeout(() => {
                    displayResults(data);
                    document.getElementById('loading').classList.remove('active');
                    createConfetti();
                }, 2000);
            } catch (error) {
                alert('❌ Error making prediction. Please try again.');
                document.getElementById('loading').classList.remove('active');
            }
        }

        function displayResults(data) {
            const resultsDiv = document.getElementById('results');

            let winnerText = '';
            if (data.predicted_winner === 'Home Win') {
                winnerText = '🏆 ' + data.home_team + ' Wins!';
            } else if (data.predicted_winner === 'Away Win') {
                winnerText = '🏆 ' + data.away_team + ' Wins!';
            } else {
                winnerText = '🤝 Match Draw!';
            }

            // Calculate intensity
            const maxProb = Math.max(data.probabilities['Home Win'], data.probabilities['Away Win']);
            const intensity = Math.round(100 - maxProb + 20);

            resultsDiv.innerHTML = `
                <div class="winner-banner">
                    <div class="winner-text">${winnerText}</div>
                    <div class="confidence-pill">
                        <span>🎯</span>
                        <span>AI Confidence: <span id="confValue">0</span>%</span>
                    </div>
                </div>

                <div class="intensity-section">
                    <div class="section-title">
                        <span>🔥</span> Match Intensity Meter
                    </div>
                    <div class="intensity-track">
                        <div class="intensity-marker" id="intensityMarker"></div>
                    </div>
                    <div class="intensity-labels">
                        <span>Calm</span>
                        <span>Competitive</span>
                        <span>Intense</span>
                    </div>
                </div>

                <div class="prob-section">
                    <div class="section-title">
                        <span>📊</span> Win Probabilities
                    </div>

                    <div class="prob-bar-container">
                        <div class="prob-label">
                            <span class="prob-name">🏠 Home Win</span>
                            <span class="prob-value" id="homeProb">0%</span>
                        </div>
                        <div class="prob-track">
                            <div class="prob-fill home" id="homeBar">
                                <span class="mini-ball">⚽</span>
                            </div>
                        </div>
                    </div>

                    <div class="prob-bar-container">
                        <div class="prob-label">
                            <span class="prob-name">⚖️ Draw</span>
                            <span class="prob-value" id="drawProb">0%</span>
                        </div>
                        <div class="prob-track">
                            <div class="prob-fill draw" id="drawBar">
                                <span class="mini-ball">⚽</span>
                            </div>
                        </div>
                    </div>

                    <div class="prob-bar-container">
                        <div class="prob-label">
                            <span class="prob-name">✈️ Away Win</span>
                            <span class="prob-value" id="awayProb">0%</span>
                        </div>
                        <div class="prob-track">
                            <div class="prob-fill away" id="awayBar">
                                <span class="mini-ball">⚽</span>
                            </div>
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
                            <div class="stats-icon">🏠</div>
                            <span class="stats-team">${data.home_team}</span>
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
                            <span class="stat-name">Conceded</span>
                            <span class="stat-value">${data.home_stats.avg_conceded}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">Matches</span>
                            <span class="stat-value">${data.home_stats.matches}</span>
                        </div>
                    </div>
                    <div class="stats-card">
                        <div class="stats-header">
                            <div class="stats-icon">✈️</div>
                            <span class="stats-team">${data.away_team}</span>
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
                            <span class="stat-name">Conceded</span>
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

            // Animate everything
            setTimeout(() => {
                document.getElementById('intensityMarker').style.left = intensity + '%';

                document.getElementById('homeBar').style.width = data.probabilities['Home Win'] + '%';
                document.getElementById('drawBar').style.width = data.probabilities['Draw'] + '%';
                document.getElementById('awayBar').style.width = data.probabilities['Away Win'] + '%';

                animateNumber(document.getElementById('homeProb'), data.probabilities['Home Win'], 1500, 1);
                animateNumber(document.getElementById('drawProb'), data.probabilities['Draw'], 1500, 1);
                animateNumber(document.getElementById('awayProb'), data.probabilities['Away Win'], 1500, 1);

                animateNumber(document.getElementById('homeGoals'), data.expected_goals_home, 1500, 2);
                animateNumber(document.getElementById('awayGoals'), data.expected_goals_away, 1500, 2);
                animateNumber(document.getElementById('confValue'), data.confidence, 1500, 1);
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
        print(f"⚽ FOOTBALL MATCH PREDICTOR RUNNING!")
        print(f"{'='*60}")
        print(f"\n🌐 Open: http://localhost:{port}")
        print("🛑 Press Ctrl+C to stop\n")

        webbrowser.open(f'http://localhost:{port}')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped.")

if __name__ == "__main__":
    run_server()
