import json
from datetime import date
from typing import Dict, Any, List
from App.dto.course.Course import Course
from App.dto.course.DesignCourse import DesignCourse
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.course.ScienceCourse import ScienceCourse
from App.dto.Platform import Platform
from App.dto.Address import Address

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

def date_hook(json_dict: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in json_dict.items():
        if isinstance(value, str):
            try:
                json_dict[key] = date.fromisoformat(value)
            except (ValueError, TypeError):
                pass
    return json_dict

def save_to_file(data: Any, filename: str) -> None:
    """Сохраняет данные в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, cls=CustomJSONEncoder, ensure_ascii=False, indent=2)

def load_from_file(filename: str) -> Any:
    """Загружает данные из JSON файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f, object_hook=date_hook)