from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    addPoints,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    commentForm,
)

postBlueprint = Blueprint("post", __name__)


@postBlueprint.route("/post/<int:postID>", methods=["GET", "POST"])
def post(postID):
    match "userName" in session:
        case True:
            form = commentForm(request.form)
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f"select id from posts")
            posts = str(cursor.fetchall())
            match str(postID) in posts:
                case True:
                    message("2", f'POST: "{postID}" FOUND')
                    connection = sqlite3.connect("db/posts.db")
                    cursor = connection.cursor()
                    cursor.execute(f'select * from posts where id = "{postID}"')
                    post = cursor.fetchone()
                    print(post)
                    cursor.execute(f'update posts set views = views+1 where id = "{postID}"')
                    connection.commit()
                    if request.method == "POST":
                        comment = request.form["comment"]
                        connection = sqlite3.connect("db/comments.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f"""
                            insert into comments(post,comment,user,date,time)
                            values({postID},"{comment}","{session["userName"]}",
                            "{currentDate()}",
                            "{currentTime()}")
                            """
                        )
                        connection.commit()
                        addPoints(5, session["userName"])
                        flash("You earned 5 points by commenting ", "success")
                        return redirect(f"/post/{postID}")
                    connection = sqlite3.connect("db/comments.db")
                    cursor = connection.cursor()
                    cursor.execute(f'select * from comments where post = "{postID}"')
                    comments = cursor.fetchall()
                    return render_template(
                        "post.html",
                        id=post[0],
                        title=post[1],
                        month=post[2],
                        content=post[3],
                        author=post[4],
                        book=post[5],
                        views=post[8],
                        date=post[6],
                        time=post[7],
                        form=form,
                        comments=comments,
                    )
                case False:
                    message("1", "404")
                    return render_template("404.html")
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need loin for create a post", "error")
            return redirect("/login")
        
