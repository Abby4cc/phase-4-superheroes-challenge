# Flask Superheroes API 

A Flask-based RESTful API to track heroes and their superpowers. Built with SQLAlchemy and Flask-Migrate, this API follows best practices and returns fully formatted JSON responses.


##  Features

- Manage **Heroes**, **Powers**, and their associations through **HeroPowers**
- Data validations:
  - **Power** descriptions must be at least **20 characters**
  - **HeroPower** strength must be one of **Strong**, **Average**, or **Weak**

- The endpoints as follows:
  - `GET /heroes` – list all heroes
  - `GET /heroes/<id>` – show one hero with their powers
  - `GET /powers` – list all powers
  - `GET /powers/<id>` – show one power
  - `PATCH /powers/<id>` – update a power's description
  - `POST /hero_powers` – create a new hero-power association


##  Setup & Installation

```bash
# Clone & install dependencies
git clone https://github.com/Abby4cc/phase-4-superheroes-challenge
cd phase-4-superheroes-challenge

# Set up the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed the database 
python seed.py

# Launch the app
flask run --port 5555


## Contact & Support
Owner: Abigail Chelangat
Email: abigail.chelangat@student.moringaschool.com

 ##  License
 MIT License.
