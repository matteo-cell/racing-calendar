# Racing Calendar

Genera automaticamente un calendario `.ics` con gli orari precisi delle sessioni F1
(e in futuro altri campionati), aggiornato ogni notte via GitHub Actions e pubblicato
tramite GitHub Pages.

## Come mettere in produzione (una tantum)

### 1. Carica questi file nel tuo repository GitHub

Struttura attesa:

```
racing-calendar/
├── .github/workflows/update-calendar.yml
├── scripts/generate_f1.py
├── docs/                (verrà creata automaticamente dallo script)
├── requirements.txt
└── README.md
```

### 2. Esegui il workflow la prima volta

- Vai su GitHub → tab "Actions" del tuo repo
- Se richiesto, clicca "I understand my workflows, go ahead and enable them"
- Seleziona il workflow "Aggiorna calendario gare" nella sidebar sinistra
- Clicca "Run workflow" → "Run workflow" (branch main)
- Attendi ~30 secondi, poi verifica che sia verde. Se rosso, apri i log per vedere l'errore
- Al termine, dovrebbe apparire il file `docs/f1.ics` nel repo (committato dal bot)

### 3. Attiva GitHub Pages

- Vai su Settings del repo → Pages (menu laterale)
- Sotto "Build and deployment" → Source: "Deploy from a branch"
- Branch: `main`, cartella: `/docs` → Save
- GitHub ti mostrerà l'URL pubblico, tipo:
  `https://TUOUSERNAME.github.io/racing-calendar/`
- Il file calendario sarà quindi raggiungibile a:
  `https://TUOUSERNAME.github.io/racing-calendar/f1.ics`

  (Puoi impiegare 1-2 minuti la prima volta prima che sia online.)

### 4. Sottoscrivi il calendario su iPhone

- Impostazioni → App → Calendario → Account → Aggiungi account → Altro → Aggiungi calendario sottoscritto
- Incolla l'URL: `https://TUOUSERNAME.github.io/racing-calendar/f1.ics`
- iOS aggiornerà automaticamente il calendario a intervalli regolari (in genere ogni poche ore)

Da qui in poi: zero manutenzione. Ogni notte lo script gira da solo, e se il calendario F1
cambia (orario spostato, sessione cancellata) il file si aggiorna e iPhone lo recepisce
al successivo refresh automatico.

## Prossimi passi

- Aggiungere script analoghi per MotoGP/Moto2/Moto3 (stessa logica, sorgente dati diversa)
- Unire i file in un unico `.ics` combinato, o tenerli separati per poter attivare/disattivare
  singoli campionati su iPhone
- Aggiungere gli script "manuali" per il Gruppo 2 (serie GT/turismo) come file YAML/JSON
  statici aggiornati 1-2 volte a stagione
