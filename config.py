token = 'vk1.a.kNPB4DdK-yJVXRimG-A6RZ6xaMzaUt9inPbhiywknCv4q1l5SKBdh6Ir_srrvVi7mUP7JqTen5b8C5mRzvJqY1WyOAPO_R9Fi_PvOe_9dvdDoC-peeAGEg2HBKhbogUFGtR-2VxHeHGHwbzf6yvsNUG1VZ9BsDEXe3nDXGSPCQw0qaRXma1S8w3Vg55Rv9s-CuoBVbOZbM5BzNPdj7hZ4A'
weather_api_key = "467e9329e78d70b728147eb922f99675"
group_id = 'club220830792'

import re
def check_group_format(group_number):
    pattern = r'^[A-Za-zА-Яа-я]{4}-\d{2}-\d{2}$'
    match = re.match(pattern, group_number)
    if match:
        return not None
    else:
        return None


def check_proffesor_pattern(string):
    pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]\.$'
    match = re.match(pattern, string)
    if match:
        return True
    else:
        return False

