"""
Final Cartoon Football Stadium Match Predictor
Moving balls + Improved team selection colors
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
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --sky-top: #4FC3F7;
            --sky-bottom: #81D4FA;
            --grass-light: #66BB6A;
            --grass-dark: #43A047;
            --stadium-wall: #5D4037;
            --stadium-roof: #8D6E63;
            --white: #ffffff;
            --black: #1a1a1a;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Nunito', sans-serif;
            background: linear-gradient(180deg, var(--sky-top) 0%, var(--sky-bottom) 35%, var(--grass-light) 35%, var(--grass-dark) 100%);
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
            height: 35%;
            background: linear-gradient(180deg, #29B6F6 0%, #81D4FA 60%, #B3E5FC 100%);
        }

        /* Cartoon Clouds */
        .cloud {
            position: absolute;
            background: white;
            border-radius: 100px;
            border: 3px solid #333;
            opacity: 0.95;
            animation: cloud-float 30s infinite linear;
        }

        .cloud::before,
        .cloud::after {
            content: '';
            position: absolute;
            background: white;
            border-radius: 100px;
            border: 3px solid #333;
        }

        .cloud::before {
            border-bottom: none;
            border-right: none;
        }

        .cloud::after {
            border-bottom: none;
            border-left: none;
        }

        .cloud1 {
            width: 100px;
            height: 40px;
            top: 8%;
            left: -150px;
        }

        .cloud1::before {
            width: 50px;
            height: 50px;
            top: -28px;
            left: 10px;
        }

        .cloud1::after {
            width: 40px;
            height: 40px;
            top: -20px;
            right: 15px;
        }

        .cloud2 {
            width: 80px;
            height: 35px;
            top: 18%;
            left: -120px;
            animation-delay: -12s;
        }

        .cloud2::before {
            width: 45px;
            height: 45px;
            top: -25px;
            left: 8px;
        }

        .cloud2::after {
            width: 35px;
            height: 35px;
            top: -18px;
            right: 12px;
        }

        .cloud3 {
            width: 90px;
            height: 38px;
            top: 5%;
            left: -130px;
            animation-delay: -22s;
        }

        .cloud3::before {
            width: 48px;
            height: 48px;
            top: -26px;
            left: 12px;
        }

        @keyframes cloud-float {
            0% { transform: translateX(0); }
            100% { transform: translateX(calc(100vw + 200px)); }
        }

        /* Cartoon Stadium Stands */
        .stadium-stands {
            position: absolute;
            bottom: 65%;
            left: 0;
            width: 100%;
            height: 80px;
            background: repeating-linear-gradient(
                90deg,
                var(--stadium-wall) 0px,
                #6D4C41 8px,
                var(--stadium-wall) 16px
            );
            border-top: 4px solid #3E2723;
            border-bottom: 4px solid #3E2723;
        }

        .stadium-stands::before {
            content: '';
            position: absolute;
            top: -25px;
            left: 0;
            width: 100%;
            height: 25px;
            background: var(--stadium-roof);
            border-radius: 50% 50% 0 0;
            border: 4px solid #3E2723;
        }

        /* Stadium Lights - Cartoon Style */
        .stadium-lights {
            position: absolute;
            top: 2%;
            width: 100%;
            display: flex;
            justify-content: space-around;
            padding: 0 10%;
        }

        .light-tower {
            position: relative;
            width: 60px;
            height: 100px;
        }

        .tower-pole {
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 8px;
            height: 70px;
            background: linear-gradient(90deg, #666, #888, #666);
            border: 2px solid #333;
            border-radius: 4px;
        }

        .tower-base {
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 15px;
            background: #555;
            border: 2px solid #333;
            border-radius: 4px;
        }

        .light-box {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 35px;
            background: #EEE;
            border: 3px solid #333;
            border-radius: 8px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            gap: 3px;
            padding: 3px;
        }

        .bulb {
            width: 10px;
            height: 10px;
            background: #FFF9C4;
            border: 1px solid #333;
            border-radius: 50%;
            animation: bulb-flash 2s infinite;
        }

        .bulb:nth-child(2n) {
            animation-delay: 0.3s;
        }

        .bulb:nth-child(3n) {
            animation-delay: 0.6s;
        }

        @keyframes bulb-flash {
            0%, 100% { background: #FFF9C4; box-shadow: 0 0 10px #FFF176; }
            50% { background: #FFF176; box-shadow: 0 0 20px #FFEE58; }
        }

        /* Cartoon Field */
        .field {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 65%;
            background: repeating-linear-gradient(
                0deg,
                var(--grass-dark) 0px,
                var(--grass-light) 25px,
                var(--grass-dark) 50px
            );
        }

        /* Field Markings */
        .field-lines {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 65%;
        }

        .center-circle {
            position: absolute;
            top: 5%;
            left: 50%;
            transform: translateX(-50%);
            width: 120px;
            height: 120px;
            border: 4px solid rgba(255,255,255,0.8);
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
        }

        .center-spot {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 12px;
            height: 12px;
            background: white;
            border: 2px solid #333;
            border-radius: 50%;
        }

        .halfway-line {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 4px;
            height: 100%;
            background: rgba(255,255,255,0.8);
        }

        .penalty-box-top {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 80px;
            border: 4px solid rgba(255,255,255,0.8);
            border-top: none;
            background: rgba(255,255,255,0.05);
        }

        /* Moving Draggable Footballs - Behind content */
        .floating-balls {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 5;
            pointer-events: none;
        }

        .float-football {
            position: absolute;
            width: 50px;
            height: 50px;
            cursor: grab;
            pointer-events: auto;
            transition: transform 0.1s;
            user-select: none;
            touch-action: none;
        }

        .float-football:active {
            cursor: grabbing;
        }

        .float-football.dragging {
            z-index: 10000;
            transform: scale(1.3) !important;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.4));
        }

        .float-football svg {
            width: 100%;
            height: 100%;
            filter: drop-shadow(3px 3px 0 rgba(0,0,0,0.2));
            pointer-events: none;
        }

        .float-football:hover svg {
            filter: drop-shadow(5px 5px 0 rgba(0,0,0,0.3));
        }

        /* Container */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 100;
        }

        /* Header */
        header {
            text-align: center;
            padding: 30px 0;
            animation: bounce-in 1s ease-out;
        }

        @keyframes bounce-in {
            0% { opacity: 0; transform: scale(0.3) translateY(-50px); }
            50% { transform: scale(1.05); }
            70% { transform: scale(0.95); }
            100% { opacity: 1; transform: scale(1); }
        }

        .logo-container {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            background: white;
            padding: 15px 35px;
            border-radius: 50px;
            border: 4px solid var(--black);
            box-shadow: 6px 6px 0 rgba(0,0,0,0.2), 0 15px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .logo-container:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 8px 8px 0 rgba(0,0,0,0.2), 0 20px 40px rgba(0,0,0,0.3);
        }

        .logo-football {
            width: 55px;
            height: 55px;
            animation: spin-slow 4s linear infinite;
        }

        @keyframes spin-slow {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        h1 {
            font-family: 'Fredoka One', cursive;
            font-size: 2.2em;
            color: var(--black);
            text-shadow: 3px 3px 0 rgba(0,0,0,0.1);
            letter-spacing: 1px;
        }

        .subtitle {
            font-size: 1em;
            color: #666;
            font-weight: 600;
        }

        /* Scroll Animation Base */
        .scroll-animate {
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .scroll-animate.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .scroll-animate.left {
            transform: translateX(-50px);
        }

        .scroll-animate.left.visible {
            transform: translateX(0);
        }

        .scroll-animate.right {
            transform: translateX(50px);
        }

        .scroll-animate.right.visible {
            transform: translateX(0);
        }

        .scroll-animate.scale {
            transform: scale(0.8);
        }

        .scroll-animate.scale.visible {
            transform: scale(1);
        }

        /* Card */
        .card {
            background: white;
            border-radius: 30px;
            padding: 35px;
            margin-bottom: 20px;
            border: 4px solid var(--black);
            box-shadow: 8px 8px 0 rgba(0,0,0,0.15), 0 15px 30px rgba(0,0,0,0.2);
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
        }

        .team-box {
            text-align: center;
        }

        .team-label {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-family: 'Fredoka One', cursive;
            font-size: 1.2em;
            color: var(--black);
            margin-bottom: 12px;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
        }

        .select-wrapper {
            position: relative;
        }

        /* IMPROVED TEAM SELECTION - Vibrant Colors */
        select {
            width: 100%;
            padding: 22px 55px 22px 25px;
            font-family: 'Fredoka One', cursive;
            font-size: 1.2em;
            color: white;
            background: linear-gradient(135deg, #FF6B6B 0%, #EE5A5A 50%, #E53935 100%);
            border: 4px solid var(--black);
            border-radius: 20px;
            cursor: pointer;
            appearance: none;
            transition: all 0.3s;
            box-shadow: 
                6px 6px 0 rgba(0,0,0,0.2),
                inset 0 -4px 0 rgba(0,0,0,0.2),
                inset 0 4px 0 rgba(255,255,255,0.3);
            text-shadow: 2px 2px 0 rgba(0,0,0,0.2);
        }

        select:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 
                10px 10px 0 rgba(0,0,0,0.2),
                inset 0 -4px 0 rgba(0,0,0,0.2),
                inset 0 4px 0 rgba(255,255,255,0.3);
            background: linear-gradient(135deg, #FF8A80 0%, #FF6B6B 50%, #F44336 100%);
            border-color: #B71C1C;
        }

        select:focus {
            outline: none;
            border-color: #FFD700;
            box-shadow: 
                0 0 0 6px rgba(255, 215, 0, 0.4),
                6px 6px 0 rgba(0,0,0,0.2),
                inset 0 -4px 0 rgba(0,0,0,0.2),
                inset 0 4px 0 rgba(255,255,255,0.3);
        }

        select option {
            font-family: 'Nunito', sans-serif;
            font-weight: 700;
            background: #C62828;
            color: white;
            padding: 15px;
            border-bottom: 2px solid #B71C1C;
        }

        .select-arrow {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 14px;
            pointer-events: none;
            color: white;
            text-shadow: 1px 1px 0 rgba(0,0,0,0.3);
        }

        .vs-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }

        .vs-badge {
            background: linear-gradient(135deg, #9C27B0, #7B1FA2);
            color: white;
            font-family: 'Fredoka One', cursive;
            font-size: 1.4em;
            padding: 15px 25px;
            border-radius: 50%;
            border: 4px solid var(--black);
            box-shadow: 5px 5px 0 rgba(0,0,0,0.2);
            animation: vs-bounce 1s ease-in-out infinite;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.3);
        }

        @keyframes vs-bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        /* Predict Button - Yellow */
        .predict-btn {
            width: 100%;
            margin-top: 30px;
            padding: 20px 40px;
            font-family: 'Fredoka One', cursive;
            font-size: 1.3em;
            color: var(--black);
            background: linear-gradient(180deg, #FFEB3B, #FBC02D);
            border: 4px solid var(--black);
            border-radius: 20px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.1s;
            box-shadow: 6px 6px 0 rgba(0,0,0,0.2);
            text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
        }

        .predict-btn:hover {
            transform: translateY(-4px);
            box-shadow: 9px 9px 0 rgba(0,0,0,0.2);
            background: linear-gradient(180deg, #FFF176, #FDD835);
        }

        .predict-btn:active {
            transform: translateY(2px);
            box-shadow: 3px 3px 0 rgba(0,0,0,0.2);
        }

        /* Loading with Classic Football Buffer */
        .loading-container {
            display: none;
            text-align: center;
            padding: 50px 20px;
        }

        .loading-container.active {
            display: block;
            animation: fade-in 0.3s ease;
        }

        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .football-buffer {
            width: 120px;
            height: 120px;
            margin: 0 auto 25px;
            position: relative;
        }

        .buffer-football {
            width: 100%;
            height: 100%;
            animation: buffer-spin 0.6s linear infinite;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.3));
        }

        @keyframes buffer-spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .buffer-shadow {
            width: 80px;
            height: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 50%;
            margin: 15px auto 0;
            animation: shadow-pulse 0.6s ease-in-out infinite;
        }

        @keyframes shadow-pulse {
            0%, 100% { transform: scale(1); opacity: 0.3; }
            50% { transform: scale(0.7); opacity: 0.15; }
        }

        .loading-text {
            font-family: 'Fredoka One', cursive;
            font-size: 1.4em;
            color: var(--black);
            text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
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
            width: 12px;
            height: 12px;
            animation: confetti-fall 3s ease-out forwards;
        }

        @keyframes confetti-fall {
            0% { opacity: 1; transform: translateY(-100px) rotate(0deg); }
            100% { opacity: 0; transform: translateY(100vh) rotate(720deg); }
        }

        /* Winner Banner */
        .winner-banner {
            text-align: center;
            padding: 35px;
            background: linear-gradient(135deg, #FFD700, #FFA000);
            border-radius: 25px;
            border: 4px solid var(--black);
            margin-bottom: 25px;
            box-shadow: 6px 6px 0 rgba(0,0,0,0.2);
            animation: winner-pop 0.6s ease-out, winner-glow 2s ease-in-out infinite;
        }

        @keyframes winner-pop {
            0% { transform: scale(0) rotate(-10deg); }
            50% { transform: scale(1.1) rotate(5deg); }
            100% { transform: scale(1) rotate(0); }
        }

        @keyframes winner-glow {
            0%, 100% { box-shadow: 6px 6px 0 rgba(0,0,0,0.2), 0 0 20px rgba(255, 215, 0, 0.5); }
            50% { box-shadow: 6px 6px 0 rgba(0,0,0,0.2), 0 0 40px rgba(255, 215, 0, 0.8); }
        }

        .winner-text {
            font-family: 'Fredoka One', cursive;
            font-size: 2em;
            color: var(--black);
            margin-bottom: 10px;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
        }

        .confidence-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 28px;
            background: var(--black);
            color: white;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1.1em;
        }

        /* Section Titles */
        .section-title {
            font-family: 'Fredoka One', cursive;
            font-size: 1.3em;
            color: var(--black);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
        }

        /* Probability Bars */
        .prob-section {
            margin-bottom: 25px;
        }

        .prob-bar-container {
            margin-bottom: 18px;
        }

        .prob-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            font-weight: 700;
            font-size: 1.05em;
        }

        .prob-name {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .prob-value {
            font-family: 'Fredoka One', cursive;
            font-size: 1.2em;
        }

        .prob-track {
            height: 35px;
            background: #e0e0e0;
            border-radius: 20px;
            overflow: hidden;
            border: 3px solid var(--black);
            box-shadow: inset 0 3px 8px rgba(0,0,0,0.2);
        }

        .prob-fill {
            height: 100%;
            border-radius: 17px;
            width: 0;
            transition: width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 12px;
            position: relative;
        }

        .prob-fill.home {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
        }

        .prob-fill.draw {
            background: linear-gradient(90deg, #9E9E9E, #BDBDBD);
        }

        .prob-fill.away {
            background: linear-gradient(90deg, #F44336, #FF5722);
        }

        .mini-football {
            width: 25px;
            height: 25px;
            animation: mini-roll 1s linear infinite;
        }

        @keyframes mini-roll {
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
            background: linear-gradient(180deg, #E3F2FD, #BBDEFB);
            border-radius: 25px;
            padding: 30px;
            text-align: center;
            border: 4px solid var(--black);
            box-shadow: 6px 6px 0 rgba(0,0,0,0.15);
            position: relative;
            overflow: hidden;
        }

        .goal-card::before {
            content: '';
            position: absolute;
            top: -30px;
            right: -30px;
            width: 100px;
            height: 100px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="white" stroke="black" stroke-width="3"/><path d="M50 5 L50 20 M50 80 L50 95 M5 50 L20 50 M80 50 L95 50" stroke="black" stroke-width="3"/></svg>');
            opacity: 0.1;
        }

        .goal-team {
            font-family: 'Fredoka One', cursive;
            font-size: 1em;
            color: #555;
            margin-bottom: 10px;
        }

        .goal-number {
            font-family: 'Fredoka One', cursive;
            font-size: 4em;
            color: #1976D2;
            line-height: 1;
            text-shadow: 3px 3px 0 rgba(0,0,0,0.1);
        }

        .goal-label {
            font-size: 0.95em;
            color: #666;
            margin-top: 8px;
            font-weight: 700;
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
            background: white;
            border-radius: 25px;
            padding: 25px;
            border: 4px solid var(--black);
            box-shadow: 6px 6px 0 rgba(0,0,0,0.15);
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
            background: linear-gradient(135deg, #2196F3, #21CBF3);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 25px;
            border: 3px solid var(--black);
            box-shadow: 3px 3px 0 rgba(0,0,0,0.2);
        }

        .stats-team {
            font-family: 'Fredoka One', cursive;
            font-size: 1.2em;
            color: var(--black);
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
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
            font-family: 'Fredoka One', cursive;
            font-size: 1.15em;
            color: #2196F3;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 25px;
            color: white;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-size: 1.1em;
        }

        footer span {
            color: #FFD700;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.3);
        }

        /* Intensity Meter */
        .intensity-section {
            margin-bottom: 25px;
        }

        .intensity-track {
            height: 45px;
            background: linear-gradient(90deg, #4CAF50, #FFEB3B, #FF5722);
            border-radius: 25px;
            border: 4px solid var(--black);
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 3px 10px rgba(0,0,0,0.2);
        }

        .intensity-marker {
            position: absolute;
            top: -12px;
            width: 6px;
            height: 69px;
            background: var(--black);
            border-radius: 3px;
            transition: left 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            left: 0;
        }

        .intensity-marker::after {
            content: '🔥';
            position: absolute;
            top: -35px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 30px;
            animation: fire-shake 0.4s ease-in-out infinite;
        }

        @keyframes fire-shake {
            0%, 100% { transform: translateX(-50%) rotate(-8deg); }
            50% { transform: translateX(-50%) rotate(8deg); }
        }

        .intensity-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            font-family: 'Fredoka One', cursive;
            font-size: 0.9em;
            color: var(--black);
        }
    </style>
</head>
<body>
    <!-- Cartoon Stadium Background -->
    <div class="stadium-bg">
        <div class="sky">
            <div class="cloud cloud1"></div>
            <div class="cloud cloud2"></div>
            <div class="cloud cloud3"></div>
        </div>
        
        <div class="stadium-lights">
            <div class="light-tower">
                <div class="tower-base"></div>
                <div class="tower-pole"></div>
                <div class="light-box">
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                </div>
            </div>
            <div class="light-tower">
                <div class="tower-base"></div>
                <div class="tower-pole"></div>
                <div class="light-box">
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                </div>
            </div>
            <div class="light-tower">
                <div class="tower-base"></div>
                <div class="tower-pole"></div>
                <div class="light-box">
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                    <div class="bulb"></div>
                </div>
            </div>
        </div>

        <div class="stadium-stands"></div>

        <div class="field">
            <div class="field-lines">
                <div class="center-circle">
                    <div class="center-spot"></div>
                </div>
                <div class="halfway-line"></div>
                <div class="penalty-box-top"></div>
            </div>
        </div>
    </div>

    <!-- Moving Draggable Footballs -->
    <div class="floating-balls" id="floatingBalls"></div>
    
    <!-- Confetti -->
    <div class="confetti-container" id="confetti"></div>

    <div class="container">
        <!-- Header -->
        <header class="scroll-animate scale">
            <div class="logo-container">
                <svg class="logo-football" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="45" fill="white" stroke="black" stroke-width="4"/>
                    <path d="M50 5 L50 20 M50 80 L50 95 M5 50 L20 50 M80 50 L95 50" stroke="black" stroke-width="4"/>
                    <path d="M22 22 L35 35 M65 65 L78 78 M22 78 L35 65 M65 35 L78 22" stroke="black" stroke-width="4"/>
                    <polygon points="50,30 65,45 60,65 40,65 35,45" fill="none" stroke="black" stroke-width="3"/>
                </svg>
                <div>
                    <h1>Match Predictor</h1>
                    <p class="subtitle">AI-Powered Football Analytics</p>
                </div>
            </div>
        </header>

        <!-- Main Card -->
        <div class="card scroll-animate">
            <!-- Match Selector -->
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

            <!-- Predict Button -->
            <button class="predict-btn" onclick="predictMatch()">
                🔮 Predict Match
            </button>

            <!-- Loading with Classic Football Buffer -->
            <div class="loading-container" id="loading">
                <div class="football-buffer">
                    <svg class="buffer-football" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="white" stroke="black" stroke-width="3"/>
                        <path d="M50 5 L50 20 M50 80 L50 95 M5 50 L20 50 M80 50 L95 50" stroke="black" stroke-width="3"/>
                        <path d="M22 22 L32 32 M68 68 L78 78 M22 78 L32 68 M68 32 L78 22" stroke="black" stroke-width="3"/>
                        <path d="M35 35 L50 25 L65 35 L60 50 L50 55 L40 50 Z" fill="none" stroke="black" stroke-width="2"/>
                        <path d="M35 35 L25 25 M65 35 L75 25 M60 50 L70 60 M40 50 L30 60 M50 55 L50 70" stroke="black" stroke-width="2"/>
                    </svg>
                    <div class="buffer-shadow"></div>
                </div>
                <p class="loading-text">Analyzing Match<span class="loading-dots"></span></p>
            </div>

            <!-- Results -->
            <div class="results-container" id="results"></div>
        </div>

        <!-- Footer -->
        <footer class="scroll-animate">
            <p>⚡ Powered by <span>Machine Learning</span> & <span>Data Analytics</span> ⚡</p>
        </footer>
    </div>

    <script>
        // Create moving and draggable footballs
        function createFloatingBalls() {
            const container = document.getElementById('floatingBalls');
            const ballSVG = `
                <svg viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="45" fill="white" stroke="black" stroke-width="3"/>
                    <path d="M50 5 L50 20 M50 80 L50 95 M5 50 L20 50 M80 50 L95 50" stroke="black" stroke-width="3"/>
                    <path d="M22 22 L32 32 M68 68 L78 78 M22 78 L32 68 M68 32 L78 22" stroke="black" stroke-width="3"/>
                </svg>
            `;
            
            for (let i = 0; i < 8; i++) {
                const ball = document.createElement('div');
                ball.className = 'float-football';
                ball.innerHTML = ballSVG;
                
                // Random starting position
                const startX = 5 + Math.random() * 90;
                const startY = 10 + Math.random() * 80;
                ball.style.left = startX + '%';
                ball.style.top = startY + '%';
                
                // Movement properties
                ball.dataset.vx = (Math.random() - 0.5) * 3;
                ball.dataset.vy = (Math.random() - 0.5) * 3;
                ball.dataset.x = startX;
                ball.dataset.y = startY;
                ball.dataset.rotation = 0;
                ball.dataset.isDragging = 'false';
                
                // Make draggable
                makeDraggable(ball);
                
                container.appendChild(ball);
            }
            
            // Start animation loop
            animateBalls();
        }
        
        // Animate balls moving around
        function animateBalls() {
            const balls = document.querySelectorAll('.float-football');
            
            balls.forEach(ball => {
                if (ball.dataset.isDragging === 'true') return;
                
                let x = parseFloat(ball.dataset.x);
                let y = parseFloat(ball.dataset.y);
                let vx = parseFloat(ball.dataset.vx);
                let vy = parseFloat(ball.dataset.vy);
                let rotation = parseFloat(ball.dataset.rotation);
                
                // Update position
                x += vx * 0.15;
                y += vy * 0.15;
                rotation += 3;
                
                // Bounce off walls
                if (x <= 2 || x >= 93) {
                    vx = -vx;
                    ball.dataset.vx = vx;
                }
                if (y <= 2 || y >= 85) {
                    vy = -vy;
                    ball.dataset.vy = vy;
                }
                
                // Keep in bounds
                x = Math.max(2, Math.min(93, x));
                y = Math.max(2, Math.min(85, y));
                
                ball.dataset.x = x;
                ball.dataset.y = y;
                ball.dataset.rotation = rotation;
                ball.style.left = x + '%';
                ball.style.top = y + '%';
                
                // Rotate
                const svg = ball.querySelector('svg');
                if (svg) {
                    svg.style.transform = `rotate(${rotation}deg)`;
                }
            });
            
            requestAnimationFrame(animateBalls);
        }
        
        // Draggable functionality
        function makeDraggable(element) {
            let isDragging = false;
            let startX, startY, initialLeft, initialTop;
            
            element.addEventListener('mousedown', dragStart);
            element.addEventListener('touchstart', dragStart, {passive: false});
            
            function dragStart(e) {
                e.preventDefault();
                isDragging = true;
                element.dataset.isDragging = 'true';
                element.classList.add('dragging');
                
                const clientX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
                const clientY = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
                
                startX = clientX;
                startY = clientY;
                initialLeft = element.offsetLeft;
                initialTop = element.offsetTop;
                
                document.addEventListener('mousemove', drag);
                document.addEventListener('touchmove', drag, {passive: false});
                document.addEventListener('mouseup', dragEnd);
                document.addEventListener('touchend', dragEnd);
            }
            
            function drag(e) {
                if (!isDragging) return;
                e.preventDefault();
                
                const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
                const clientY = e.type === 'touchmove' ? e.touches[0].clientY : e.clientY;
                
                const dx = clientX - startX;
                const dy = clientY - startY;
                
                const newLeft = initialLeft + dx;
                const newTop = initialTop + dy;
                
                element.style.left = newLeft + 'px';
                element.style.top = newTop + 'px';
                element.dataset.x = (newLeft / window.innerWidth) * 100;
                element.dataset.y = (newTop / window.innerHeight) * 100;
            }
            
            function dragEnd() {
                isDragging = false;
                element.dataset.isDragging = 'false';
                element.classList.remove('dragging');
                
                document.removeEventListener('mousemove', drag);
                document.removeEventListener('touchmove', drag);
                document.removeEventListener('mouseup', dragEnd);
                document.removeEventListener('touchend', dragEnd);
            }
        }
        
        createFloatingBalls();

        // Scroll Animation Observer
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.scroll-animate').forEach(el => {
            observer.observe(el);
        });

        // Create confetti
        function createConfetti() {
            const container = document.getElementById('confetti');
            container.innerHTML = '';
            const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#95E1D3', '#FFA07A', '#98D8C8'];
            
            for (let i = 0; i < 60; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 0.5 + 's';
                confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
                confetti.style.width = (8 + Math.random() * 8) + 'px';
                confetti.style.height = confetti.style.width;
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
                    
                    // Re-observe new elements for scroll animation
                    document.querySelectorAll('.results-container .scroll-animate').forEach(el => {
                        observer.observe(el);
                    });
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
                <div class="winner-banner scroll-animate scale">
                    <div class="winner-text">${winnerText}</div>
                    <div class="confidence-pill">
                        <span>🎯</span>
                        <span>AI Confidence: <span id="confValue">0</span>%</span>
                    </div>
                </div>

                <div class="intensity-section scroll-animate left">
                    <div class="section-title">
                        <span>🔥</span> Match Intensity Meter
                    </div>
                    <div class="intensity-track">
                        <div class="intensity-marker" id="intensityMarker"></div>
                    </div>
                    <div class="intensity-labels">
                        <span>Calm</span>
                        <span>Competitive</span>
                        <span>INTENSE!</span>
                    </div>
                </div>

                <div class="prob-section scroll-animate right">
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
                                <svg class="mini-football" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="45" fill="white" stroke="black" stroke-width="4"/>
                                    <path d="M50 10 L50 25 M50 75 L50 90 M10 50 L25 50 M75 50 L90 50" stroke="black" stroke-width="4"/>
                                </svg>
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
                                <svg class="mini-football" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="45" fill="white" stroke="black" stroke-width="4"/>
                                    <path d="M50 10 L50 25 M50 75 L50 90 M10 50 L25 50 M75 50 L90 50" stroke="black" stroke-width="4"/>
                                </svg>
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
                                <svg class="mini-football" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="45" fill="white" stroke="black" stroke-width="4"/>
                                    <path d="M50 10 L50 25 M50 75 L50 90 M10 50 L25 50 M75 50 L90 50" stroke="black" stroke-width="4"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="goals-section scroll-animate">
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

                <div class="section-title scroll-animate left">
                    <span>📈</span> Team Statistics
                </div>
                <div class="stats-section">
                    <div class="stats-card scroll-animate left">
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
                    <div class="stats-card scroll-animate right">
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
        print(f"⚽ FINAL CARTOON STADIUM PREDICTOR RUNNING!")
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
