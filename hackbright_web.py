"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'NA')

    if github != 'NA':
        first, last, github = hackbright.get_student_by_github(github)
        projects = hackbright.get_grades_by_github(github)

        print("projects:")
        print(projects)

        # return "{} is the GitHub account for {} {}".format(github, first, last)
        return render_template('student_info.html', 
            first=first, last=last, github=github, projects=projects)
    else:
        return 'Student not found'

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add-student-form")
def student_form():
    """Show form for adding a student."""
    return render_template("add_student.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(fname, lname, github)

    return render_template("successful_add.html", first=fname, last=lname)

@app.route("/project")
def get_project():
    """Show information about a project."""

    title = request.args.get('title', 'NA')
    project_info = hackbright.get_project_by_title(title)
    
    return render_template('project_info.html', element=project_info)
            

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
