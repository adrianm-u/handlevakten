# handlevakten

Handlevakten er en webapplikasjon under utvikling i emnet DAT130 Webprogrammering og
Databaser. Applikasjonen er bygget med Flask og MySQL på backend, og HTML, CSS og
JavaScript på frontend. Målet er å la brukere søke, filtrere og sammenligne priser på
dagligvarer ved hjelp av kassal.app API, samt opprette konto og lagre ønskelister.

## Funksjonalitet

- Viser produkter og priser fra Kassal API.
- Synkroniserer produkter, butikker og priser til en lokal MySQL-database.
- Lar brukere registrere seg og logge inn.
- Har grunnlag for ønskelister og produktdetaljer.

## Databaseoppsett

Prosjektet bruker databasen `handlevaktenDB`. Tabellen og relasjonene opprettes med filen
`database/schema.sql`.

Kjør denne kommandoen i terminalen for å opprette databasen og tabellene:

```bash
mysql -u root -p < database/schema.sql
```

Dette oppretter blant annet tabellene for:

- `users`
- `products`
- `stores`
- `prices`
- `price_history`
- `wishlist`
- `wishlist_items`
- `allergens`
- `product_allergens`

## Synkronisering av produkter

Når databasen er opprettet, kan du fylle den med produktdata fra Kassal API ved å kjøre
Flask-kommandoen `sync-products`.

```bash
flask sync-products
```

Kommandoen gjør følgende:

1. Leser produkter side for side fra Kassal API.
3. Lagrer eller oppdaterer produktinformasjon i `products`.
4. Lagrer eller oppdaterer butikkdata i `stores`.
5. Lagrer prisinformasjon i `prices`.

## Kjøring lokalt

Før du kjører appen må du ha:

- en aktiv MySQL-server
- opprettet databasen med `database/schema.sql`
- installert prosjektets avhengigheter

Start deretter Flask-appen med:

```bash
flask run
```

## Kommentar om databasen

I `app.py` er databaseinnstillingene satt direkte i koden. Hvis du bruker et annet
brukernavn, passord eller databasenavn lokalt, må disse verdiene oppdateres der.
