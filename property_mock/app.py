from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock data for property listings
listings = [
    {
        'id': 1,
        'title': 'Cozy Cottage',
        'location': 'Auckland',
        'price': 120,
        'available': True,
        'image': 'cozy_cottage.jpg',
        'bedrooms': 2,
        'bathrooms': 1,
        'parking': True,
        'testimonials': [
            "Lovely place, very cozy and comfortable!",
            "Perfect getaway spot, will visit again."
        ]
    },
    {
        'id': 2,
        'title': 'Modern Apartment',
        'location': 'Wellington',
        'price': 150,
        'available': True,
        'image': 'modern_apartment.jpg',
        'bedrooms': 3,
        'bathrooms': 2,
        'parking': True,
        'testimonials': [
            "Amazing apartment with all the modern amenities.",
            "Great location, highly recommend!"
        ]
    },
    {
        'id': 3,
        'title': 'Beach House',
        'location': 'Christchurch',
        'price': 200,
        'available': True,
        'image': 'beach_house.jpg',
        'bedrooms': 4,
        'bathrooms': 2,
        'parking': True,
        'testimonials': [
            "Stunning views and right on the beach.",
            "A bit pricey but worth it for the location."
        ]
    },
    {
        'id': 4,
        'title': 'Mountain Retreat',
        'location': 'Queenstown',
        'price': 250,
        'available': True,
        'image': 'mountain_retreat.jpg',
        'bedrooms': 5,
        'bathrooms': 3,
        'parking': True,
        'testimonials': [
            "Perfect place for a winter getaway.",
            "Close to ski resorts, very cozy."
        ]
    },
    {
        'id': 5,
        'title': 'Urban Loft',
        'location': 'Auckland',
        'price': 180,
        'available': True,
        'image': 'urban_loft.jpeg',
        'bedrooms': 2,
        'bathrooms': 2,
        'parking': False,
        'testimonials': [
            "Modern and stylish, in the heart of the city.",
            "Great for a weekend stay."
        ]
    },
    {
        'id': 6,
        'title': 'Country Villa',
        'location': 'Hamilton',
        'price': 220,
        'available': True,
        'image': 'country_villa.jpeg',
        'bedrooms': 3,
        'bathrooms': 2,
        'parking': True,
        'testimonials': [
            "Beautiful and quiet, with lovely gardens.",
            "A great escape from the city."
        ]
    }
]

@app.route('/')
def index():
    return render_template('index.html', listings=listings[:2])  # Show top 2 listings

@app.route('/listings', methods=['POST', 'GET'])
def search_listings():
    if request.method == 'POST':
        location = request.form.get('location')
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')
        bedrooms = request.form.get('bedrooms')
        parking = request.form.get('parking')

        filtered_listings = [
            listing for listing in listings
            if (not location or location.lower() in listing['location'].lower()) and
               (not min_price or listing['price'] >= int(min_price)) and
               (not max_price or listing['price'] <= int(max_price)) and
               (not bedrooms or listing['bedrooms'] == int(bedrooms)) and
               (not parking or str(listing['parking']) == parking) and
               listing['available']
        ]
    else:
        filtered_listings = listings  # This will show all listings when accessed via GET method

    return render_template('listings.html', listings=filtered_listings)

@app.route('/listing/<int:listing_id>')
def view_listing(listing_id):
    listing = next((l for l in listings if l['id'] == listing_id), None)
    if listing:
        return render_template('view_listing.html', listing=listing)
    else:
        return "Listing not found", 404

@app.route('/book/<int:listing_id>', methods=['POST', 'GET'])
def book_listing(listing_id):
    listing = next((l for l in listings if l['id'] == listing_id), None)
    if listing and listing['available']:
        return render_template('booking.html', listing=listing)
    else:
        return redirect(url_for('index'))

@app.route('/confirm_payment/<int:listing_id>', methods=['POST'])
def confirm_payment(listing_id):
    listing = next((l for l in listings if l['id'] == listing_id), None)
    if listing and listing['available']:
        checkin_date = request.form.get('checkin_date')
        checkout_date = request.form.get('checkout_date')
        notes = request.form.get('notes')
        booking_reference = f"BOOK-{listing_id}-{request.form.get('name')[:3].upper()}"
        listing['available'] = False
        return render_template('booking_confirmation.html', reference=booking_reference, listing=listing,
                               checkin_date=checkin_date, checkout_date=checkout_date, notes=notes)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
