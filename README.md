# APImmerce 🎮

APImmerce is a lightweight e-commerce style game catalog built with Flask, DuckDB, and Tailwind CSS. It consumes the RAWG API to display game data, allowing users to browse, filter, and favorite games, all with local storage powered by DuckDB.

---

## Features

- Fetches game data dynamically from the RAWG API
- Displays games in a clean, responsive grid layout with Tailwind CSS
- Shows detailed information about each game
- Supports filtering and searching (to be implemented)
- Stores user favorites and viewed games locally using DuckDB

---

## Tech Stack

- **Flask** — Backend framework
- **DuckDB** — Local analytics and storage
- **Tailwind CSS** — Styling and responsive design
- **RAWG API** — Game data source

---

## Getting Started

### Prerequisites

- Python 3.7+
- Node.js and npm (for Tailwind CSS build)

### Installation

1. Clone the repo

   ```bash
   git clone https://github.com/seu-usuario/APImmerce.git
   cd APImmerce
   ```

2. Run the Flask app

```bash
python app.py
```
