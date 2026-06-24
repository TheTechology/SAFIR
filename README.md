# SAFIR — Sistem AI de Monitorizare Irigații

**Transformă Pixelii în Oxigen** · Asociația Grupul Verde · Vrancea, România

---

SAFIR este o soluție **open-source** de monitorizare inteligentă a irigațiilor, creată de Asociația Grupul Verde împreună cu **55 de tineri din 5 țări europene** (România, Croația, Albania, Danemarca, Germania).

## Website

Deschide [index.html](index.html) direct în browser sau activează **GitHub Pages** din Settings → Pages → Branch: main pentru a-l servi online.

## Ce face SAFIR

- **Prognoză apă subterană** — modele de previziune bazate pe date senzor în timp real
- **LSTM Umiditate Sol** — rețea neurală pentru optimizarea automată a irigațiilor
- **Control Solar** — irigații inteligente pe bază de energie solară și stare baterie
- **Reinforcement Learning** — planificare adaptivă a deciziilor de irigație
- **API REST** — endpoint-uri complete, documentație Swagger inclusă
- **Dashboard Live** — grafice interactive cu simulare 14 zile de date senzor

## Structura proiectului

```
SAFIR/
├── index.html                        ← Website complet (GitHub Pages)
├── data/
│   └── sample_sensor_data.csv        ← Date de test senzori
├── src/safir/
│   ├── api.py                        ← API FastAPI cu toate endpoint-urile
│   ├── groundwater_forecast.py       ← Model prognoză apă subterană
│   ├── soil_moisture_lstm.py         ← Model LSTM umiditate sol
│   ├── solar_irrigation_controller.py← Controler irigații solare
│   ├── rl_scheduler.py               ← Scheduler Reinforcement Learning
│   ├── dashboard.py                  ← Logică dashboard
│   ├── data_ingestion.py             ← Ingestie și validare date
│   ├── cli.py                        ← Interfață linie de comandă
│   └── server.py                     ← Server ASGI
├── setup.py                          ← Configurare pachet Python
├── requirements.txt                  ← Dependințe
└── LICENSE                           ← MIT License
```

## Instalare și Lansare Locală

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
safir serve --host 0.0.0.0 --port 8000
```

Deschide apoi `http://localhost:8000` în browser.

## API Endpoints

| Metodă | Endpoint | Descriere |
|--------|----------|-----------|
| `POST` | `/sensor` | Trimite date senzor |
| `GET` | `/sensor` | Obține toate înregistrările |
| `GET` | `/dashboard` | Sumar tablou de bord |
| `GET` | `/forecast/groundwater` | Prognoză apă subterană |
| `GET` | `/project/info` | Detalii proiect |
| `GET` | `/project/team` | Informații echipă |
| `GET` | `/api/status` | Status API |

Documentație Swagger la `http://localhost:8000/docs`.

## Validare date CSV

```bash
python3 -m safir ingest data/sample_sensor_data.csv
```

## Tehnologii

Python 3.11 · FastAPI · TensorFlow/Keras · Pandas · NumPy · Chart.js · MIT License

## Echipa

| | |
|---|---|
| **Coordonator** | Marian Dumitru — Asociația Grupul Verde |
| **55 tineri europeni** | România · Croația · Albania · Danemarca · Germania |
| **Pilot internațional** | Laos |

---

**SAFIR © 2026 — Asociația Grupul Verde · Adjud, Vrancea · Open Source MIT**

[grupulverde.ro](https://www.grupulverde.ro)
