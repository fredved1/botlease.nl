# Vercel Database Setup voor BotLease Contact Form

## Stappen om Vercel Postgres in te stellen:

### 1. Deploy naar Vercel
```bash
# Installeer Vercel CLI als je die nog niet hebt
npm i -g vercel

# Deploy het project
vercel
```

### 2. Maak Vercel Postgres Database
1. Ga naar je Vercel dashboard
2. Selecteer je project
3. Ga naar "Storage" tab
4. Klik op "Create Database"
5. Kies "Postgres"
6. Geef het een naam (bijv. "botlease-contacts")
7. Klik op "Create"

### 3. Maak de contacts tabel
In Vercel dashboard, ga naar je database en klik op "Query":

```sql
CREATE TABLE contacts (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  company VARCHAR(255),
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(50) DEFAULT 'new',
  notes TEXT
);

-- Index voor snellere queries
CREATE INDEX idx_contacts_email ON contacts(email);
CREATE INDEX idx_contacts_created_at ON contacts(created_at);
```

### 4. Update de API route
In `api/contact.js`, uncomment het Vercel Postgres gedeelte:

```javascript
import { sql } from '@vercel/postgres';

// In de handler function:
const { rows } = await sql`
  INSERT INTO contacts (name, email, phone, company, message)
  VALUES (${name}, ${email}, ${phone}, ${company}, ${message})
  RETURNING id
`;
```

### 5. Installeer dependencies
```bash
npm install @vercel/postgres
```

### 6. Environment Variables
Vercel voegt automatisch deze env vars toe:
- `POSTGRES_URL`
- `POSTGRES_PRISMA_URL`
- `POSTGRES_URL_NON_POOLING`
- `POSTGRES_USER`
- `POSTGRES_HOST`
- `POSTGRES_PASSWORD`
- `POSTGRES_DATABASE`

### 7. Bekijk submissions in Vercel Dashboard
1. Ga naar Storage → je database
2. Klik op "Data" tab
3. Hier zie je alle contact form submissions

### 8. Update de frontend JavaScript
In `index.html`, vervang het localStorage gedeelte met:

```javascript
const response = await fetch('/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
});

const result = await response.json();

if (!response.ok) {
    throw new Error(result.error || 'Submission failed');
}
```

## Lokaal testen

Voor lokaal development, gebruik:
```bash
vercel env pull .env.local
vercel dev
```

Dit haalt de database credentials op en start een lokale development server.

## Extra: Email notificaties

Je kunt ook email notificaties toevoegen met Vercel's email service:

```javascript
// In api/contact.js
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'BotLease <noreply@botlease.nl>',
  to: 'thomas@botlease.nl',
  subject: 'Nieuwe contact aanvraag',
  html: `
    <h2>Nieuwe aanvraag van ${name}</h2>
    <p><strong>Email:</strong> ${email}</p>
    <p><strong>Bedrijf:</strong> ${company}</p>
    <p><strong>Bericht:</strong> ${message}</p>
  `
});
```