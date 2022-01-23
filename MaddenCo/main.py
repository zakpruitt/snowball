
def parse_text(file_name):
    with open(file_name, 'w') as file:
        data = file.read()
        # parse data
        return data
        
if __name__ == '__main__':
    print(parse_text('maddenco_data.txt'))
    