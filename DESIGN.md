Overview

This project is a fully GUI-based gym management application created using Python, Tkinter, and SQLite.
The system supports two types of users:
	•	Members – can check in, view membership info, and change their membership.
	•	Staff / Managers – can manage members, staff, and class schedules.

The system uses a window-based navigation model and a modular code structure that separates each major feature into its own file.

⸻

System Architecture

The application follows a multi-window Tkinter architecture, where each major feature opens as a new Toplevel window. SQLite databases store user information.

Key Components

main.py: Landing screen for starting as member or staff
login.py: Staff login & member check-in system
main_page.py: Core dashboard for both members and staff
members.py: Add, edit, remove members (staff only)
staff.py: Add, edit, remove staff (manager only)
schedules.py: Create or view class schedules
members.db: Stores all member data
staff.db: Stores all staff profiles

The system uses a controller-style flow:
	1.	User selects role
	2.	Login window opens
	3.	A dashboard loads based on user type
	4.	Specific management windows can be opened from the dashboard

Major Classes

GymInterface (main_page.py)

This is the central controller for the application.
	•	Loads staff dashboard or member dashboard based on login result
	•	Handles navigation between windows
	•	Manages the member inactivity timeout
	•	Provides access to member and staff management features

EditMembershipWindow

A popup that allows members to change their membership type.
It updates only the membership column in the database.

Members (members.py)

GUI used by staff to:
	•	Add new members
	•	Edit existing members
	•	Remove members
	•	Search through members using a smart search bar

Staff (staff.py)

Manager-only interface for:
	•	Adding staff
	•	Editing staff
	•	Removing staff
	•	Managing staff permissions

Schedules (schedules.py)

Allows staff to:
	•	Create class schedules
	•	View schedules
	•	Edit or delete existing entries
Members can view—but not edit—schedules.

Login (login.py)

Handles:
	•	Staff authentication (username + password)
	•	Member check-in using member ID
	•	Passes authenticated users to GymInterface

⸻

Database Design

Members Table

Stores:
	•	id
	•	name
	•	email
	•	phone
	•	membership type
	•	username
	•	password

Staff Table

Stores:
	•	id
	•	name
	•	role (Employee or Manager)
	•	username
	•	password

Both tables are accessed through simple CRUD (Create, Read, Update, Delete) operations.

⸻

Design Decisions

1. Tkinter for GUI

Tkinter was chosen because:
	•	It’s included with Python
	•	Easy for building multi-window applications
	•	Well-suited for CS2450 usability requirements

2. Modular file structure

Each feature is placed in its own file so the program stays:
	•	Organized
	•	Easy to maintain
	•	Easy to debug
	•	Easy to navigate for graders

3. SQLite for storage

SQLite was chosen because it:
	•	Requires no server setup
	•	Works well with Tkinter apps
	•	Stores data reliably between runs

4. Use of Toplevel windows

Using tk.Toplevel for each feature keeps the UI clean and separates responsibilities.

5. Dual login flow

Staff login requires authentication, while members simply check in using their ID.
This mirrors real gym systems and fits the assignment’s goal of designing realistic workflows.

⸻

Challenges Faced
	•	Ensuring windows were managed cleanly without locking or freezing
	•	Debugging database updates when incorrect columns were used
	•	Designing a member login system separate from staff login
	•	Making sure GUI elements updated correctly after membership changes
	•	Handling the auto-timeout feature without interrupting navigation

Future Improvements
	•	Add a visual theme (colors, icons, styling)
	•	Add check-in timestamps and history view for staff
	•	Include real billing or renewal systems
	•	Improve schedule editing with drag-and-drop or calendar UI
	•	Add profile pictures and more personalization
	•	Create better error handling and input validation
