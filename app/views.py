from django.shortcuts import render, redirect
from django.db import connection

def login(request):
    context = {}
    status = ""
    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, user_password FROM user_base WHERE user_id = %s", 
                           [request.POST["user_id"]])
            customers = cursor.fetchone()
        if customers == None:
            status = "Login failed, no such user. Please create an account."
        elif customers[0] == "admin@admin.com":
            if customers[1] == request.POST["user_password"]:
                status = "Login successful."
                return redirect('admin_page')
            else:
                status = "Login failed, wrong password."
        else:
            if customers[1] == request.POST["user_password"]:
                status = "Login successful."
                return redirect('home_user', id = request.POST["user_id"])
            else:
                status = "Login failed, wrong password."
    context["status"] = status
    return render(request,'app/login.html', context)

def register(request):
    """Shows the main page"""
    context = {}
    status = ''
    if request.POST:
        ## Check if userid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_base WHERE user_id = %s", [request.POST['user_id']])
            user = cursor.fetchone()
            ## No user with same id
            if user == None:
                cursor.execute("INSERT INTO user_base VALUES (%s, %s, %s, %s, %s)", 
                               [request.POST['user_id'],
                                request.POST['user_password'], 
                                request.POST['first_name'],
                                request.POST['last_name'] , 
                                request.POST['phone_number']])
                return redirect('login')    
            else:
                status = 'User with ID %s already exists' % (request.POST['user_id'])
    context['status'] = status
    return render(request, "app/register.html", context)

def dashboard(request):
    """Shows the admin dashboard"""
    context = {}
    status = ''

    context['status'] = status
    ## Use sample query to get listings
    """Displays the total revenue for each listing"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT l.listing_name,
            SUM((upper(r.date_range) - lower(r.date_range)) * l.price) AS total_revenue
            FROM reservations r, listings l
            WHERE r.listing_id = l.listing_id
            GROUP BY l.listing_name
            ORDER BY total_revenue DESC
            LIMIT 10
            """
            ),
        totalrev = cursor.fetchall()
        result_dictRev = {'recordsRev': totalrev}
        
    """Displays the total revenue for each neighbourhood, along with number of listings in that neighbourhood"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT l.neighbourhood,
                SUM((upper(r.date_range) - lower(r.date_range)) * l.price) AS total_revenue,
            COUNT(*) as number_of_listings
            FROM reservations r, listings l
            WHERE r.listing_id = l.listing_id
            GROUP BY l.neighbourhood
            ORDER BY total_revenue DESC
            LIMIT 10
            """
            ),
        totalrevL = cursor.fetchall()
        result_dictRevL = {'recordsRevL': totalrevL}
        
    """Displays the top 20% of Owners by Total Revenue"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT l.owner_id, u.first_name, u.last_name,
                SUM((upper(r.date_range) - lower(r.date_range)) * l.price) AS total_revenue
            FROM reservations r, listings l, user_base u
            WHERE r.listing_id = l.listing_id
                AND l.owner_id = u.user_id
            GROUP BY l.owner_id, u.first_name, u.last_name
            ORDER BY total_revenue DESC
            LIMIT (SELECT COUNT(DISTINCT owner_id)*0.2 FROM listings);
            """
            ),
        totalO = cursor.fetchall()
        result_dictO = {'recordsO': totalO}

    return render(request,'app/dashboard.html', {'recordsRev': totalrev, 'recordsRevL': totalrevL, 'recordsO': totalO})

def admin_page(request):
    """Shows the admin page"""
    return render(request,'app/admin_page.html')

def landing(request):
    """Shows the landing page"""
    return render(request,'app/landing.html')

# Create your views here.
def home(request):
    """Shows the home page after login"""
    return render(request,'app/home.html')

# Create your views here.
def view(request, id):
    """Shows view page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings WHERE listing_id = %s", [id])
        listing = cursor.fetchone()
    result_dict = {'list': listing}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows add page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM listings WHERE listing_id = %s", [request.POST['listing_id']])
            customer = cursor.fetchone()
            ## No listing with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO listings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['listing_id'], request.POST['listing_name'], request.POST['neighbourhood'],
                           request.POST['neighbourhood_group'] , request.POST['address'],
                           request.POST['room_type'] , request.POST['price'], request.POST['owner_id'], request.POST['total_occupancy'],
                           request.POST['total_bedrooms'] , request.POST['has_internet'], request.POST['has_aircon'], request.POST['has_kitchen'],
                           request.POST['has_heater'] ])
                return redirect('index')    
            else:
                status = 'Listing with ID %s already exists' % (request.POST['listing_id'])
                
    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows edit page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings WHERE listing_id = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute(
               """
               UPDATE listings SET listing_id = %s, 
                   listing_name = %s, neighbourhood = %s, 
                   neighbourhood_group = %s, address = %s, 
                   room_type = %s,price = %s,owner_id = %s,
                   total_occupancy = %s,total_bedrooms = %s,
                   has_internet = %s,has_aircon = %s,
                   has_kitchen = %s,has_heater = %s 
               WHERE listing_id = %s
               """
            , [request.POST['listing_id'], request.POST['listing_name'], request.POST['neighbourhood'],
                   request.POST['neighbourhood_group'] , request.POST['address'],
                   request.POST['room_type'] , request.POST['price'], request.POST['owner_id'], request.POST['total_occupancy'],
                   request.POST['total_bedrooms'] , request.POST['has_internet'], request.POST['has_aircon'], request.POST['has_kitchen'],
                   request.POST['has_heater'], id ])
            status = 'Listing edited successfully!'
            cursor.execute("SELECT * FROM listings WHERE listing_id = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)

def reservations(request):
    """Shows the reservations table"""
    context = {}
    status = ''
    
    ## Delete listing
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM reservations WHERE reservation_id = %s", [request.POST['idR']])
    
    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute(
                """
                SELECT * 
                FROM  reservations r
                WHERE reservation_id = %s 
                ORDER BY r.reservation_id
                """,
                [
                    request.POST['reservation_id']
                ])                
                listings = cursor.fetchall()

            result_dictR = {'recordsR': reservations}

            return render(request,'app/reservations.html', result_dictR)
    else:
        context['status'] = status
        ## Use sample query to get listings

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM reservations r
                ORDER BY r.reservation_id
                """
                ),
            reservations = cursor.fetchall()

        result_dictR = {'recordsR': reservations}

        return render(request,'app/reservations.html', result_dictR)

def home_user(request, id):
    """Shows the home page for each user"""
    context = {}
    status = ''
    
    ## Delete reservation
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM reservations WHERE reservation_id = %s", [request.POST['idR']])
    else:
        context['status'] = status
        ## Use sample query to get listings

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM reservations r
                WHERE user_id = %s
                ORDER BY r.reservation_id
                """
                , [id]),
            reservations = cursor.fetchall()

        result_dictR = {'recordsR': reservations}

        return render(request,'app/home_user.html', result_dictR)
    

def marketplace(request):
    """Shows the listings table"""
    context = {}
    status = ''
    
    ## Delete listing
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM listings WHERE listing_id = %s", [request.POST['id']])
    
    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute(
                """
                SELECT l.listing_id,
                    l.listing_name,
                    l.neighbourhood, l.neighbourhood_group, l.address, l.room_type,
                    l.price, CASE WHEN a.average_review is NULL THEN 0 ELSE a.average_review END,
                    l.owner_id, l.total_occupancy, l.total_bedrooms
                FROM
                    listings l
                WHERE neighbourhood_group = %s
                    AND total_occupancy >= %s
                LEFT JOIN
                (SELECT res.listing_id,
                AVG(rev.review)::NUMERIC(3,2) AS average_review
                FROM reviews rev, reservations res
                WHERE rev.reservation_id = res.reservation_id
                GROUP BY res.listing_id) AS a
                ON l.listing_id = a.listing_id
                ORDER BY l.listing_id
                """,
                [
                    request.POST['neighbourhood_group'],
                    request.POST['total_occupancy']
                ])                
                listings = cursor.fetchall()

            result_dict = {'records': listings}

            return render(request,'app/marketplace.html', result_dict)
    else:
        context['status'] = status
        ## Use sample query to get listings

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT l.listing_id,
                    l.listing_name,
                    l.neighbourhood, l.neighbourhood_group, l.address, l.room_type,
                    l.price, CASE WHEN a.average_review is NULL THEN 0 ELSE a.average_review END,
                    l.owner_id, l.total_occupancy, l.total_bedrooms
                FROM
                    listings l
                LEFT JOIN
                (SELECT res.listing_id,
                AVG(rev.review)::NUMERIC(3,2) AS average_review
                FROM reviews rev, reservations res
                WHERE rev.reservation_id = res.reservation_id
                GROUP BY res.listing_id) AS a
                ON l.listing_id = a.listing_id
                ORDER BY l.listing_id
                """
                ),
            listings = cursor.fetchall()

        result_dict = {'records': listings}

        return render(request,'app/marketplace.html', result_dict)
    
def marketplace_user(request):
    """Shows the listings table"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute(
                """
                SELECT * 
                FROM  listings l
                WHERE neighbourhood_group = %s 
                AND total_occupancy >= %s 
                ORDER BY l.listing_id
                """,
                [
                    request.POST['neighbourhood_group'],
                    request.POST['total_occupancy']
                ])                
                listings = cursor.fetchall()

            result_dict = {'records': listings}

            return render(request,'app/marketplace_user.html', result_dict)
    else:
        context['status'] = status
        ## Use sample query to get listings

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM listings l
                ORDER BY l.listing_id
                """
                ),
            listings = cursor.fetchall()

        result_dict = {'records': listings}

        return render(request,'app/marketplace_user.html', result_dict)
