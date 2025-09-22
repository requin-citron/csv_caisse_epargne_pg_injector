CREATE TABLE IF NOT EXISTS bank_transactions (
    id SERIAL PRIMARY KEY,
    date_comptabilisation DATE,
    libelle_simplifie TEXT DEFAULT '',
    libelle_operation TEXT DEFAULT '',
    reference TEXT DEFAULT '',
    information TEXT DEFAULT '',
    type_operation TEXT DEFAULT '',
    categorie TEXT DEFAULT '',
    sous_categorie TEXT DEFAULT '',
    debit NUMERIC DEFAULT 0,
    credit NUMERIC DEFAULT 0,
    date_operation DATE,
    date_de_valeur DATE,
    pointage_operation BOOLEAN DEFAULT FALSE
);