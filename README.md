
# 🎮 AXOPY: Learn Python Through Interactive Gaming

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flet-purple?style=for-the-badge&logo=flutter&logoColor=white)](https://flet.dev/)
[![Online Tunnel](https://img.shields.io/badge/Tunneling-ngrok-green?style=for-the-badge)](https://ngrok.com/)
[![Cloud Deployment](https://img.shields.io/badge/Cloud-Render-orange?style=for-the-badge)](https://render.com/)

*An interactive desktop and web game combining classic Tic-Tac-Toe strategy with Python programming education!*


## 🌐 Running & Online Play Options 
You can run and play **AXOPY** using flexible methods:
* **Local Terminal (ngrok Tunnel):** Run the game locally on your machine (`python main.py`) and use **ngrok** as a tunneling tool to generate a public link. This allows you and your friends to play online together instantly from your local session!
* **Cloud Hosting (Render):** The project is fully configured with port and host variables, making it ready for seamless deployment on cloud hosting platforms like **Render**.

---

## 📖 About The Project
**AXOPY** is an educational project built in **Python** using the **Flet** framework. It transforms traditional grid games into an exciting learning platform. Instead of just placing an 'X' or 'O', players must correctly answer Python programming questions to claim a cell on the board!

---

## ✨ Key Features
* 🧠 **Python Knowledge Check:** Test and reinforce your understanding of functions, keywords, arguments, lists, and syntax.
* 👥 **Multiple Game Modes:** 
  * Local Multiplayer (2P) on the same device.
  * Play vs Computer (AI).
  * Online Multiplayer using secure 4-digit room codes.
* ⚡ **Dynamic Strategy Board:** Incorrect answers or skipped questions turn cells into an **"OPEN"** state, revealing the question to everyone and adding tactical depth.
* 🎨 **Clean & Modern UI:** Designed with soft colors, responsive layouts, and a smooth user interface via Flet.

---

## 🕹️ How to Play
1. **Start the Game:** Launch the application and select your preferred game mode from the Main Menu.
2. **Select a Cell:** Click on any available cell in the 3x3 grid.
3. **Answer the Question:** 
   * A Python programming question will pop up. Type your answer and click **Submit**.
   * **Correct Answer:** Your symbol (**X** or **O**) claims the cell! 🎯
   * **Incorrect / Skip:** The cell becomes **OPEN** for everyone, and your turn ends. ⚠️
4. **Win the Game:** Get 3 of your symbols in a row (horizontally, vertically, or diagonally) to win! 🏆

---

## 🚀 Getting Started & Installation

### Prerequisites
Make sure you have Python installed on your machine. You will need to install the **Flet** library:
```bash
pip install flet

