from db import get_preference_summary
from db import get_preference_text


print(get_preference_text())

prefs = get_preference_summary()
print("Applied:", prefs["applied"])
print("Rejected:", prefs["rejected"])