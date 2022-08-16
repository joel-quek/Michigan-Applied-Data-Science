sales_record = {"Car model": "Toyota", "Owner": "James", "Price": 45000}

statement = "{} owns a car of {} make which costs ${}"

print(statement.format(sales_record['Owner'], sales_record['Car model'], sales_record['Price']))