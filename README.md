# WordTalk - Telugu Slang Corpus Collection App

A gamified Streamlit application for collecting Telugu slang words and building a comprehensive language corpus.

## Features

🎮 **Gamification Elements:**
- Level progression system (10 levels from Rookie to Master)
- Achievement system with badges and rewards
- Daily challenges and streaks
- Combo multipliers for consecutive high scores
- Power-ups and special rewards

🌍 **Data Collection:**
- User authentication with location tracking
- Interactive maps for geographic data
- Semantic similarity scoring using AI
- Multi-language support (Telugu/English)
- CSV data export for research

🏆 **Social Features:**
- Real-time leaderboard
- User statistics and progress tracking
- Weekly challenges and competitions
- Achievement sharing

## Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
wordtalk-app/
├── app.py                 # Main application entry point
├── config.py             # Page configuration and CSS styling
├── language.py           # Multi-language support
├── auth.py              # User authentication and login
├── main_app.py          # Main corpus collection interface
├── word_explanation.py   # Word explanation and scoring
├── leaderboard.py       # Leaderboard and statistics
├── scoring.py           # AI-based semantic scoring
├── words.py             # Telugu word collections
├── gamification.py      # Game mechanics and achievements
├── admin.py             # Admin panel for data management
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Usage

1. **Login**: Fill in your personal details and location
2. **Create Corpus**: Choose a category and describe your slang collection
3. **Explain Words**: Provide explanations for Telugu slang words
4. **Earn Points**: Get scored based on semantic similarity
5. **Level Up**: Progress through levels and unlock achievements
6. **Compete**: Check the leaderboard and compete with others

## Admin Features

- Access admin panel with password: `admin@123`
- Download collected data as CSV
- Reset application data
- View platform statistics

## Technical Details

- **Framework**: Streamlit
- **AI Model**: Sentence Transformers (all-MiniLM-L6-v2)
- **Maps**: Folium with Streamlit integration
- **Data Storage**: CSV files
- **Styling**: Custom CSS with animations

## Data Collection

The app collects:
- User demographics and location
- Telugu slang words and explanations
- Semantic similarity scores
- Usage context and categories
- Temporal data for analysis

## Contributing

This is a research project for Telugu language corpus building. Contributions and feedback are welcome!

## License

This project is for educational and research purposes.