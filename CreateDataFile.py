import pandas as pd

data = []
stop = False
while stop is False:
    check_input = False
    while check_input is False:
        element = input('Name des Elements (z.B. Fe)\n')
        edge = float(input(f'Wo liegt die Edge von {element}?\n'))
        reference_points = []
        more_ref = True
        while more_ref is True:
            ref = input(f'Wo liegt der Referenz-Punkte von {element}?\n'
                        f'Falls es keinen weiteren mehr gibt, dann bitte 0 '
                        f'eingeben.\n')
            if ref == '0':
                more_ref = False
            elif ref == '':
                more_ref = True
            else:
                reference_points.append(float(ref))

        datapoint = {'name': element, 'edge': edge, 'ref': reference_points}
        correct_input = False
        while correct_input is False:
            correct = input(f'Stimmen die Eingaben (y/n)?\n{datapoint}\n')
            if correct == 'y':
                check_input = True
                correct_input = True
            elif correct == 'n':
                check_input = False
                correct_input = True
            else:
                print('Bitte y für ja und n für nein eingen.')
        check_more = False
        while check_more is False:
            more_elements = input('Gibt es weitere Elemente?\n')
            if more_elements == 'y':
                check_more = True
            elif more_elements == 'n':
                check_more = True
                stop = True
            else:
                print('Bitte y für ja und n für nein eingen.')
    data.append(datapoint)
    df = pd.DataFrame(data)
    df.to_csv('HephaestusData_NEW.csv')

print(df)
