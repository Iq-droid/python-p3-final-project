import sys
print(sys.path)
import click
from sqlalchemy import create_engine
from models import create_tables,create_session, add_review

@click.command()
@click.option('--vehicle_type', prompt='Vehicle Type')
@click.option('--brand', prompt='Brand')
@click.option('--condition', prompt='Condition')
@click.option('--buyer_name', prompt='Buyer Name')
@click.option('--contact', prompt='Contact')
@click.option('--rating', prompt='Rating', type=int)
@click.option('--comment', prompt='Comment')
def main(vehicle_type, brand, condition, buyer_name, contact, rating, comment):
    db_url = 'sqlite:///terra_track.db'
    engine = create_engine(db_url)
    create_tables(engine)
    session = create_session(engine)
    new_review = add_review(session, vehicle_type, brand, condition, buyer_name, contact, rating, comment)
    print(f'Review successfully added!\nReview ID: {new_review.id}')
    
if __name__ == '__main__':
    main()