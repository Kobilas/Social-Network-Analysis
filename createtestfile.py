import csv

with open('twitter_combined.txt', 'r') as read_csv:
    csv_reader = csv.reader(read_csv, delimiter=' ')
    with open('test.txt', 'w+', newline='') as write_csv:
        csv_writer = csv.writer(write_csv, delimiter=' ')
        i = 0
        for row in csv_reader:
            if i >= 100000:
                csv_writer.writerow(row)
            i += 1