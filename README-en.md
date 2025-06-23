# Demand Analysis

## 1\. Functional requirements

This system is mainly for teachers and students in school, providing a platform for online questions, answers, and interactive communication. The main functions include:

1.  **User Modules**
    *   User registration, login, logout (supports registration by email or student ID)
    *   User profile management (avatar, nickname, profile, major, grade, etc.)
    *   Forgot password and password modification function
2.  **Issue Management Module**
    *   User posts questions (title, body, add tags)
    *   Users browse the question list and support filtering by time, popularity, and tags
    *   View question details, including answers and comment lists
    *   Edit and delete your own questions
    *   Support Questions Posted Anonymously
3.  **Answer Management Module**
    *   User answers to questions
    *   Like and comment on the answer
    *   The question poster can select the best answer
    *   Users can delete their own answers
4.  **Tag management module**
    *   When asking a question, you can select an existing tag or create a new tag
    *   Support browsing questions by tag classification
5.  **Interaction and notification module**
    *   Like reminder, answer notification, comment notification
    *   My Questions/My Answers List Page
6.  **Search function module**
    *   Support keyword search for question title and text
    *   Support filtering questions by tags
7.  **Points and level system (optional)**
    *   Users earn points by asking questions, answering, and being liked.
    *   Improve your level based on points and encourage activity
8.  **Backstage management module**
    *   Administrators can manage users, questions, answers, and report information
    *   Support review and deletion of illegal content

## 2\. Non-functional requirements

*   **System availability**
    *   The system should support the basic access needs of at least 500 concurrent online users.
*   **Response speed**
    *   The page loading time is controlled within 3 seconds, and the response time for common operations is less than 1 second.
*   **Security**
    *   Prevent SQL injection, XSS attacks, and encrypt password storage.
    *   User data protection, hiding user identity information when asking questions anonymously.
*   **Scalability**
    *   The system module design should have good scalability to support the addition of new functions such as course Q&A and information sharing in the future.
*   **compatibility**
    *   Supports access from mainstream browsers and is compatible with mobile display (responsive layout).

# Core data table design

1.  **User table (** You can use Django's own `AbstractUser` extension)

*   id (primary key)
*   username
*   email
*   password
*   avatar
*   bio
*   major
*   grade
*   is\_active (whether activated)
*   date\_joined (registration time)
*   score (score, used for point system, optional)

1.  **Question**

*   id (primary key)
*   author (outside key -> User)
*   title
*   content (main text, supports rich text)
*   is\_anonymous (whether to publish anonymously)
*   created\_at (creation time)
*   updated\_at
*   view\_count
*   like\_count (number of likes)

1.  **Answer**

*   id (primary key)
*   question (outside key -> Question)
*   author (outside key -> User)
*   content (the body of the answer)
*   is\_accepted (whether it is adopted)
*   created\_at (creation time)
*   updated\_at
*   like\_count (number of likes)

1.  **Comment form** (Both questions and answers can have comments, so a general Comment is needed)

*   id (primary key)
*   content\_type (indicates whether it is a question or answer for a comment, using Django's ContentType)
*   object\_id (corresponding to question ID or answer ID)
*   author (outside key -> User)
*   content
*   created\_at (creation time)

1.  **Tag table**

*   id (primary key)
*   name (tag name)
*   created\_at (creation time)

1.  **Question-tag association table (QuestionTag)**

*   id (primary key)
*   question (outside key -> Question)
*   tag (foreign key -> Tag)

1.  **Notification**

*   id (primary key)
*   receiver (outside key -> User)
*   sender (foreign key -> User, who triggered it)
*   content (notification content, such as: "Your question has a new answer")
*   is\_read (read or not)
*   created\_at (creation time)

* * *

# Entity Relationship (ER Relationship)

*   A user can post multiple questions (User — 1:N — Question)
*   A question can have multiple answers (Question — 1:N — Answer)
*   A question can have multiple tags (Question — N:M — Tag)
*   One answer can only belong to one question
*   A user can like a question or answer (this can be done by adding an additional Like table)
*   A user can receive multiple notifications

In our campus question-and-answer system, the core of the ER diagram revolves around: **users** , **questions** , **answers** , **tags** , **comments** , and **notifications** .

* * *

```
[User] ——<release>—— [Question] ——<Relationship>—— [Tag]
   |                    |
   |                    └——<have>—— [Answer]
   |                                   |
   |                                   └——<have>—— [Comment]
   |
   └——<release>—— [Comment]

[User] ——<trigger>—— [Notification]
```

### 1\. User table

| Fields | type | illustrate |
| --- | --- | --- |
| id | Primary Key | Automatically generate |
| username | String | username |
| email | String | Mail |
| password | String | Password (hashed) |
| avatar | picture | avatar |
| bio | text | Introduction |
| major | String | major |
| grade | String | grade |
| score | Integer | integral |
| date\_joined | time | Registration Time |

### 2\. Question

| Fields | type | illustrate |
| --- | --- | --- |
| id | Primary Key |  |
| title | String | Question Title |
| content | Rich Text | Question content |
| is\_anonymous | Boolean | Anonymous |
| author\_id | Foreign Key -> User | Questioner |
| created\_at | time | Creation time |
| updated\_at | time | Update time |
| view\_count | Integer | Views |
| like\_count | Integer | Likes |

### 3\. Answer

| Fields | type | illustrate |
| --- | --- | --- |
| id | Primary Key |  |
| question\_id | Outside key -> Question | The problem |
| author\_id | Foreign Key -> User | Respondent |
| content | Rich Text | Answer content |
| is\_accepted | Boolean | Whether it is adopted |
| created\_at | time | Creation time |
| updated\_at | time | Update time |
| like\_count | Integer | Likes |

### 4\. Tag table

| Fields | type | illustrate |
| --- | --- | --- |
| id | Primary Key |  |
| name | String | Tag Name |
| created\_at | time | Creation time |

### 5\. QuestionTag question and tag association table

| Fields | type | illustrate |
| --- | --- | --- |
| id | Primary Key |  |
| question\_id | ForeignKey -> Question |  |
| tag\_id | Foreign Key -> Tag |  |

### 6\. Comment

| Fields | type | illustrate |
| --- | --- | --- |
| id | Primary Key |  |
| content\_type | ContentType | Related to question or answer |
| object\_id | Integer | Link ID |
| author\_id | Foreign Key -> User | Commentator |
| content | text | Comments |
| created\_at | time | Creation time |

### 7\. Notification 

| Fields | type | illustrate |
| --- | --- | --- |
| id | Primary Key |  |
| receiver\_id | Foreign Key -> User | Notification Recipients |
| sender\_id | Foreign Key -> User | Notification originator |
| content | text | Notification content |
| is\_read | Boolean | Have you read it? |
| created\_at | time | Creation time |

# Project Structure

```csharp
campusqa/                      # The root directory created by PyCharm
│
├── campusqa/                 # Main configuration directory（settings.py / urls.py）
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                     # All sub-functional modules app
│   ├── user/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│   │
│   ├── question/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│   │
│   ├── answer/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│   │
│   ├── comment/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
    
│   ├── tag/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
    
│   └── notification/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│
├── templates/                # Global template
│   └── base.html
│
├── static/                   # Static resource directory
│   ├── css/
│   │   └── style.css
│   └── images/
│   │   └── default_avatar.png
│
├── media/                    # User uploaded files, such as avatars
│   ├── avatars/
│
├── manage.py
└── requirements.txt          # Project Dependencies

```
