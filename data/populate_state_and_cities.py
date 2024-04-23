import csv
import uuid
from sqlalchemy.orm import Session
from src.database import Session
from src.models.uf import UF
from src.models.municipality import Municipality


def populate_states(states_csv_path):
    db: Session = Session()
    with open(states_csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f'Adding state {row["UF"]}')
            state = UF(uf_name=row['Estado'], uf=row['UF'])
            success, error = state.save(db)

            if success:
                print(f'State {row["UF"]} with success')
            else:
                print(f'Error adding {row["UF"]}. Error: {error}')


def populate_cities(cities_csv_path):
    db: Session = Session()
    with open(cities_csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f'Adding cidade {row["Município"]}')
            uf = db.query(UF).filter_by(uf=row['UF']).first()
            if uf:
                city = Municipality(id=uuid.uuid4(), name=row['Município'], uf=uf.uf)
                success, error = city.save(db)

                if success:
                    print(f'State {row["Município"]} with success')
                else:
                    print(f'Error adding {row["Município"]}. Error: {error}')


if __name__ == '__main__':
    states_csv_path = 'states.csv'  # Update with the path to your states CSV file
    cities_csv_path = 'cities.csv'  # Update with the path to your cities CSV file

    populate_states(states_csv_path)
    populate_cities(cities_csv_path)
