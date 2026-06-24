# SAFIR: Agricultură inteligentă bazată pe inteligență artificială și irigații pentru reziliență

## Prezentare generală

SAFIR este o soluție **open-source și finalizată** de monitorizare inteligentă a irigațiilor pentru reziliența climatică în Laos. Proiectul a fost creat de **Asociația Grupul Verde** în parteneriat cu **35 de tineri din județul Vrancea, România**.

### Ce combină SAFIR

- modele de prognoză a apelor subterane
- modele LSTM pentru previziuni de umiditate a solului
- controlere solare inteligente pentru irigații
- programator de învățare prin consolidare pentru adaptare dinamică
- endpoint-uri API și tablouri de bord open-data pentru acces și colaborare

## Angajament Open Source

Toate componentele sunt **publice și gratuite** pentru reutilizare, îmbunătățire și colaborare. Codul și datele senzorilor pot fi distribuite prin depozite Python și endpoint-uri API deschise pentru a sprijini transparența și adoptarea locală.

## Structura proiectului

```
Proiect_codMediu/
├── static/
│   ├── index.html          ← Pagina finalizată gata de publicare
│   └── demo.html           ← Versiunea demo
├── src/safir/
│   ├── api.py              ← API FastAPI complet cu endpoint-uri
│   ├── groundwater_forecast.py
│   ├── soil_moisture_lstm.py
│   ├── solar_irrigation_controller.py
│   ├── rl_scheduler.py
│   ├── dashboard.py
│   ├── data_ingestion.py
│   ├── cli.py
│   └── server.py
├── data/
│   └── sample_sensor_data.csv    ← Date de test
├── setup.py                       ← Configurare pachet
├── README.md                      ← Documentație
└── LICENSE                        ← MIT License
```

## Instalare și Lansare

### 1. Mediu Python

```bash
cd Proiect_codMediu
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalare pachet

```bash
pip install -e .
```

### 3. Rulează serverul SAFIR

```bash
safir serve --host 127.0.0.1 --port 8000
```

### 4. Acces pagini

- **Index principal (pagina finalizată):**
  ```
  http://127.0.0.1:8000/static/index.html
  ```

- **Demo alternativ:**
  ```
  http://127.0.0.1:8000/static/demo.html
  ```

- **API Swagger Documentation:**
  ```
  http://127.0.0.1:8000/docs
  ```

## Endpoint-uri API

### Senzori & Monitorizare

- `POST /sensor` — Trimite date senzor
- `GET /sensor` — Obține toate datele senzorilor
- `GET /dashboard` — Sumar tablou de bord cu metrici

### Prognoze

- `GET /forecast/groundwater` — Prognoză apă subterană

### Informații Proiect

- `GET /project/info` — Detalii proiect și caracteristici
- `GET /project/team` — Informații echipă și organizație
- `GET /api/status` — Status API și lista endpoint-uri

## Testare rapidă

Pentru a valida un fișier CSV de date cu schema de senzori:

```bash
python3 -m safir ingest data/sample_sensor_data.csv
```

## Tehnologii Utilizate

- **Python 3.9+** — Limbaj principal
- **FastAPI** — Framework web pentru API
- **TensorFlow** — Model LSTM pentru predicții
- **Pandas & NumPy** — Procesare date
- **Scikit-learn** — ML utilities
- **Chart.js** — Vizualizări grafice pe frontend

## Echipa și Organizație

- **Asociația Grupul Verde** — Coordonare și implementare
- **35 Tineri din Județul Vrancea** — Design, date, testare și promovare
- **Scop:** Agricultură durabilă și reziliență climatică

## Publicare și Deployment

### Opțiunea 1: Local (Development)

```bash
safir serve --host 127.0.0.1 --port 8000
```

### Opțiunea 2: Public (Production)

```bash
safir serve --host 0.0.0.0 --port 8000
```

Apoi configurează un reverse proxy (nginx) și SSL certificate (Let's Encrypt).

### Opțiunea 3: Docker

```bash
docker build -t safir-irrigation .
docker run -p 8000:8000 safir-irrigation
```

## Licență

Acest proiect este licențiat **MIT**. Vezi `LICENSE` pentru detalii complete.

---

**SAFIR © 2026 — Dezvoltat de Asociația Grupul Verde | Pentru o agricultură durabilă și reziliență climatică în Laos și Vrancea**
