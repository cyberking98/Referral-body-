# Gmailnator (Emailnator) API - Temporär E-post Service

**Service URL:** https://www.emailnator.com (tidigare gmailnator.com)  
**API Host:** gmailnator.p.rapidapi.com  
**Protokoll:** HTTPS  
**Authentication:** RapidAPI headers

## API Credentials
```python
headers = {
    'x-rapidapi-key': "6d643ca1bcmshf82deca57766f56p1f67abjsn6e71bf12c68a",
    'x-rapidapi-host': "gmailnator.p.rapidapi.com"
}
```

## Översikt
Gmailnator är en avancerad temporär e-posttjänst som håller spam borta från din riktiga e-post. 
Tjänsten erbjuder möjlighet att använda riktiga Gmail-adresser för tillfällig kommunikation.

## Endpoints

### 1. Generera E-postadress
**Method:** POST  
**Endpoint:** `/generate-email`

**Parameters:**
- `options` (Array, Required): Välj en eller flera alternativ [1,2,3,4,5,6,8,9]
  - `1` - Generera public domain mail
  - `2` - Generera public Plus(+) Gmail
  - `3` - Generera public Dot(.) Gmail
  - `4` - Generera private domain mail
  - `5` - Generera private Plus(+) Gmail
  - `6` - Generera private Dot(.) Gmail
  - `8` - Generera public Googlemail
  - `9` - Generera private Googlemail

**Exempel:**
```python
import http.client
import json

conn = http.client.HTTPSConnection("gmailnator.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6d643ca1bcmshf82deca57766f56p1f67abjsn6e71bf12c68a",
    'x-rapidapi-host': "gmailnator.p.rapidapi.com",
    'Content-Type': 'application/json'
}

payload = json.dumps({"options": [1]})
conn.request("POST", "/generate-email", payload, headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

---

### 2. Generera Bulk E-postadresser
**Method:** POST  
**Endpoint:** `/bulk-emails`

**Parameters:**
- `limit` (Integer, Required): Antal e-postadresser att generera (max: 500)
- `option` (Array, Required): Välj en eller flera alternativ [1,2,3,4,5,6,8,9]
  - Samma alternativ som `/generate-email`

**Exempel:**
```python
import http.client
import json

conn = http.client.HTTPSConnection("gmailnator.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6d643ca1bcmshf82deca57766f56p1f67abjsn6e71bf12c68a",
    'x-rapidapi-host': "gmailnator.p.rapidapi.com",
    'Content-Type': 'application/json'
}

payload = json.dumps({
    "limit": 10,
    "option": [1, 2]
})
conn.request("POST", "/bulk-emails", payload, headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

---

### 3. Hämta Inbox (Meddelanden)
**Method:** POST  
**Endpoint:** `/inbox`

**Parameters:**
- `email` (String, Required): E-postadressen du vill hämta meddelanden från
- `limit` (Integer, Optional): Antal meddelanden att hämta (max: 20)

**Exempel:**
```python
import http.client
import json

conn = http.client.HTTPSConnection("gmailnator.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6d643ca1bcmshf82deca57766f56p1f67abjsn6e71bf12c68a",
    'x-rapidapi-host': "gmailnator.p.rapidapi.com",
    'Content-Type': 'application/json'
}

payload = json.dumps({
    "email": "example@gmail.com",
    "limit": 10
})
conn.request("POST", "/inbox", payload, headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

---

### 4. Hämta Enskilt Meddelande
**Method:** GET  
**Endpoint:** `/messageid`

**Parameters:**
- `id` (String, Required): Unikt ID för meddelandet du vill hämta

**Exempel:**
```python
import http.client

conn = http.client.HTTPSConnection("gmailnator.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6d643ca1bcmshf82deca57766f56p1f67abjsn6e71bf12c68a",
    'x-rapidapi-host': "gmailnator.p.rapidapi.com"
}

message_id = "eyJpdiI6IlhtajhrNmFsL045Ni9JTjBSUzhwYWc9PSI..."
conn.request("GET", f"/messageid?id={message_id}", headers=headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

---

### 5. Radera Meddelande
**Method:** GET  
**Endpoint:** `/delete`

**Parameters:**
- `id` (String, Required): Unikt ID för meddelandet du vill radera

**Exempel:**
```python
import http.client

conn = http.client.HTTPSConnection("gmailnator.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6d643ca1bcmshf82deca57766f56p1f67abjsn6e71bf12c68a",
    'x-rapidapi-host': "gmailnator.p.rapidapi.com"
}

message_id = "eyJpdiI6IlhtajhrNmFsL045Ni9JTjBSUzhwYWc9PSI..."
conn.request("GET", f"/delete?id={message_id}", headers=headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

---

## Användningsscenario för Projektet

### Typiskt Workflow:
1. **Generera temporär e-post** - Använd `/generate-email` med option `[1]` för public domain
2. **Använd e-posten** - Registrera konto på målplattformen med den genererade e-postadressen
3. **Vänta på verifieringsmail** - Polling mot `/inbox` med den genererade e-postadressen
4. **Hämta verifieringslänk** - Använd `/messageid` för att få fullständigt innehåll
5. **Rensa upp** - Radera meddelandet med `/delete` efter användning

### Integration med Playwright:
```python
# 1. Generera e-post
email = generate_email_via_api(option=[1])

# 2. Fyll i registreringsformulär
await page.fill('input[name="email"]', email)
await page.click('button[type="submit"]')

# 3. Vänta och hämta verifieringsmail
await asyncio.sleep(5)  # Vänta på att mail ska komma
messages = get_inbox(email, limit=1)

# 4. Extrahera verifieringslänk från meddelande
message_content = get_message_by_id(messages[0]['id'])
verification_url = extract_verification_link(message_content)

# 5. Navigera till verifieringslänken
await page.goto(verification_url)
```

## API Rate Limits & Plans

**BASIC Plan (Current):** $0.00/mo  
**PRO Plan:** $19.99/mo  
**ULTRA Plan:** $49.99/mo  
**MEGA Plan:** $99.99/mo  

## Begränsningar
- Max 500 e-postadresser per bulk-generering
- Max 20 meddelanden per inbox-hämtning
- Option 7 (Generate private Real Gmail) är inaktiverad/borttagen

## Viktiga Noteringar
- ID:n för meddelanden är krypterade strängar (JWT-liknande format)
- Använd alltid `Content-Type: application/json` för POST-förfrågningar
- API:et körs via RapidAPI - kräver RapidAPI-specifika headers
- Emailnator.com är den nya domänen (gmailnator.com är föråldrad)
