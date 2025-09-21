from App.dto.course.ScienceCourse import ScienceCourse
from App.dto.course.ProgrammingCourse import ProgrammingCourse
from App.dto.course.DesignCourse import DesignCourse
from datetime import date
from typing import List

class CourseFactory:
    @staticmethod
    def create_course(course_type: str, title: str, start_date: date, end_date: date, instructor: str, students: List[str], topics: List[str], **kwargs):
        if course_type == "programming":
            languages = kwargs.get("languages", ["Python", "Java"])
            return ProgrammingCourse(title, start_date, end_date, instructor, students, topics, languages)
        elif course_type == "design":
            tools = kwargs.get("tools", ["Figma", "Photoshop"])
            return DesignCourse(title, start_date, end_date, instructor, students, topics, tools)
        elif course_type == "science":
            field = kwargs.get("field", ["Physics", "Mathematics"])
            return ScienceCourse(title, start_date, end_date, instructor, students, topics, field)
        else:
            return ValueError(f"Неизвестный тип курса: {course_type}")

    @staticmethod
    def from_dict(data: dict):
        course_type = data.get('type', '').lower()
        
        if 'programming' in course_type:
            return ProgrammingCourse.from_dict(data)
        elif 'design' in course_type:
            return DesignCourse.from_dict(data)
        elif 'science' in course_type:
            return ScienceCourse.from_dict(data)
        else:
            if 'languages' in data:
                return ProgrammingCourse.from_dict(data)
            elif 'tools' in data:
                return DesignCourse.from_dict(data)
            elif 'field' in data:
                return ScienceCourse.from_dict(data)
            else:
                from App.dto.course.Course import Course
                return Course.from_dict(data)