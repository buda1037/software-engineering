# Student Data Model

```mermaid
erDiagram
    STUDENT ||--|| ADDRESS : has
    STUDENT ||--o{ EXAM_RESULT : has
    STUDENT {
        int id PK
        string matriculation_number UK
        string? username UK
        string first_name
        string last_name
        Gender? gender
        date date_of_birth
        string email UK
        StudyProgram study_program
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
