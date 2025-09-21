import json
from datetime import date
from typing import Dict, Any, List, Type
from App.dto.course.Course import Course
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.course.DesignCourse import DesignCourse
from App.dto.course.ScienceCourse import ScienceCourse
from App.dto.Platform import Platform
from App.dto.Address import Address

class JSONSerializer:
    @staticmethod
    def serialize(obj: Any) -> str:
        """Сериализует объект в JSON строку"""
        if hasattr(obj, 'to_dict'):
            return json.dumps(obj.to_dict(), ensure_ascii=False, indent=2, cls=DateTimeEncoder)
        elif isinstance(obj, (list, tuple)):
            return json.dumps([item.to_dict() if hasattr(item, 'to_dict') else item for item in obj], 
                             ensure_ascii=False, indent=2, cls=DateTimeEncoder)
        else:
            raise ValueError(f"Неподдерживаемый тип для сериализации: {type(obj)}")

    @staticmethod
    def deserialize(json_str: str, target_type: Type = None) -> Any:
        """Десериализует JSON строку в объект"""
        data = json.loads(json_str)
        
        if target_type:
            if target_type == Platform:
                return Platform.from_dict(data)
            elif target_type == Address:
                return Address.from_dict(data)
            elif target_type in [Course, ProgrammingCourse, DesignCourse, ScienceCourse]:
                return JSONSerializer._create_course_from_dict(data)
            elif target_type == list:
                return [JSONSerializer._create_course_from_dict(item) for item in data]
        
        # Автоматическое определение типа
        if isinstance(data, list) and data and isinstance(data[0], dict) and 'type' in data[0]:
            return [JSONSerializer._create_course_from_dict(item) for item in data]
        elif isinstance(data, dict):
            if 'type' in data:
                return JSONSerializer._create_course_from_dict(data)
            elif 'name' in data and 'address' in data:
                return Platform.from_dict(data)
            elif 'domain' in data and 'url' in data:
                return Address.from_dict(data)
        
        return data

    @staticmethod
    def _create_course_from_dict(data: Dict[str, Any]) -> Course:
        """Создает конкретный экземпляр курса на основе типа"""
        course_type = data.get('type', 'Course')
        
        course_classes = {
            'ProgrammingCourse': ProgrammingCourse,
            'DesignCourse': DesignCourse,
            'ScienceCourse': ScienceCourse
        }
        
        if course_type in course_classes:
            return course_classes[course_type].from_dict(data)
        else:
            raise ValueError(f"Неизвестный тип курса: {course_type}")

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)