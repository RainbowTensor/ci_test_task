import argparse

from database.importer.csv_importer import CsvImporter


parser = argparse.ArgumentParser(
    description="import cav file into database")
parser.add_argument("--csv_path", required=True,
                    help="csv file containng data to import")
parser.add_argument("--table", required=False, default="players",
                    help="table name in which to import")

if __name__ == "__main__":
    args = parser.parse_args()
    importer = CsvImporter(args.csv_path, args.table)
    importer.import_csv()

