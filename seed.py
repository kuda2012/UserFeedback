"""Seed file to make sample data for pets db."""

from models import User, Feedback, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Feedback.query.delete()

# Add User
kuda_hashed_password = User.register('password')
sydnee_hashed_password = User.register('password')
kuda = User(first_name="Kuda", last_name="Mwakutuya", email='kuda2012@gmail.com',
            username="kuda2012", password=kuda_hashed_password)
sydnee = User(first_name="Sydnee", last_name="Mwakutuya", email='sydnee@gmail.com',
              username="sydnee", password=sydnee_hashed_password)
# Add new objects to session, so they'll persist
db.session.add_all([kuda, sydnee])
# Commit--otherwise], this never gets saved!
db.session.commit()

# add some feedback posts
feedback_kuda = Feedback(
    title="Kuda1", content="Some content", username="kuda2012")
feedback_sydnee = Feedback(
    title="Sydnee1", content="Some content", username="sydnee")

db.session.add_all([feedback_kuda, feedback_sydnee])
db.session.commit()
