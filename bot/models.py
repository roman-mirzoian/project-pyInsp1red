# всі структури даних (Field, Record і так далі)
from collections import UserDict, defaultdict

class Notes(UserDict):
    def add_note(self, user_name: str, note: str):
        user_notes = self.data.setdefault(user_name, {})
        if user_notes:
            max_id = max(int(k) for k in user_notes.keys())
            note_id = str(max_id + 1)
        else:
            note_id = "1"

        user_notes[note_id] = note
        return note_id

    def edit_note(self):
        pass

    def get_all_user_notes(self, user_name: str) -> dict:
        return self.data.get(user_name, {})

    def find_notes(self, note_text: str) -> dict:
        result = defaultdict(list)

        for user_name, notes in self.data.items():
            for id, text in notes.items():
                if note_text in text:
                    result[user_name].append({"id": id, "text": text})

        return dict(result)

    def delete_note(self, user_name: str, note_id: str):
        if user_name in self.data and note_id in self.data[user_name]:
            del self.data[user_name][note_id]
            return True
        
        return False