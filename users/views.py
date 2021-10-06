from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from .forms import (
    UserForm, UserProfileForm, AuthForm
)
from main.mixins import (
    AjaxFormMixin, 
    reCaptcha_validation, 
    form_errors, 
    redirect_params
)



result = 'Error'
message = 'Please try again'


# generic formview with the mixin to display user account page
class AccountView(TemplateView):
    template_name = 'users/account.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

def profile_view(request):     # this allows users to update their profile
    user = request.user
    user_profile = user.profile
    
    form = UserProfileForm(instance=user_profile)
    
    if request.is_ajax():
        form = UserProfileForm(data=request.POST, instance=user_profile)
        
        if form.is_valid():
            obj = form.save()
            obj.has_profile = True
            obj.save()
            message = 'Profile has Updated Succesfully'
            result = 'Success'
        
        else:
            message = form_errors(form)
        
        data = {'message': message, 'result': result}
        return JsonResponse(data)
    
    else:
        context = {'form': form}
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context['base_country'] = settings.BASE_COUNTRY
        
    return render(request, 'users/profile.html', context)
        
        

# generic formview with the mixin for user sign-up with recapture security
class SignUpView(AjaxFormMixin, FormView):
    template_name = 'users/sign_up.html'
    form_class = UserForm
    success_url = '/'
    
    def get_context_data(self, **kwargs):   #reCapture key required
        context = super().get_context_data(**kwargs)
        context['recaptcha_site_key'] = settings.RECAPTCHA_KEY
        return context
    
    def form_valid(self, form): # overwriting the mixin logic to get, check and save reCapture score
        response = super(AjaxFormMixin).form_valid(form)
        
        if self.request.is_ajax():
            token = form.cleaned_data.get('token')
            captcha = reCaptcha_validation(token)
            
            if captcha['success']:
                obj = form.save()
                obj.email = obj.email
                obj.save()
                
                user_profile = obj.userprofile
                user_profile.captcha_score = float(captcha['score'])
                user_profile.save()
                
                login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')
                
                result = 'Success'
                message = 'Thanks for signing up'
                
            data = {'result': result, 'message': message}
            return JsonResponse(data)
        return response
    


class SignInView(AjaxFormMixin, FormView):
    template_name = 'users/sign_in.html'
    form_class = AuthForm
    success_url = '/'
    
    def form_valid(self, form):
        response = super(AjaxFormMixin).form_valid(form)
        
        if self.request.is_ajax():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # tryna authenticate user
            user = authenticate(self.request, username=username, password=password)
            
            if user is not None:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                result = 'success'
                message = 'Logged in'
            
            else:
                message = form_errors(form)
            
            data = {'result': result, 'message': message}
            return JsonResponse(data)
        return response
    

def sign_out(request):
    logout(request)
    return redirect(reverse('user:sign-in'))