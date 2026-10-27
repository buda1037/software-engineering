# Student Data Model

```mermaid
erDiagram
    STUDENT ||--|| ADDRESS : has
    STUDENT ||--o{ EXAM_RESULT : has
    STUDENT {
        int id PK
        string matriculation_number UK "search"
        string? username UK
        string first_name
        string last_name "search"
        Gender? gender
        date date_of_birth
        string email UK "search"
        StudyProgram study_program "search"
        date enrollment_date
    }
    ADDRESS {
        int id PK
        int student_id FK, UK
        string street
        string house_number
        string postal_code
        string city
    }
    EXAM_RESULT {
        int id PK
        int student_id FK
        string module
        decimal grade
        int ects
        date exam_date
    }
```
