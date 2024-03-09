from helper.fetchTemplates import fetch_template

class RouterTemplate():
    condition: str

    def __init__(self, condition:str) -> None:
        self.condition = condition

    nurse_template = fetch_template('nurse_template')
    pharmacist_template = fetch_template('pharmacist_template')
    dietician_template = fetch_template('dietician_template')
    psychologist_template = fetch_template('psychologist_template')


    prompt_infos = [
            {
                'name': 'nurse',
                'description': 'Best for patient condition education/awarness, preliminary assistance and general doubts about the condition',
                'prompt_template': nurse_template
            },
            {
                'name': 'pharmacist',
                'description': 'Best for questions related to prescribing general medications or clarifying doubts about medication regarding our condition only',
                'prompt_template': pharmacist_template
            },
            {
                'name': 'dietician',
                'description': 'Good for qeustions related to diet, portion control, meal planning, nutrition and lifestyle doubts regarding our condition only',
                'prompt_template': dietician_template
            },
            {
                'name': 'psychologist',
                'description': 'Good for questions which are inclined towards assisting human behaviour, emotions or help in adjusting to a our condition',
                'prompt_template': psychologist_template
            }
        ]
     
