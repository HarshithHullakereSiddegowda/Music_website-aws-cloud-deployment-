# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_render_template]
# [START gae_python3_render_template]
import datetime
import controller as dynamodb
from flask import Flask, render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from controller import newuser_dynamodb
from flask import session
from controller import put_music
from flask import session
import boto3
from controller import remove
from controller import create_presigned_url
import requests
app = Flask(__name__)


app.secret_key = 'harshithhs'

#Login page
@app.route("/", methods=['GET', 'POST'])
def root_checklogin():
    if request.method == 'POST':
        email = request.form['email']#entered user email and password at frontpage
        password = request.form['password']#entered user email and password at frontpage
        print(email, password)
        session['email']=email
        session['password']=password
        

        
        
        read = dynamodb.read_login(email, password)#Accesing the user name and password from dynamodb.readlogin
        #print(login.get('Item'))
        login = read.get('Item')
        
        if login is not None:
            
            if login['email'] == email and login['password'] == password:            
                user_name =login['user_name']
                session['user_name']=user_name

                subsc_music = dynamodb.get_subscribed_music(email, password)

                return render_template('mainpage.html', user_name=user_name, subscription=subsc_music)
                
            
        else:
            notvalid ='Email or Password is invalid'
            return render_template('root_checklogin.html', name=notvalid)    

    return render_template('root_checklogin.html')


#Registration page
@app.route('/registerpage', methods=['GET', 'POST'])
def root_register():
    
    if request.method == "POST":
        email = request.form['email']#entered user email and Email at registeration page
        username = request.form['username']#entered username  at regestration page
        password = request.form['password']#entered  password at frontpage

        dynamo = dynamodb.read_login(email, password)
        #print(dynamo['Item'])

        register = dynamo.get('Item')

        if register:
            if register['email'] == email or register['password']== password:

                message="The Email is already exists"

            return render_template('registerpage.html', message=message)
        else:
            newuser_dynamodb(email, username, password) 
            message="The Registration is Successful: please login with your email and password "
            
            return redirect('/')

            print('The entered email already exists')


    return render_template ('registerpage.html')

#Main page
@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    subscribed_music = []
    #print(subscribed_music)
    email=session['email']
    password=session['password']
    user_name =session['user_name']
    
    
    subsc_music = dynamodb.get_subscribed_music(email, password)
    
    
        # print(subsc_music)
       
        # return render_template('mainpage.html', subscription=subsc_music)

    # if request.method=="POST" and 'remove' in request.form:
    #     title = request.form['title']
    #     artist = request.form['artist']
    #     year = request.form['year']
        
    #     music_info= {'title': title, 'artist': artist, 'year': year}

    #     remove(email, password,music_info)
    #     return render_template('mainpage.html', user_name=user_name, subscription=subsc_music)
    

    if request.method=="POST":
        title=request.form['title']
        artist=request.form['artist']
        year=request.form['year']
        
        
        read_results =dynamodb.scan_music(title,artist,year)
        #new
       
        # response=requests.get(url)
        
        if read_results is None:
            query_message="No result is retrieved. Please query again."
            return render_template('mainpage.html',user_name=user_name, query_message=query_message, subscription=subsc_music)
        else:
            for item in read_results:
                artist_name=item['artist']
                artist_image_url=create_presigned_url("harshithbucket",f"{artist_name}.jpg")
                #response=requests.get(artist_image_url)
                item['artist_image']= artist_image_url
            return render_template('mainpage.html',user_name=user_name, read_results=read_results, subscription=subsc_music)

        
    elif request.method=="GET" and "title" in request.args:
        subscribed_title= request.args.getlist('title')
        subscribed_artist= request.args.getlist('artist')
        subscribed_year= request.args.getlist('year')
        subscribed_artist_image= request.args.getlist('artist_image')
        
    
        for i in range(len(subscribed_title)):
            music_info = {'title': subscribed_title[i], 'artist': subscribed_artist[i], 'year':subscribed_year[i], 'artist_image':subscribed_artist_image[i]}
            subscribed_music.append(music_info)
        
            print(subscribed_music)
        put_music(email, password, subscribed_music)
        return render_template('mainpage.html',user_name=user_name,subscription=subsc_music)
    
    


    

    return render_template('mainpage.html',user_name=user_name, subscription=subsc_music)

# @app.route('/remove_music')
# def remove_music():
#     email=session['email']
#     password=session['password']
#     user_name =session['user_name']
#     print("---------------------",user_name)
    


#     subsc_music = dynamodb.get_subscribed_music(email, password)
#     if request.method=="POST" and 'remove' in request.form:
#         title = request.form['title']
#         artist = request.form['artist']
#         year = request.form['year']
        
#         music_info= {'title': title, 'artist': artist, 'year': year}

#         remove(email, password,music_info)
#         return render_template('mainpage.html', user_name=user_name, subscription=subsc_music)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_render_template]
# [END gae_python38_render_template]
