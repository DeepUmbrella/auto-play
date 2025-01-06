from .skill_area import Skill

initData = {
    'skillList': [
        {
            'id': 'skill1',
            'range': [100, 100],
            'releaseQuickKeyboard': 'a',
            'compositionKeyboards': '',
            'coolTime': 5,
            'level': 1
        },
        {
            'id': 'skill2',
            'range': [200, 200],
            'releaseQuickKeyboard': 'b',
            'compositionKeyboards': '',
            'coolTime': 3,
            'level': 2
        }
    ]
}


class DnfRole:
    def __init__(self, role_id):
        self.self_pos = [0, 0, 0, 0]
        self.skill_list = []
        self.role_id = role_id
        self.direction = 'R'

        # Assuming initData.skillList is provided externally
        for item in initData['skillList']:
            skill = Skill(
                id=item['id'],
                range=item['range'],
                release_quick_keyboard=item.get('releaseQuickKeyboard', 'x'),
                composition_keyboards=item.get('compositionKeyboards', ''),
                cool_time=item.get('coolTime', 0),
                level=item.get('level', 0)
            )
            self.skill_list.append(skill)

    def update_pos(self, x, y, x1, y1):
        self.self_pos = [x, y, x1, y1]
