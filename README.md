# CS-340-10389-M01-Client-Server-Development-2025

## About

This repository is part of my ongoing CS portfolio.This repository is part of my ongoing CS portfolio. It contains my Project Two dashboard for Grazioso Salvare plus the write-up that explains how to run it and why I built it the way I did.

## Repository Contents

ProjectTwoDashboard.ipynb (Dash app with interactive table, role filters, pie chart, and map)
CRUD_Python_Module.py (Reusable CRUD helper connecting to MongoDB)
Grazioso Salvare Logo.png (Logo used in the header)
README_ProjectTwo.docx (README with screenshots)

screenshots 
01_start.png (Reset/All)
02_water.png (Water Rescue)
03_mountain.png (Mountain/Wilderness)
04_disaster.png (Disaster / Individual Tracking)
05_reset_selected.png (Reset with first row selected, map pin visible)

---
## How to Run
1. With MongoDB running, import the dataset once:

cd datasets
mongoimport --type=csv --headerline --db aac --collection animals --drop ./aac_shelter_outcomes.csv

2. Ensure the DB user exists in mongosh

use admin
db.createUser({ user: "aacuser", pwd: passwordPrompt(), roles:[{role:"readWrite", db:"aac"}] })

3. Open ProjectTwoDashboard.ipynb and run all cells. The app runs inline on port 8050. If a port is busy, change to 8051 in the last line.
   (I used username aacuser and password PasswordIsPie. For public repos, replace with your own credentials or environment variables.)

---

## Additional Reflections

1) Maintainable, readable, adaptable code - 

I wrote a small AnimalShelter class to handle MongoDB connections and CRUD. Keeping database logic in one place made the dashboard code simple: callbacks just call read(query) and render results. The advantages were obvious when I moved from Project One to Project Two. I didn’t rewrite database code; I reused it. In the future, I can plug the same module into another Dash app, a Flask API, or even a CLI tool by only changing constructor args such as host, port, and db names. Having clear names, short functions, and early returns also helped with readability.

2) My approach to problems as a computer scientist - 

I start with the requirements, then map them to data and behavior. For this project I listed each rescue role and turned it into a MongoDB query: allowed breeds, age windows in weeks, and the required sex status. After that I sketched the MVC: MongoDB as Model, Dash widgets as View, and callbacks plus the CRUD class as Controller. Compared to past assignments, I spent more time isolating concerns so the UI didn’t know anything about connection strings or auth. If I build future databases for a client, I’ll keep doing domain-driven queries first, then wrap them behind clean interfaces, and finally build one or two automated tests to make sure the filters don’t regress.

3) What computer scientists do and why it matters - 

We turn messy data and fuzzy goals into tools people can actually use. Here, a small nonprofit can quickly find dogs that fit strict training profiles. That saves time, reduces manual filtering, and helps them place the right animals into the right programs faster. Even a lightweight dashboard can meaningfully improve decisions and outcomes when the data is current and the interaction is simple.

---

## Collaborators
For this assignment, I have added my instructor **ProfessorScranton** as a collaborator so they can review my portfolio work.

## Acknowledgments
Thanks to my instructor and classmates for their support and detailed feedback throughout the CS-340 course.

## Contact
For any questions or suggestions, please feel free to open an issue or contact me.
