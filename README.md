# APImmerce 🎮

GameBay is a lightweight e-commerce style game catalog built with Flask, DuckDB, and Tailwind CSS. It consumes the RAWG API to display game data, allowing users to browse, filter, and favorite games, all with local storage powered by DuckDB.

---

## Features

- Fetches game data dynamically from the RAWG API
- Displays games in a clean, responsive grid layout with Tailwind CSS by CDN
- Shows detailed information about each game
- Supports filtering and searching (it will implemented)
- Stores user favorites and viewed games locally using DuckDB (it will implemented)

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

2. Create and Open the venv

To create:

```bash
python -m venv venv_gamebay
```

Windows

```bash :
.\venv_gamebay\Scripts\Activate.ps1
```

MacIos

```bash
source venv_gamebay/bin/activate
```

3.Install dependencies

```bash
python install -r requirements.txt
```

4. Run the Flask app

```bash
python app.py
```

IMPORTANT: black . (formata todos os arquivos do projeto)
