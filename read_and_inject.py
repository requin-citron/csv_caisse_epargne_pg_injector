from db_connect import insert_transaction
import csv

from datetime import datetime

def parse_date(date_str: str | None) -> datetime | None:
    """Parses a date string in DD/MM/YYYY format."""
    if date_str:
        try:
            return datetime.strptime(date_str, '%d/%m/%Y').date()
        except ValueError:
            return None
    return None

def convert_dict_to_transaction(row: dict) -> dict:
    """
    Convertit une ligne de CSV (sous forme de dictionnaire) en un dictionnaire de transaction.
    """
    return {
        'Date de comptabilisation': parse_date(row.get('Date de comptabilisation')),
        'Libelle simplifie': row.get('Libelle simplifie'),
        'Libelle operation': row.get('Libelle operation'),
        'Reference': row.get('Reference'),
        'Informations complementaires': row.get('Informations complementaires'),
        'Type operation': row.get('Type operation'),
        'Categorie': row.get('Categorie'),
        'Sous categorie': row.get('Sous categorie'),
        'Debit': float(row['Debit'].replace(',', '.')) if row.get('Debit') else None,
        'Credit': float(row['Credit'].replace(',', '.')) if row.get('Credit') else None,
        'Date operation': parse_date(row.get('Date operation')),
        'Date de valeur': parse_date(row.get('Date de valeur')),
        'Pointage operation': row.get('Pointage operation')
    }


# If your CSV has headers and you want to read it as a list of dictionaries:
def read_csv_as_dicts(file_path):
    """
    Reads a CSV file with headers into a list of dictionaries.
    """
    data = []
    with open(file_path, mode='r', encoding='utf-8', errors='ignore') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        for row in reader:
            data.append(convert_dict_to_transaction( dict(row) ))
    return data

for transaction in read_csv_as_dicts('./csv/bank.csv'):
    flag = insert_transaction(transaction)

    if flag == False:
        print("Erreur lors de l'insertion de la transaction :", transaction)