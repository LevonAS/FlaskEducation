from flask import Blueprint, render_template, redirect


report_app = Blueprint('report', __name__, static_folder='../static', url_prefix='/reports')

# REPORTS = {
#     1: "Yesterday",
#     2: "Today",
#     3: "Tomorrow",
# }
REPORTS = [1, 2, 3, 4, 5]

@report_app.route('/')
def report_list():
    return render_template(
        'reports/list.html',
        reports=REPORTS,
    )