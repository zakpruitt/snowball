from models.call import Call

calls_db = Call()

class TableHandler:
    def __init__(self, start=None, end=None, sub_dept=None) -> None:
        self.call_totals = calls_db.get_total_immediate_and_later_counts(start, end, sub_dept)
        self.emp_call_totals = calls_db.get_immediate_and_later_count_per_employee(start, end, sub_dept)
        self.email_totals = calls_db.get_total_email_counts(start, end, sub_dept)
        self.emp_email_totals = calls_db.get_email_counts_per_employee(start, end, sub_dept)
        self.table = []

    def generate_table(self):
        for i in range(len(self.emp_call_totals)):
            # region DF Anatomy
            
            # self.calls_totals[0][0] is the total number of calls
            # self.calls_totals[0][1] is the total number of immediate
            # self.calls_totals[0][2] is the total number of later

            # self.emp_calls_totals[i][0] is the employee's name
            # self.emp_calls_totals[i][1] is the employee's total count
            # self.emp_calls_totals[i][2] is the employee's immediate count
            # self.emp_calls_totals[i][3] is the employee's later count

            # self.emp_emails_totals[i][0] is the employee's name
            # self.emp_emails_totals[i][1] is the employee's total count

            # self.emails_totals[0][0] is the total number of emails

            # row[0] = name
            # row[1] = new immediate
            # row[2] = new immediate percentage
            # row[3] = new later
            # row[4] = new later percentage
            # row[5] = calls total for emp
            # row[6] = immediate total percentage
            # row[7] = email total for emp
            # row[8] = total new for emp (total calls + total emails) (row[5] + row[7])
            # row[9] = support % (row[8] / total calls + total emails for all employees)
            # row[10] = immediate % (row[1] / row[8])
            # row[11] = late % (row[3] / row[8])
            # row[12] = email % (row[7] / row[8])

            # endregion
            
            # Initialize the row
            row = []

            # Add call related data
            row.append(self.emp_call_totals[i][0]) # 0
            row.append(self.emp_call_totals[i][2]) # 1
            row.append(float(self.emp_call_totals[i][2]) / float(self.call_totals[0][1])) # 2
            row.append(self.emp_call_totals[i][3]) # 3
            row.append(float(self.emp_call_totals[i][3]) / float(self.call_totals[0][2])) # 4
            row.append(self.emp_call_totals[i][1]) # 5
            row.append(float(self.emp_call_totals[i][2]) / float(self.call_totals[0][0])) # 6
            
            # Add email related data
            email_tuple = self.__get_email_tuple(self.emp_call_totals[i][0])
            row.append(email_tuple[1]) # 7
            
            # Add aggregated related data
            row.append(row[5] + row[7]) # 8
            row.append(row[8] / (float(self.call_totals[0][0]) + float(self.email_totals[0][0]))) # 9
            row.append(row[1] / row[8]) # 10
            row.append(row[3] / row[8]) # 11
            row.append(row[7] / row[8]) # 12

            # Add row to table
            self.table.append(row)
    
    def __get_email_tuple(self, name):
        for tuple in self.emp_email_totals:
            if tuple[0] == name:
                return tuple

    def print_table(self):
        for row in self.table:
            print("Person: " + row[0])
            print("New Immediate: " + str(row[1]))
            print("New Immediate Percentage: " + str(row[2]))
            print("New Later: " + str(row[3]))
            print("New Later Percentage: " + str(row[4]))
            print("Total: " + str(row[5]))
            print("Immediate Total Percentage: " + str(row[6]))
            print("\n")

