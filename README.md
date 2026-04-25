# flask-basic

A lightweight Flask hackathon starter template with Blueprints, Jinja2 templates, and simple CSS.

## Stack

- **Backend**: Flask
- **Templates**: Jinja2
- **Styles**: CSS simples
- **Storage**: in-memory list (extensível para SQLite)

## Project Structure

```
flask-basic/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
│
├── templates/
│   ├── base.html
│   └── index.html
│
├── static/
│   └── style.css
│
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python run.py
```

Access at: http://127.0.0.1:5000
