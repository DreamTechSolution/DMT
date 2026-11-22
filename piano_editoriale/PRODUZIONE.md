# Procedura di produzione di una serie ("Lo sapevi? Te lo spiega Claudio")

Ogni serie = 2 Reel verticali 1080×1920 in italiano: **v1** (~45-60 s, "cosa è successo") e **v2** (~60-85 s, "perché ti riguarda / cosa fare"). Una serie vive in `serieNN/` (vedi `serie04/` come modello completo).

## Regole editoriali (obbligatorie)
- Solo fatti verificati su fonti primarie o di primo livello (Reuters, Bloomberg, CNBC, FT, WSJ, Il Sole 24 Ore, ANSA, Istat, BCE, Banca d'Italia, Consob, documenti ufficiali). Ogni cifra ha una fonte annotata in `piano_editoriale/ricerche/`.
- Separare fatti e scenari ("scenari, non certezze"). Indagine ≠ accusa. "Sospetto" ≠ reato.
- Parola vietata: "bruciati" (usare "liquidati" o "persi").
- Mercati, titoli, investimenti, crypto: "Questo non è un consiglio finanziario." a voce e a schermo nel v2 (e riga a schermo nel v1 se si parla di titoli).
- Persone: solo fatti pubblici e ruoli; mai vita privata o pettegolezzi; niente nomi di persone non accusate formalmente.
- Il nome "Claude/Anthropic" va trattato in modo neutrale.

## Struttura file di una serie
```
serieNN/
  engine.js style.css render.js   ← copiati da serie01/ (NON modificarli)
  v1.html v2.html                  ← scene (copiare la struttura di serie04/v1.html)
  durs1.js durs2.js voce1/ voce2/  ← generati da tools/fetch_voice.py
  cover.html                       ← copiato da serie04/cover.html, cambiare solo V e il disegno
  out/serieNN_parte1.mp4 out/serieNN_parte2.mp4 out/cover_serieNN_parte1.jpg out/cover_serieNN_parte2.jpg
```
Copione in `piano_editoriale/copioni/serieNN_<tema>.md` (tabella Sez. | Voce | A schermo).

## Passi
1. **Copione**: sezioni A, B, C… ognuna = una scena = una frase/blocco di voce. La prima sezione è sempre `I` (sigla, voce già pronta) e l'ultima `H` (chiusura: v1 = rimando alla parte 2, v2 = "Salva il video…" + domanda per i commenti).
2. **Voce** (Higgsfield, voce Marcus): per ogni sezione chiamare `mcp__higgsfield__generate_audio_batch` con
   `{"model":"elevenlabs_v4","prompt":"<etichetta>","dialogue":[{"text":"<testo>","voice_type":"preset","voice_id":"6f98d3dd-324f-4845-8c28-c1d1647a06cd"}],"stability":0.4,"similarity_boost":0.8}`.
   Massimo 6 job contemporanei per l'account (se "Rate limit reached", aspettare con `mcp__higgsfield__jobs_wait` e reinviare solo quelli falliti). Numeri scritti in lettere nel testo ("ottantatré dollari"). Non rigenerare la sigla `I`.
3. **Scarica e prepara**: `python3 tools/fetch_voice.py serieNN 1 A=<url> B=<url> ...` (idem per 2). Stampa le durate.
4. **Scene**: scrivere `v1.html`/`v2.html` come in `serie04`. `window.ORDER` = ['I','A',…,'H']. Ogni scena `R.X=(t,d)=>{…}` usa il tempo locale `t` (la voce della sezione inizia a t≈0,25 s e dura quanto in `voce?/durations.json`): far apparire gli elementi quando la voce li nomina. Helper disponibili da engine.js: `ap`, `pop`, `words`, `typeT`, `drawPath`, `fmt`, `P`, `eo`, `eio`, `eback`, `ex`, `rnd`.
   - Stile: sfondi scuri (#121014, #0d1022, #071410…) o carta (#f4f0e8); arancio #e2683c / #c94f2a; crema #f3ebde; titoli `bold` (Archivo Black maiuscolo), frasi `serif` corsivo, dati `mono`.
   - **Elementi grafici NUOVI per ogni serie** (non riusare scene di altre serie: niente stessa ellisse, griglia, scrigno, razzo…). Solo lo stile è comune.
   - Zona sicura Instagram: contenuto tra y≈280 e y≈1450. Nessun testo deve uscire dai 1080 px di larghezza (ridurre font-size se serve).
5. **Controllo visivo**: `tools/stills.sh serieNN 1 /tmp/x.png` → guardare l'immagine; correggere testi che escono dal bordo, sovrapposizioni, scene vuote. Ripetere per v2.
6. **Mix**: `python3 tools/build_mix.py serieNN 1 I,A,B,…,H A:<sec> B:<sec>` (i valori sono i secondi locali dei "pop" principali, per gli effetti sonori).
7. **Render**: `tools/render_video.sh serieNN 1 serieNN_parte1` (poi parte 2). Un render alla volta per agente (la CPU è condivisa).
8. **Copertine**: `cover.html` (modello serie04) → `out/cover_serieNN_parte1.jpg` e `parte2.jpg` (screenshot 1080×1920 di `cover.html?v=p1`/`p2`), titolo che stia nei bordi. Versione 4:5: `ffmpeg -i out/cover_…jpg -vf "crop=1080:1350:0:300" copertine_post/<tema>_parteN_4x5.jpg`.
9. **Didascalie**: scrivere in `piano_editoriale/didascalie_serieNN.md` le due descrizioni Instagram (gancio in prima riga, punti chiave con cifre, fonti, disclaimer se finanziario, 3-5 hashtag, rimando all'altra parte).
10. **Verifica finale**: durata mp4 ≈ durata stampata; contact sheet di 1 fotogramma ogni 5 s; volume max < 0 dB.

NON fare git commit/push (lo fa il coordinatore).
