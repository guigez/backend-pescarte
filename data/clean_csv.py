import csv

# Define the path to the original and new CSV files
input_csv_path = 'cities.csv'
output_csv_path = 'cities.csv'

# Define the columns you want to keep in the new CSV
columns_to_keep = ['Município', 'UF']


def clean_csv(input_path, output_path, columns):
    with open(input_path, mode='r', encoding='utf-8') as infile, \
         open(output_path, mode='w', encoding='utf-8', newline='') as outfile:

        # Create CSV reader and writer
        reader = csv.DictReader(infile, delimiter=';')
        writer = csv.DictWriter(outfile, fieldnames=columns)

        # Write the header to the new CSV
        writer.writeheader()

        # Iterate over each row in the original CSV
        for row in reader:
            # Filter the row to only include the columns you want to keep
            filtered_row = {column: row[column] for column in columns}
            # Write the filtered row to the new CSV
            writer.writerow(filtered_row)


def print_csv_columns(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        # Create a CSV DictReader
        reader = csv.DictReader(csvfile, delimiter=';')

        # Access the column names from the DictReader.fieldnames attribute
        columns = reader.fieldnames

        if columns:
            print("Column names in the CSV file:")
            for column in columns:
                print(column)
        else:
            print("No columns found.")


if __name__ == '__main__':
    # Run the function with your file paths and columns
    clean_csv(input_csv_path, output_csv_path, columns_to_keep)
    # print_csv_columns(input_csv_path)
