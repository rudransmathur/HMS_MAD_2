# Hospital Management System

To build a Hospital Management System (HMS) web application that allows Admins, Doctors, Patients to interact with the system based on their roles.
## Approach:
The Hospital Management System will be developed with Flask providing a secure REST API and VueJS handling all client-side interactions. SQLite will act as the primary database, created using SQL Alchemy models. Redis will be integrated for caching frequently accessed data, while Celery with Redis will handle background tasks such as sending reminders or generating reports. Role-based access control will ensure that Admins, Doctors, and Patients interact with the system according to permissions.
## Technologies and Frameworks Used
|Technology / Library|	Purpose|
|-|-|
|Flask|	Core backend web framework|
|SQAlchemy|	Object Relational Mapper for SQLite database|
|Bootstrap 5|	Frontend styling and responsive design|
|Flask-Login|	User authentication and session management|
|SQLite|	Lightweight local database for storing user data|
|Redis|	Caching|

## Database Schema / ER Diagram
**Tables:**
|Table|Description|
|-|-|
|User | Stores core account and authentication details|
|Role | Defines system roles (doctor, patient, admin…)|
|RolesUsers (Mapping Table)| Associates users and roles (many-to-many).|
|Patient | Stores patient-specific details.|
|Doctor | Stores doctor-specific profile.|
|DoctorAvailability | Stores weekly doctor timings.|
|Request | Stores user requests (e.g., profile update requests).|
|Appointment | Stores appointments between patients and doctors.|
|Treatment | Stores treatment session details.|

**Relationships:**
- One-to-Many → User → RolesUsers
- Many-to-Many → User ↔ Role (via RolesUsers)
- One-to-One → User → Patient
- One-to-One → User → Doctor
- One-to-Many → User → Request
- One-to-Many → User → DoctorAvailability

<img width="975" height="768" alt="image" src="https://github.com/user-attachments/assets/22ef6a10-c0e0-478c-a708-c9af66e1e4ff" />

## API Resource Endpoints
|Endpoint	|Method	|Description|
|-|-|-|
|/api/auth/login|	POST|	Authenticate user and generate session|
|/api/auth/register|	POST|	Register new User|
|/api/appointments	|GET, POST|	Use All Appointments|
|/api/appointment/id|	GET, PUT, PATCH, DELETE	|Use Appointment’s details|
|/api/treatments |GET, POST|	Use All Treatments|
|/api/treatment/id|	GET, PUT, PATCH, DELETE|	Use Treatment’s details|
|/api/ users	|GET, POST|	Use All Users|
|/api/ user/id|	GET, PUT, PATCH, DELETE	|Use User’s details|
|/api/ doctors|	GET, POST|	Use All Doctor Users|
|/api/ patients|	GET, POST|	Use All Patient Users|
|/api/ doctoravailability|	GET, POST|	Use All Doctor’s Availabilities|
|/api/ doctoravailability/id|	GET, PUT, PATCH, DELETE|	Use Doctor’s Availability’s details|
|/api/ requests| GET, PUT, PATCH, DELETE	|Use All Doctor Requests|
|/api/ request/id|	GET, PUT, PATCH, DELETE|	Use Doctor Request’s details|
