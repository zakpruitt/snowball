# Snowball

## 1. Project Overview
Snowball is a desktop analytics suite for MaddenCo customer support operations. The Electron shell embeds a Flask web
application that ingests daily support reports, normalizes the data into a SQLite database, and exposes interactive tables and
charts to help the team track call and email workloads.

## 2. Features
- **Guided report parsing** – Upload single or multiple raw reports and automatically extract call and email activity.
- **Data stewardship tools** – Review, edit, and delete call records and employee metadata directly from the built-in sheets view.
- **Visualization dashboards** – Generate bar and pie charts showing employee performance, sub-department volume, and channel mix.
- **Export-ready formatting** – Normalize data and formatting helpers that keep downstream Excel outputs consistent.
- **Packaged desktop runtime** – Electron shell bundles the Python server and static assets for a turn-key Windows installer.

## 3. Tech Stack
- **Frontend**: Electron, HTML templates, Chart.js (via Flask templates)
- **Backend**: Python 3, Flask, SQLite, Pillow
- **Tooling**: Node.js, electron-packager, python-shell, tree-kill

## 4. Getting Started
### Prerequisites
- Node.js 16+
- npm 8+
- Python 3.9+
- Windows build tools for packaging (only required when running `npm run build`)

### Installation
```bash
# clone the repository
git clone https://github.com/zakpruitt/senior-project.git
cd senior-project

# install Node.js dependencies
npm install

# (optional) create a Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`

# install Python requirements
pip install Flask Pillow
```

### Configuration
- Ensure the `data/` directory contains a writable SQLite database (a starter `snowball.db` is included).
- The application stores temporary uploads in `resources/app/data/temp/`; the folder is created automatically on first run.
- Update `src/static/myIcon.ico` to customize the packaged application icon.

### Run Locally
```bash
# start the Electron shell (spawns the Flask server automatically)
npm start
```
This command launches the Electron wrapper and opens the UI at `http://127.0.0.1:5000` in the desktop window.

### Run Tests
The project does not yet include automated tests. You can run the placeholder script to confirm wiring:
```bash
npm test
```

## 5. API Documentation
| Method | Route | Description |
| ------ | ----- | ----------- |
| GET | `/` | Render the home dashboard. |
| GET/POST | `/parse/` | Upload report files for single or multi-file parsing workflows. |
| GET | `/sheets/` | Display parsed call and employee tables. |
| POST | `/sheets/delete` | Remove a specific call record from the database. |
| GET | `/data/all-count` | Retrieve aggregated counts for total calls and emails. |
| GET | `/data/bar-data` | Return per-employee totals filtered by date range and sub-department. |
| GET | `/data/pie-email-data` | Return pie chart data for email counts by employee. |
| GET | `/data/pie-data` | Return pie chart data for immediate vs. later calls by employee. |
| GET/POST | `/settings/` | Manage employee metadata, color assignments, and department mappings. |

## 6. Project Structure
```
.
├── data/                # SQLite database
├── main.js              # Electron bootstrapper that launches the Python server
├── package.json         # Node.js manifest and scripts
├── src/
│   ├── main.py          # Flask entry point
│   ├── routes/          # Flask blueprints for views and APIs
│   ├── models/          # SQLite data access layer
│   ├── templates/       # HTML templates rendered by Flask
│   ├── static/          # Icons, styles, and client-side assets
│   └── utility.py       # Helpers for file handling and configuration
└── README.md
```

## 7. Contributing
We welcome contributions that improve data workflows, visualizations, or packaging automation:
1. Fork the project and create a feature branch (`git checkout -b feature/amazing-improvement`).
2. Commit your updates with descriptive messages.
3. Run `npm start` to verify the UI loads and any manual QA steps relevant to your change.
4. Submit a pull request describing the problem, solution, and testing.

## 8. License
Distributed under the **Apache 2.0 License**. See the [`LICENSE`](LICENSE) file for details.

## 9. Contact
- Zak Pruitt – [LinkedIn](https://www.linkedin.com/in/zak-pruitt-136567191/) · pruittzn@gmail.com
- Swayde Sanders – [LinkedIn](https://www.linkedin.com/in/zak-pruitt-136567191/) · ssanders2@eagles.usi.edu
- Logan Oakley – [LinkedIn](https://www.linkedin.com/in/zak-pruitt-136567191/) · loakley@eagles.usi.edu

Project Link: [https://github.com/zakpruitt/senior-project](https://github.com/zakpruitt/senior-project)
