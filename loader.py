import csv
from io import TextIOWrapper


def load_data(csv_file):
    import_list = []

    # Чтение данных из CSV файла и запись их в базу данных
    csv_file = TextIOWrapper(csv_file)
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)  # Пропускаем заголовок, если он есть в CSV файле
    for row in csv_reader:

        listener_data = []
        program_data = []

        for col in range(0, 10):
            listener_data.append(row[col])

        for col in range(10, 34):
            if row[col] == 'Да':
                program_data.append(col - 9)

        if len(listener_data[7]) > 250:
            listener_data[7] = listener_data[7][:250]
        if len(program_data[9]) > 250:
            program_data[9] = program_data[9][:250]
        import_list.append([listener_data, program_data])

    return import_list