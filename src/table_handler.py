from models.call import Call

calls_db = Call()

class TableHandler:
    def __init__(self, start=None, end=None, sub_dept=None) -> None:
        self.totals = calls_db.get_total_immediate_and_later_counts(start, end, sub_dept)
        self.emp_totals = calls_db.get_immediate_and_later_count_per_employee(start, end, sub_dept)
        self.table = []

    def generate_table(self):
        # generate employee row
        for i in range(len(self.emp_totals)):
            row = []
            
            # self.totals[0] is the total number of calls
            # self.totals[1] is the total number of immediate
            # self.totals[2] is the total number of later

            # self.emp_totals[i][0] is the employee's name
            # self.emp_totals[i][1] is the employee's total count
            # self.emp_totals[i][2] is the employee's immediate count
            # self.emp_totals[i][3] is the employee's later count


            row.append(self.emp_totals[i][2])
            row.append(float(self.emp_totals[i][2]) / float(self.totals[1]))

            row.append(self.emp_totals[i][3])
            row.append(float(self.emp_totals[i][3]) / float(self.totals[2]))

            row.append(self.emp_totals[i][1])

            row.append(float(self.emp_totals[i][2]) / float(self.totals[0]))



    def get_new_immediate_column():
        pass
    

