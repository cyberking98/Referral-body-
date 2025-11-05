# Referral-body-

## Översikt
En automatiserad lösning som bearbetar hänvisningslänkar genom att anropa ett API för temporära e-postadresser för kontoskapande. Skriptet navigerar till den angivna URL:en, slutför registreringsflödet och kan därefter autentisera sig på plattformen för att utföra specifika uppföljningsaktiviteter.

## Teknisk Stack
- **Browser Automation:** Playwright
- **Språk:** Python (modulär struktur)
- **Proxy:** OXLabs Residential Proxies
- **Temporär E-post:** Gmailnator (Emailnator) API
- **CAPTCHA Lösning:** 2Captcha

## Projektstruktur
```
Referral-body-/
├── main.py                      # Huvudprogram (under utveckling)
├── gmailnator_service.py        # Gmailnator API integration
├── example_integration.py       # Exempel på användning
├── .env-exmpel                  # Mall för miljövariabler
├── docs/
│   ├── gmailnator_api.md       # Gmailnator API dokumentation
│   ├── gmailnator_usage.md     # Gmailnator användningsguide
│   ├── oxlabs dokumentasjon.md # Oxylabs API dokumentation
│   └── status.md               # Projekt status (uppdateras vid varje ändring)
└── tests/                       # Testfiler (när de skapas)
```

## Snabbstart

### 1. Konfigurera Miljövariabler
Kopiera `.env-exmpel` till `.env` och fyll i dina API-nycklar:
```bash
cp .env-exmpel .env
# Redigera .env med dina nycklar
```

### 2. Installera Beroenden
```bash
# Playwright (för browser automation)
pip install playwright
playwright install

# Övriga beroenden läggs till efter behov
```

### 3. Testa Gmailnator Service
```bash
# Sätt din API-nyckel
export RAPIDAPI_KEY='your_rapidapi_key'

# Kör exempel
python3 example_integration.py
```

## Implementerade Komponenter

### ✅ Gmailnator Service
Komplett implementation av Gmailnator API för temporär e-post.

**Funktioner:**
- Generera temporära e-postadresser (enskilda eller bulk)
- Hämta inbox och meddelanden
- Extrahera verifieringslänkar automatiskt
- Radera meddelanden efter användning

**Dokumentation:**
- [API Referens](docs/gmailnator_api.md)
- [Användningsguide](docs/gmailnator_usage.md)
- Kod: `gmailnator_service.py`
- Exempel: `example_integration.py`

### ⚠️ Under Utveckling
- Playwright integration (exempel finns)
- Oxylabs proxy integration
- 2Captcha integration
- Huvudflöde i `main.py`

## API Dokumentation
- **Gmailnator:** Se `docs/gmailnator_api.md` och `docs/gmailnator_usage.md`
- **Oxylabs:** Se `docs/oxlabs dokumentasjon.md`
- **2Captcha:** Dokumentation kommer

## Projektstatus
Se `docs/status.md` för detaljerad status och senaste uppdateringar.

## Utvecklingsregler

### Kodstruktur
- Håll ren och städad struktur
- Tester i `tests/` mappen
- All dokumentation i `docs/` mappen
- Ingen duplicerade filer (max en .bak-fil vid behov)
- Ta bort oanvända filer

### Kodkvalitet
- Kommentera kod logiskt och tydligt (Svenska eller Engelska)
- Modulär struktur - separera olika funktioner
- Ingen placeholder-kod - implementera komplett funktionalitet

### Obligatoriskt
- **Uppdatera `docs/status.md` efter VARJE ändring**
  - Vad som ändrades
  - Varför det ändrades
  - Aktuellt tillstånd
  - Nästa steg

## Bidra
1. Följ projektets regler ovan
2. Uppdatera `docs/status.md`
3. Kommentera kod tydligt
4. Testa din kod innan commit

## Licens
[Lägg till licensinformation här]
