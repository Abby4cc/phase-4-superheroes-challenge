from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)


    @app.route('/')
    def index():
        return jsonify({"message": "Superheroes code challenge!"}), 200

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        return jsonify([h.to_dict() for h in heroes]), 200

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if not hero:
            return jsonify({"error": "Hero not found"}), 404
        
        data = hero.to_dict()
        data['hero_powers'] = [
            {
                'id': hp.id,
                'hero_id': hp.hero_id,
                'power_id': hp.power_id,
                'strength': hp.strength,
                'power': hp.power.to_dict()
            } for hp in hero.hero_powers
        ]
        return jsonify(data), 200

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        return jsonify([p.to_dict() for p in powers]), 200

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404
        return jsonify(power.to_dict()), 200

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404

        data = request.get_json()
        if 'description' not in data:
            return jsonify({"errors": ["Missing description"]}), 400

        try:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict()), 200
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()

        required = ['hero_id', 'power_id', 'strength']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"errors": [f"Missing: {', '.join(missing)}"]}), 400

        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        if not hero or not power:
            return jsonify({"errors": ["Invalid hero_id or power_id"]}), 400

        try:
            hero_power = HeroPower(
                hero_id=data['hero_id'],
                power_id=data['power_id'],
                strength=data['strength']
            )
            db.session.add(hero_power)
            db.session.commit()

            return jsonify(hero_power.to_dict_with_nested()), 201
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
