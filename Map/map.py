people = ['Dr. Christopher Brooks', 'Dr. Kevyn Collins-Thompson', 'Dr. VG Vinod Vydiswaran', 'Dr. Daniel Romero']

def split_title_and_name(person):
    name_list = []
    for i in person:
        title = i.split()[0]
        last_name = i.split()[-1]
        name_list.append(title + " " + last_name)
    return name_list

print(split_title_and_name(people))
