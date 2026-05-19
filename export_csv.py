import csv
import datetime

def export_csv_file(export_list, code):
# 2 для рассылки писем, 1 для moodle
    if int(code) == 2:
        filename = 'export_csv/' + 'contact.csv'
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                ['firstname', 'username', 'password', 'email', 'start_date', 'end_date'])
            for listener in export_list:
                export_record = [listener.firstname, listener.username, listener.password, listener.email, listener.start_date, listener.end_date]

                writer.writerow(export_record)
        return filename

    date = datetime.date.today()
    filename = 'export_csv/' + str(date) + '_export.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['username', 'password', 'email', 'firstname', 'lastname', 'institution', 'phone1', 'course1',
                         'course2', 'course3', 'course4', 'course5', 'role1', 'role2', 'role3', 'role4', 'role5'])
        for listener in export_list:
            export_record = [listener.username, listener.password, listener.email, listener.firstname, listener.lastname, listener.institution, listener.phone]
            count = len(listener.programs)
            for program in listener.programs:
                export_record.append(program.id)

            for cell in range(5 - count):
                export_record.append('')

            for program in listener.programs:
                export_record.append('student')

            writer.writerow(export_record)
    return filename