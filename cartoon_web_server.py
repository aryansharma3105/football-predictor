"""
Cartoon Style Football Match Predictor Web Server
Fun, animated, FIFA Street inspired theme
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
    <title>⚽ Football Match Predictor - Cartoon Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Comic+Neue:wght@400;700&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --grass-green: #2d5a27;
            --light-grass: #4a7c43;
            --sky-blue: #87CEEB;
            --bright-yellow: #FFD700;
            --orange: #FF8C00;
            --white: #ffffff;
            --dark: #1a1a1a;
            --card-bg: rgba(255, 255, 255, 0.95);
        }

        body {
            font-family: 'Fredoka', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
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

        /* Sky with clouds */
        .sky {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 40%;
            background: linear-gradient(180deg, #4FC3F7 0%, #87CEEB 100%);
        }

        .cloud {
            position: absolute;
            background: white;
            border-radius: 100px;
            opacity: 0.9;
            animation: float-cloud 20s infinite ease-in-out;
        }

        .cloud::before {
            content: '';
            position: absolute;
            background: white;
            border-radius: 100px;
        }

        .cloud1 {
            width: 100px;
            height: 40px;
            top: 20%;
            left: -100px;
        }

        .cloud1::before {
            width: 50px;
            height: 50px;
            top: -25px;
            left: 10px;
        }

        .cloud2 {
            width: 80px;
            height: 35px;
            top: 10%;
            left: -80px;
            animation-delay: -7s;
        }

        .cloud2::before {
            width: 60px;
            height: 40px;
            top: -20px;
            right: 15px;
        }

        @keyframes float-cloud {
            0% { transform: translateX(0); }
            100% { transform: translateX(calc(100vw + 200px)); }
        }

        /* Stadium Lights */
        .stadium-lights {
            position: absolute;
            top: 5%;
            width: 100%;
            display: flex;
            justify-content: space-around;
            padding: 0 10%;
        }

        .light-pole {
            width: 8px;
            height: 80px;
            background: linear-gradient(180deg, #666, #333);
            border-radius: 4px;
            position: relative;
        }

        .light-head {
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 25px;
            background: linear-gradient(180deg, #888, #555);
            border-radius: 10px 10px 0 0;
        }

        .light-beam {
            position: absolute;
            top: 5px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 50px;
            background: radial-gradient(ellipse, rgba(255,255,200,0.8) 0%, rgba(255,255,200,0.3) 40%, transparent 70%);
            animation: flicker 3s infinite;
        }

        @keyframes flicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
            75% { opacity: 0.9; }
        }

        /* Crowd Silhouettes */
        .crowd {
            position: absolute;
            bottom: 60%;
            left: 0;
            width: 100%;
            height: 60px;
            background: repeating-linear-gradient(
                90deg,
                #1a1a2e 0px,
                #16213e 5px,
                #1a1a2e 10px
            );
            opacity: 0.8;
        }

        .crowd::before {
            content: '👥👥👥👥👥👥👥👥👥👥';
            position: absolute;
            top: -10px;
            left: 0;
            font-size: 20px;
            letter-spacing: -5px;
            animation: crowd-wave 2s infinite ease-in-out;
            white-space: nowrap;
            width: 200%;
        }

        @keyframes crowd-wave {
            0%, 100% { transform: translateX(0) translateY(0); }
            25% { transform: translateX(-2%) translateY(-3px); }
            50% { transform: translateX(-4%) translateY(0); }
            75% { transform: translateX(-2%) translateY(-3px); }
        }

        /* Grass Field */
        .field {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 60%;
            background: 
                repeating-linear-gradient(
                    0deg,
                    var(--grass-green) 0px,
                    var(--light-grass) 40px,
                    var(--grass-green) 80px
                );
        }

        /* Field Lines */
        .field-lines {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 60%;
        }

        .center-circle {
            position: absolute;
            top: 10%;
            left: 50%;
            transform: translateX(-50%);
            width: 150px;
            height: 150px;
            border: 4px solid rgba(255,255,255,0.6);
            border-radius: 50%;
        }

        .center-dot {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 10px;
            height: 10px;
            background: rgba(255,255,255,0.8);
            border-radius: 50%;
        }

        .half-line {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 4px;
            height: 100%;
            background: rgba(255,255,255,0.6);
        }

        /* Floating Footballs */
        .floating-balls {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .float-ball {
            position: absolute;
            font-size: 30px;
            animation: float-ball 15s infinite ease-in-out;
            opacity: 0.6;
        }

        @keyframes float-ball {
            0%, 100% { 
                transform: translateY(0) rotate(0deg);
                opacity: 0;
            }
            10% { opacity: 0.6; }
            90% { opacity: 0.6; }
            100% { 
                transform: translateY(-100vh) rotate(720deg);
                opacity: 0;
            }
        }

        /* Container */
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 10;
        }

        /* Header */
        header {
            text-align: center;
            padding: 20px 0;
            animation: bounce-in 1s ease-out;
        }

        @keyframes bounce-in {
            0% { opacity: 0; transform: scale(0.3) translateY(-50px); }
            50% { transform: scale(1.05) translateY(0); }
            70% { transform: scale(0.95); }
            100% { opacity: 1; transform: scale(1); }
        }

        .logo-container {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            background: var(--card-bg);
            padding: 15px 30px;
            border-radius: 50px;
            border: 4px solid var(--dark);
            box-shadow: 
                0 8px 0 rgba(0,0,0,0.2),
                0 15px 20px rgba(0,0,0,0.2);
            animation: wobble 2s ease-in-out infinite;
        }

        @keyframes wobble {
            0%, 100% { transform: rotate(-2deg); }
            50% { transform: rotate(2deg); }
        }

        .logo-ball {
            font-size: 50px;
            animation: spin-ball 3s linear infinite;
        }

        @keyframes spin-ball {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        h1 {
            font-family: 'Fredoka', sans-serif;
            font-size: 2.5em;
            font-weight: 700;
            color: var(--dark);
            text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
        }

        .subtitle {
            font-family: 'Comic Neue', cursive;
            font-size: 1.2em;
            color: var(--orange);
            font-weight: 700;
        }

        /* Comic Card */
        .comic-card {
            background: var(--card-bg);
            border-radius: 30px;
            padding: 30px;
            margin-bottom: 20px;
            border: 4px solid var(--dark);
            box-shadow: 
                0 8px 0 rgba(0,0,0,0.2),
                0 15px 30px rgba(0,0,0,0.2);
            position: relative;
            animation: slide-up-bounce 0.8s ease-out 0.2s both;
        }

        @keyframes slide-up-bounce {
            0% { opacity: 0; transform: translateY(50px); }
            60% { transform: translateY(-10px); }
            80% { transform: translateY(5px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .comic-card::before {
            content: '';
            position: absolute;
            top: -4px;
            left: -4px;
            right: -4px;
            bottom: -4px;
            background: linear-gradient(45deg, var(--bright-yellow), var(--orange), var(--bright-yellow));
            border-radius: 34px;
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .comic-card:hover::before {
            opacity: 1;
        }

        /* Match Selector */
        .match-selector {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 20px;
            align-items: end;
        }

        @media (max-width: 768px) {
            .match-selector {
                grid-template-columns: 1fr;
            }
            .vs-section {
                transform: rotate(90deg);
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
            gap: 10px;
            font-family: 'Fredoka', sans-serif;
            font-size: 1.2em;
            font-weight: 700;
            color: #fff;
            margin-bottom: 12px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            letter-spacing: 1px;
        }

        .select-wrapper {
            position: relative;
        }

        select {
            width: 100%;
            padding: 18px 50px 18px 20px;
            font-family: 'Fredoka', sans-serif;
            font-size: 1.1em;
            font-weight: 600;
            color: #fff;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            cursor: pointer;
            appearance: none;
            transition: all 0.3s;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }

        select:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            border-color: rgba(255,255,255,0.6);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        select:focus {
            outline: none;
            border-color: #fff;
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.2), 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        select option {
            background: #764ba2;
            color: #fff;
            padding: 10px;
        }

        .select-arrow {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 12px;
            pointer-events: none;
        }

        .vs-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }

        .vs-badge {
            background: linear-gradient(135deg, #f093fb, #f5576c);
            color: white;
            font-family: 'Fredoka', sans-serif;
            font-size: 1.5em;
            font-weight: 800;
            padding: 15px 25px;
            border-radius: 50%;
            border: 3px solid rgba(255,255,255,0.5);
            box-shadow: 0 6px 20px rgba(240, 147, 251, 0.4);
            animation: vs-pulse 1.5s ease-in-out infinite;
        }

        @keyframes vs-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        /* Predict Button */
        .predict-btn {
            width: 100%;
            margin-top: 25px;
            padding: 18px 40px;
            font-family: 'Fredoka', sans-serif;
            font-size: 1.3em;
            font-weight: 700;
            color: var(--dark);
            background: linear-gradient(180deg, var(--bright-yellow), #ffb700);
            border: 4px solid var(--dark);
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

        .predict-btn::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255,255,255,0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .predict-btn:active::after {
            width: 300px;
            height: 300px;
        }

        /* Loading Animation */
        .loading-container {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .loading-container.active {
            display: block;
            animation: fade-in 0.3s ease;
        }

        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .football-loader {
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            position: relative;
        }

        .football {
            font-size: 80px;
            display: block;
            animation: football-bounce 0.6s ease-in-out infinite;
            filter: drop-shadow(0 10px 10px rgba(0,0,0,0.3));
        }

        @keyframes football-bounce {
            0%, 100% { 
                transform: translateY(0) rotate(0deg);
                animation-timing-function: ease-out;
            }
            50% { 
                transform: translateY(-30px) rotate(180deg);
                animation-timing-function: ease-in;
            }
        }

        .football-shadow {
            width: 60px;
            height: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 50%;
            margin: 10px auto 0;
            animation: shadow-scale 0.6s ease-in-out infinite;
        }

        @keyframes shadow-scale {
            0%, 100% { transform: scale(1); opacity: 0.3; }
            50% { transform: scale(0.6); opacity: 0.1; }
        }

        .loading-text {
            font-family: 'Comic Neue', cursive;
            font-size: 1.3em;
            font-weight: 700;
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

        /* Results Container */
        .results-container {
            display: none;
        }

        .results-container.active {
            display: block;
            animation: goal-celebration 0.8s ease-out;
        }

        @keyframes goal-celebration {
            0% { 
                opacity: 0; 
                transform: scale(0.5) rotate(-10deg);
            }
            50% {
                transform: scale(1.1) rotate(5deg);
            }
            70% {
                transform: scale(0.95) rotate(-2deg);
            }
            100% { 
                opacity: 1; 
                transform: scale(1) rotate(0);
            }
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
            0% {
                opacity: 1;
                transform: translateY(-100px) rotate(0deg);
            }
            100% {
                opacity: 0;
                transform: translateY(100vh) rotate(720deg);
            }
        }

        /* Winner Banner */
        .winner-banner {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, var(--bright-yellow), #ffcc00);
            border-radius: 25px;
            border: 4px solid var(--dark);
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 0 rgba(0,0,0,0.2);
        }

        .goal-text {
            font-family: 'Fredoka', sans-serif;
            font-size: 3em;
            font-weight: 800;
            color: var(--dark);
            text-shadow: 3px 3px 0 rgba(0,0,0,0.1);
            animation: goal-pop 0.5s ease-out;
            margin-bottom: 10px;
        }

        @keyframes goal-pop {
            0% { transform: scale(0); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1); }
        }

        .winner-name {
            font-family: 'Fredoka', sans-serif;
            font-size: 1.8em;
            font-weight: 700;
            color: var(--dark);
        }

        .confidence-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
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
            font-family: 'Comic Neue', cursive;
            font-size: 1.2em;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .energy-bar-container {
            margin-bottom: 15px;
        }

        .energy-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .energy-name {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .energy-value {
            font-family: 'Fredoka', sans-serif;
            font-size: 1.2em;
            font-weight: 700;
        }

        .energy-track {
            height: 35px;
            background: #e0e0e0;
            border-radius: 20px;
            overflow: hidden;
            border: 3px solid var(--dark);
            position: relative;
        }

        .energy-fill {
            height: 100%;
            border-radius: 17px;
            width: 0;
            transition: width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
        }

        .energy-fill.home {
            background: linear-gradient(90deg, #27ae60, #2ecc71);
        }

        .energy-fill.draw {
            background: linear-gradient(90deg, #95a5a6, #bdc3c7);
        }

        .energy-fill.away {
            background: linear-gradient(90deg, #e74c3c, #ff6b6b);
        }

        .mini-ball {
            font-size: 20px;
            animation: ball-roll 2s linear infinite;
        }

        @keyframes ball-roll {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
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
            border-radius: 25px;
            padding: 25px;
            text-align: center;
            border: 4px solid var(--dark);
            box-shadow: 0 6px 0 rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }

        .goal-card::before {
            content: '⚽';
            position: absolute;
            top: -20px;
            right: -20px;
            font-size: 80px;
            opacity: 0.1;
        }

        .goal-team-name {
            font-family: 'Comic Neue', cursive;
            font-size: 1em;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 10px;
        }

        .goal-number {
            font-family: 'Fredoka', sans-serif;
            font-size: 4em;
            font-weight: 800;
            color: var(--orange);
            line-height: 1;
            text-shadow: 3px 3px 0 rgba(0,0,0,0.1);
        }

        .goal-label {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
            font-weight: 600;
        }

        /* Wave Animation */
        .wave-container {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 20px;
            overflow: hidden;
        }

        .wave {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 200%;
            height: 100%;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23ffffff' fill-opacity='0.3' d='M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
            background-size: 50% 100%;
            animation: wave-move 3s linear infinite;
        }

        @keyframes wave-move {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
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
            background: linear-gradient(180deg, #fff, #f0f0f0);
            border-radius: 25px;
            padding: 25px;
            border: 4px solid var(--dark);
            box-shadow: 0 6px 0 rgba(0,0,0,0.2);
        }

        .stats-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px dashed #ddd;
        }

        .stats-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--orange), #ff6b35);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 25px;
            border: 3px solid var(--dark);
        }

        .stats-team-title {
            font-family: 'Fredoka', sans-serif;
            font-weight: 700;
            font-size: 1.2em;
            color: var(--dark);
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 2px dashed #eee;
        }

        .stat-row:last-child {
            border-bottom: none;
        }

        .stat-name {
            font-weight: 600;
            color: #666;
        }

        .stat-value {
            font-family: 'Fredoka', sans-serif;
            font-weight: 700;
            font-size: 1.1em;
            color: var(--orange);
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 20px;
            color: white;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }

        footer span {
            color: var(--bright-yellow);
        }

        /* Intensity Meter */
        .intensity-section {
            margin-bottom: 25px;
        }

        .intensity-track {
            height: 40px;
            background: linear-gradient(90deg, #27ae60, #f1c40f, #e74c3c);
            border-radius: 20px;
            border: 4px solid var(--dark);
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 3px 10px rgba(0,0,0,0.2);
        }

        .intensity-marker {
            position: absolute;
            top: -10px;
            width: 4px;
            height: 60px;
            background: var(--dark);
            border-radius: 2px;
            transition: left 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            left: 0;
        }

        .intensity-marker::after {
            content: '🔥';
            position: absolute;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 25px;
            animation: fire-shake 0.5s ease-in-out infinite;
        }

        @keyframes fire-shake {
            0%, 100% { transform: translateX(-50%) rotate(-5deg); }
            50% { transform: translateX(-50%) rotate(5deg); }
        }

        .intensity-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            font-size: 0.85em;
            font-weight: 700;
            color: var(--dark);
        }

        /* Tooltip */
        .tooltip {
            position: relative;
            cursor: help;
        }

        .tooltip::after {
            content: attr(data-tip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            padding: 10px 15px;
            background: var(--dark);
            color: white;
            border-radius: 15px;
            font-size: 0.85em;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: all 0.3s;
            font-family: 'Comic Neue', cursive;
        }

        .tooltip::before {
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 8px solid transparent;
            border-top-color: var(--dark);
            opacity: 0;
            transition: all 0.3s;
            margin-bottom: -8px;
        }

        .tooltip:hover::after,
        .tooltip:hover::before {
            opacity: 1;
            bottom: calc(100% + 10px);
        }
    </style>
</head>
<body>
    <div class="bg-pattern"></div>

    <div class="floating-balls" id="floatingBalls"></div>
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

        <div class="comic-card">
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
                🔮 Predict Match!
            </button>

            <div class="loading-container" id="loading">
                <div class="football-loader">
                    <span class="football">⚽</span>
                    <div class="football-shadow"></div>
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
        // Create floating footballs
        function createFloatingBalls() {
            const container = document.getElementById('floatingBalls');
            for (let i = 0; i < 8; i++) {
                const ball = document.createElement('div');
                ball.className = 'float-ball';
                ball.textContent = '⚽';
                ball.style.left = Math.random() * 100 + '%';
                ball.style.animationDelay = Math.random() * 15 + 's';
                ball.style.animationDuration = (12 + Math.random() * 8) + 's';
                container.appendChild(ball);
            }
        }
        createFloatingBalls();

        // Create confetti
        function createConfetti() {
            const container = document.getElementById('confetti');
            container.innerHTML = '';
            const colors = ['#FFD700', '#FF8C00', '#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181'];
            
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

            // Show loading
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
                winnerText = data.home_team + ' Wins! 🏆';
            } else if (data.predicted_winner === 'Away Win') {
                winnerText = data.away_team + ' Wins! 🏆';
            } else {
                winnerText = 'It\'s a Draw! 🤝';
            }

            // Calculate intensity
            const maxProb = Math.max(data.probabilities['Home Win'], data.probabilities['Away Win']);
            const intensity = Math.round(100 - maxProb + 20);

            resultsDiv.innerHTML = `
                <div class="winner-banner">
                    <div class="goal-text">GOAL!!!</div>
                    <div class="winner-name">${winnerText}</div>
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
                        <span>😴 Friendly</span>
                        <span>⚡ Competitive</span>
                        <span>🔥 INTENSE!</span>
                    </div>
                </div>

                <div class="prob-section">
                    <div class="section-title">
                        <span>📊</span> Win Probabilities
                    </div>

                    <div class="energy-bar-container">
                        <div class="energy-label">
                            <span class="energy-name">🏠 Home Win</span>
                            <span class="energy-value" id="homeProb">0%</span>
                        </div>
                        <div class="energy-track">
                            <div class="energy-fill home" id="homeBar">
                                <span class="mini-ball">⚽</span>
                            </div>
                        </div>
                    </div>

                    <div class="energy-bar-container">
                        <div class="energy-label">
                            <span class="energy-name">⚖️ Draw</span>
                            <span class="energy-value" id="drawProb">0%</span>
                        </div>
                        <div class="energy-track">
                            <div class="energy-fill draw" id="drawBar">
                                <span class="mini-ball">⚽</span>
                            </div>
                        </div>
                    </div>

                    <div class="energy-bar-container">
                        <div class="energy-label">
                            <span class="energy-name">✈️ Away Win</span>
                            <span class="energy-value" id="awayProb">0%</span>
                        </div>
                        <div class="energy-track">
                            <div class="energy-fill away" id="awayBar">
                                <span class="mini-ball">⚽</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="goals-section">
                    <div class="goal-card">
                        <div class="goal-team-name">${data.home_team}</div>
                        <div class="goal-number" id="homeGoals">0</div>
                        <div class="goal-label">Expected Goals ⚽</div>
                        <div class="wave-container"><div class="wave"></div></div>
                    </div>
                    <div class="goal-card">
                        <div class="goal-team-name">${data.away_team}</div>
                        <div class="goal-number" id="awayGoals">0</div>
                        <div class="goal-label">Expected Goals ⚽</div>
                        <div class="wave-container"><div class="wave"></div></div>
                    </div>
                </div>

                <div class="section-title">
                    <span>📈</span> Team Statistics
                </div>
                <div class="stats-section">
                    <div class="stats-card">
                        <div class="stats-header">
                            <div class="stats-icon">🏠</div>
                            <span class="stats-team-title">${data.home_team}</span>
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
                            <span class="stats-team-title">${data.away_team}</span>
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
        print(f"🎮 CARTOON FOOTBALL PREDICTOR RUNNING!")
        print(f"{'='*60}")
        print(f"\n⚽ Open: http://localhost:{port}")
        print("🛑 Press Ctrl+C to stop\n")

        webbrowser.open(f'http://localhost:{port}')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped.")

if __name__ == "__main__":
    run_server()
