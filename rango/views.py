from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime

def decode(category_name_url):
	return category_name_url.replace('_',' ')

def encode(category_name):
	return category_name.replace(' ','_')

def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__istartswith=starts_with)
	else:
		cat_list = Category.objects.order_by('name')

	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]

	for cat in cat_list:
		cat.url = encode(cat.name)

	return cat_list


def index(request):
	
	# Code to demonstrate cookies work
	# request.session.set_test_cookie()

	# if request.session.test_cookie_worked():
	
	# 	request.session.delete_test_cookie()
	context = RequestContext(request)
	
	cat_list = Category.objects.order_by('name')
	context_dict = {}
	
	for category in cat_list:
		category.url = category.name.replace(' ','_')

	page_list = Page.objects.order_by('-views')[:5]
	
	context_dict['pages'] = page_list
	context_dict['cat_list'] = cat_list
	#will only appear if the number is > 0!
	#visits = int(request.COOKIES.get('visits', '0'))
	
	if request.session.get('last_visit'):
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits','0')

		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 3:
			request.session['visits'] = visits+1
			request.session['last_visit'] = str(datetime.now())

	else:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1
	
	return render_to_response('rango/index.html',context_dict,context)

def about(request):
	context = RequestContext(request)
	context_dict = {}
	last_visit_time = None
	visits_num = None

	if request.session.get('last_visit'):
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits','0')

		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 3:
			request.session['visits'] = visits+1
			request.session['last_visit'] = str(datetime.now())

	else:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1

	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0

	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list
	context_dict['last_visit_time'] = last_visit_time
	context_dict['visits_num'] = count

	return render_to_response('rango/about.html',context_dict,context)

def category(request, category_name_url):
	context = RequestContext(request)
	
	category_name = decode(category_name_url)

	context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	try:
		category = Category.objects.get(name__iexact=category_name)
		context_dict['category'] = category

		pages = Page.objects.filter(category=category).order_by('-views')
		context_dict['pages'] = pages
	except Category.DoesNotExist:
		pass

	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
			context_dict['result_list'] = result_list

	
	return render_to_response('rango/category.html',context_dict, context)

def add_category(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			#call the index view to go to the homepage
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()

	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list
	context_dict['form']=form
	return render_to_response('rango/add_category.html', context_dict, context)

def add_page(request,category_name_url):
	context = RequestContext(request)

	category_name = decode(category_name_url)

	context_dict = {}
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit=False)
		
			try:
				cat = Category.objects.get(name=category_name)
				page.category = cat
			except Category.DoesNotExist:
				return render_to_response('rango/add_category.html', context_dict, context)

			page.views = 0
			page.save()

			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {
		'category_name_url': category_name_url,
		'category_name': category_name, 
		'form': form}
	
	return render_to_response('rango/add_page.html',context_dict,
		context)

def register(request):
	context = RequestContext(request)

	registered = False

	context_dict = {}
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now we save the UserProfile model instance.
			profile.save()

			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}

	return render_to_response('rango/register.html', context_dict, context)

def user_login(request):
	context = RequestContext(request)

	context_dict = {}
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango/')

			else:
				return HttpResponse("Your rango account is disabled.")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	else:
		return render_to_response('rango/login.html',context_dict,context)

def some_view(request):
	if not request.user.is_authenticated():
		return HttpResponse("You are logged in.")
	else:
		return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
	text = "You're logged in!"
	context_dict = {'text':text}
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	return render_to_response('rango/restricted.html',context_dict,context_instance=RequestContext(request))

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')

def search(request):
	context = RequestContext(request)
	result_list = []

	context_dict = {}
	cat_list = get_category_list()

	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			result_list = run_query(query)

	context_dict = {'result_list': result_list,'cat_list': cat_list}
	
	return render_to_response('rango/search.html', context_dict, context)

@login_required
def profile(request):
	context = RequestContext(request)
	context_dict = {}
	cat_list = get_category_list()
	context_dict['cat_list'] = cat_list

	u = User.objects.get(username=request.user)
	
	try:
		up = UserProfile.objects.get(user=u)
	except:
		up = None

	context_dict['user'] = u
	context_dict['userprofile'] = up

	return render_to_response('rango/profile.html', context_dict, context)

def track_url(request):
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				return HttpResponseRedirect(page.url)
			except Page.DoesNotExist:
				return HttpResponseRedirect('/rango/')

@login_required
def like_category(request):
	context = RequestContext(request)
	cat_id = None

	if request.method == 'GET':
		cat_id = request.GET['category_id']

	likes = 0
	if cat_id:
		category = Category.objects.get(id=int(cat_id))
		if category:
			likes = category.likes + 1
			category.likes = likes
			category.save()

	return HttpResponse(likes)

def suggest_category(request):
	context = RequestContext(request)
	cat_list = []
	starts_with = ''

	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	cat_list = get_category_list(5, starts_with)

	return render_to_response('rango/category_list.html', {'cat_list': cat_list}, context)

@login_required
def auto_add_page(request):
	context = RequestContext(request)
	cat_id = None
	url = None
	title = None
	context_dict = {}
	
	if request.method == 'GET':
		cat_id = request.GET['category_id']
		url = request.GET['url']
		title = request.GET['title']
		
		if cat_id:
			category = Category.objects.get(id=int(cat_id))
			p = Page.objects.get_or_create(category=category, title=title, url=url)
			pages = Page.objects.filter(category=category).order_by('-views')
			context_dict['pages'] = pages

	return render_to_response('rango/pages_list.html',context_dict,context)























