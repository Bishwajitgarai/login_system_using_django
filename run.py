from flaskapp import app,db
# from flaskapp.models import Post,User
# db.create_all()

if __name__=="__main__":
    app.run(debug=True,port=5050)