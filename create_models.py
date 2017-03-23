from models import db, What, Who

# Delete all
db.reflect()
db.drop_all()

# Create all
db.create_all()

# Brief > What data
what_product = What('product')
what_service = What('service')
what_other = What('other')
db.session.add(what_product)
db.session.add(what_service)
db.session.add(what_other)
db.session.commit()

# Brief > What data
who_child = Who('child')
who_young = Who('young')
who_adult = Who('adult')
who_old = Who('old')
who_other = Who('other')
db.session.add(who_child)
db.session.add(who_young)
db.session.add(who_adult)
db.session.add(who_other)
db.session.commit()
# User data
