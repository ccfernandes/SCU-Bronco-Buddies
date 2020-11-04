from bronco_buddies import app

# run the app 
if __name__ == '__main__':
    # init_db()
    # Change the debug to False when deploying to production
    app.run(debug=False, host='127.0.0.1')
