import csv


def create_logs_csv():
    with open('../  logs/logs.csv', 'w') as csv_file:
        header = ['file_name', 'status']
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(header)


def append_logs_to_csv(file_name, status):
    with open('../logs/log.csv', 'a') as csf_file:
        csvwriter = csv.writer(csf_file)
        file_metadata = [file_name, status]
        csvwriter.writerow(file_metadata)

