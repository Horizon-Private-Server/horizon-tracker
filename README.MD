# Horizon Tracker Backend

This repository is for the backend for the Horizon Private Server's tracker for Retched and Clank: Up Your Arsenal and Ratchet: Deadlocked.
This backend is designed as a proxy for the production Horizon database and middleware.
This interface is designed to ingest player data and store it in a more usable format for improved data analytics.

This backend serves as an API to drive the following game features.

### Ratchet and Clank: Up Your Arsenal

1. Stats
   1. Leaderboards
   2. Player cards
   3. Account Aggregations (account merging)
2. In-Game Real-Time Updates (Based on the UYA Tracker by Nick1)

### Ratchet Deadlocked

1. Stats
   1. Leaderboards
   2. Custom Leaderboards
   3. Player Cards + Survival Player Cards
2. Games
   1. Game History
3. Tracker (TBD)

## Setup

TBD Setup Guide

## Structure

1. `horizon/` - Root folder for all code.
   1. `models/` - SQLAlchemy ORM model files.
   2. `parsing/` - Collection of utilities for processing data from the Horizon production servers. This is separate from `utils/` as a place to incorporate existing code.
   3. `schemas/` - SQLAlchemy ORM schema files.
   4. `utils/` - General utilities folder.
   5. `views/` - API Create, Read, Update, Delete (CRUD) routes.