from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from app.models import UserProfile
from app.models import Class
from app.models import Place
from app.models import Layout
from app.models import Zone



from django.template.context import RequestContext

from ClassMateZ.settings import MEDIA_DIR

from app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import QueryDict
from datetime import datetime, date
import os
import itertools

def index(request):
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!

    day = date.today().strftime("%A")

    context_dict = {'day':day}

    if request.user.is_authenticated():
        print ("Authenticition complete")
        userClasses = UserProfile.objects.get(user=request.user)
        context_dict['userClasses'] = userClasses
        print (userClasses)


    response = render(request, 'ClassMateZ/index.html', context_dict)
	# Call function to handle the cookies
	# Return response back to the user, updating any cookies that need changed.
    return response


def index_week(request):
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!

    day = date.today().strftime("%A")

    context_dict = {'day':day}

    if request.user.is_authenticated():
        print ("Authenticition complete")
        userClasses = UserProfile.objects.get(user=request.user)
        context_dict['userClasses'] = userClasses
        print (userClasses)


    response = render(request, 'ClassMateZ/index_week.html', context_dict)
	# Call function to handle the cookies
	# Return response back to the user, updating any cookies that need changed.
    return response


def showClass(request, classId):
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!

    day = date.today().strftime("%A")

    context_dict = {'day':day}

    classToShow = Class.objects.get(classId=classId)
    context_dict['classToShow'] = classToShow

    zones = Zone.objects.filter(zClass=classToShow)
    context_dict['zones'] = zones

    zonesCoordList = classToShow.place.layout.zoneCoords
    nbrOfZones = range(len(zonesCoordList.split(";")))
    context_dict['zonesCoordList'] = zonesCoordList
    context_dict['nbrOfZones'] = nbrOfZones

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
		decision = request.POST.get('choice')
		zoneNbr = request.POST.get('zoneNbr')

		if (zoneNbr != "None"):
		    if (decision == "1"):
		        zoneChosen = Zone.objects.get(zClass=classToShow, zoneNumber=int(zoneNbr))
		        zoneChosen.users.add(user_profile)
		    elif (decision == "0"):
		        zoneChosen = Zone.objects.get(zClass=classToShow, zoneNumber=int(zoneNbr))
		        zoneChosen.users.remove(user_profile)

    response = render(request, 'ClassMateZ/showClass.html', context_dict)
	# Call function to handle the cookies
	# Return response back to the user, updating any cookies that need changed.
    return response


def register(request):
	# A boolean value for telling the template
	# whether the registration was successful.
	# Set to False initially. Code changes value to
	# True when registration succeeds.
	registered = False
	# If it's a HTTP POST, we're interested in processing form data.
	print ("registration request received")
	if request.method == 'POST':

		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		# If the two forms are valid...
		print (user_form)
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()
			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves,
			# we set commit=False. This delays saving the model
			# until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.name = user.username
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and
			#put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			# Now we save the UserProfile model instance.
			profile.save()
			password = request.POST.get('password', None)
			authenticated = authenticate(username=user.username, password=password)
			if authenticated:
			    login(request, authenticated)
			# Update our variable to indicate that the template
			# registration was successful.
			registered = True
		else:
			# Invalid form or forms - mistakes or something else?
			# Print problems to the terminal.
			print(user_form.errors, profile_form.errors)
	else:
		# Not a HTTP POST, so we render our form using two ModelForm instances.
		# These forms will be blank, ready for user input.
		user_form = UserForm()
		profile_form = UserProfileForm()
		# Render the template depending on the context.
	return render(request,
		'ClassMateZ/register.html',
		{'user_form': user_form,
		'profile_form': profile_form,
		'registered': registered})


def user_login(request):
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# We use request.POST.get('<variable>') as opposed
		# to request.POST['<variable>'], because the
		# request.POST.get('<variable>') returns None if the
		# value does not exist, while request.POST['<variable>']
		# will raise a KeyError exception.
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect(reverse('app:index'))
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print("Invalid login details: {0}, {1}".format(username, password))
			return render(request, 'ClassMateZ/index.html', {})
	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'ClassMateZ/index.html', {})


@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.

	return HttpResponseRedirect(reverse('app:index'))

def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	last_visit_cookie = get_server_side_cookie(request,
	'last_visit',
	str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7],
	'%Y-%m-%d %H:%M:%S')
	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		#update the last visit cookie now that we have updated the count
		request.session['last_visit'] = str(datetime.now())
	else:
		visits = 1
		# set the last visit cookie
		request.session['last_visit'] = last_visit_cookie
	# Update/set the visits cookie
	request.session['visits'] = visits

def about (request):
	print(request.method)
	print(request.user)
	return render(request, 'ClassMateZ/about.html', {})

def profile (request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    dict = {'picture': user_profile.picture, 'name': user_profile.name, 'classes': user_profile.classes }
    data_json = QueryDict('', mutable=True)
    data_json.update(dict)
    updated = False

    if user.is_authenticated():
        print("Authenticition complete")
    if request.method == 'POST':
        data = request.POST
        print(data)
        #profile_form = UserProfileForm(data=data)
        if True: #profile_form.is_valid():
            print(data)
            #profile = profile_form.save(commit=False)
            user_profile.name = data.get("name")
            #user_profile.classes = profile.classes
            print(request.FILES)
            if 'file' in request.FILES:
                print(1000000000000)
                #user_profile.picture = request.FILES['picture']
            if 'picture' in request.FILES:
                picture = str(request.FILES.get('picture'))
                print(str(request.FILES.get('picture',False)), 1000000)
                handle_uploaded_file(picture, request.FILES['picture'])
                user_profile.picture = "/profile_images/" + picture

            classes = data.getlist("classes", [])
            added_classes = []
            for class_name in classes:
                added_classes.append(Class.objects.filter(name=class_name))
            merged = Class.objects.filter(name = "adasdasdaasdasdasdasdfasfsdagdrfgs")
            for query in added_classes:
                merged = itertools.chain(merged, query)
            user_profile.classes = merged
            user_profile.save()
            updated = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_profile.errors)
        user.email = data.__getitem__("email")
        user.save()
    else:
        profile_form = UserProfileForm(data=data_json)
    return render(request, 'ClassMateZ/profile.html', {#'profile_form': profile_form,
        'updated': updated, 'user_profile': user_profile, 'all_classes': all_classes()})

#Saves the file in /media/profile_images
def handle_uploaded_file(url, f):
    path = os.path.join(MEDIA_DIR, 'profile_images')
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, url), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#Returns a dictonary the includes all the class blocks with the same name
def find_classes(user):
    user_profile = UserProfile.objects.get(user=user)
    print(user_profile.classes)
    classes_dict = {}
    for class_block in user_profile.classes:
        classes_dict[class_block.name] = class_block
    return classes_dict

def all_classes():
    classes = Class.objects.filter().distinct()
    '''names = []
    merged = Class.objects.filter(name="122131231fsdfs1312saf")
    for class_block in classes:
        name = class_block.name
        if name not in names:
            names.append(class_block.name)
            merged = itertools.chain(merged, class_block)
    print(merged)
    return merged'''
    return classes

def SquadZ (request):
	print(request.method)
	print(request.user)
	return render(request, 'ClassMateZ/SquadZ.html', {})
