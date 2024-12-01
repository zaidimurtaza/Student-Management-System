# Student Management System

The **Student Management System** is a FastAPI-based RESTful API for managing student records, using MongoDB as the database. It provides endpoints for creating, retrieving, updating, and deleting student information, making it suitable for educational institutions or related applications.

## Features

- **Create**: Add new student records with details such as name, age, and address.
- **Retrieve**:
  - List all students.
  - Fetch a specific student by their unique ID.
  - Filter students by country or age.
- **Update**: Modify specific fields of a student's record.
- **Delete**: Remove a student from the database.
- **Health Check**: Basic endpoints to test the service.

## Tech Stack

- **Backend**: FastAPI
- **Database**: MongoDB (via Motor, an asynchronous driver)
- **Deployment**: PythonAnywhere (or local execution)

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB instance (local or cloud-based)
- `pip` for dependency management

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/zaidimurtaza/Student-Management-System.git
   cd Student-Management-System
