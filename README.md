# PlayerLens

PlayerLens is a machine-learning–driven football analytics application designed to evaluate a player’s overall match influence and performance consistency using structured match data. The project focuses on translating raw football statistics into interpretable insights that go beyond traditional metrics such as goals and assists.

## Problem Statement
Conventional football metrics often fail to capture a player’s true influence on a match, especially for non-goal-scoring roles. There is a need for a more holistic, data-driven approach to assess player impact and consistency across matches.

## How PlayerLens Differs from xG
Expected Goals (xG) is a shot-centric metric that estimates the probability of a shot resulting in a goal. PlayerLens is player-centric and context-aware. While xG may be used as one of several input signals, PlayerLens evaluates overall match influence by considering technical actions, involvement, efficiency, role-based expectations, and match context. The objective is not to measure chance quality, but to quantify how much a player meaningfully affected the game.

## System Overview
The project is structured as a modular ML application consisting of:
- Data preprocessing and feature engineering
- Machine learning models for player impact estimation
- A backend service to serve statistics and predictions
- An interactive frontend for user exploration

## Features
- Player-level statistical analysis
- ML-based impact and consistency scoring
- Match and season-level comparisons
- Interactive visualization of stats and predictions

## Tech Stack
- Python
- Pandas, NumPy, scikit-learn
- Flask or FastAPI (backend)
- Simple web frontend (to be added)

## Future Enhancements
- Advanced contextual modeling
- Expanded datasets and leagues
- Enhanced visual analytics
