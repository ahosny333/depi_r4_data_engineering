from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import math

app = Flask(__name__)
CORS(app)

CSV_FILE = "jobs.csv"

# =========================
# LOAD CSV
# =========================

def load_data():
    df = pd.read_csv(CSV_FILE)

    # Replace NaN with empty string
    df = df.fillna("")

    return df


# =========================
# API ROUTE
# =========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/jobs", methods=["GET"])
def get_jobs():

    df = load_data()

    # =========================
    # QUERY PARAMETERS
    # =========================

    q = request.args.get("q", "").strip().lower()

    job_type = request.args.get("type", "").strip()
    location = request.args.get("location", "").strip()
    source = request.args.get("source", "").strip()

    sort_by = request.args.get("sort_by", "").strip()
    sort_dir = request.args.get("sort_dir", "asc").strip()

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    # =========================
    # SEARCH
    # =========================

    if q:

        df = df[
            df["Job_Title"].str.lower().str.contains(q, na=False)
            |
            df["Company_Name"].str.lower().str.contains(q, na=False)
            |
            df["Searched_For"].str.lower().str.contains(q, na=False)
        ]

    # =========================
    # FILTERS
    # =========================

    if job_type:
        df = df[df["Job_Type"] == job_type]

    if location:
        df = df[df["Location"].str.contains(location, case=False, na=False)]

    if source:
        df = df[
            df["Source_Website"]
            .str.lower()
            .str.contains(source.lower(), na=False)
        ]

    # =========================
    # SORTING
    # =========================

    allowed_sort_columns = [
        "Job_Title",
        "Company_Name",
        "Location",
        "Posted_Date",
        "Job_Type",
        "Experience_Required",
        "Salary",
        "Searched_For",
        "Source_Website"
    ]

    if sort_by in allowed_sort_columns:

        ascending = sort_dir == "asc"

        df = df.sort_values(
            by=sort_by,
            ascending=ascending
        )

    # =========================
    # STATS
    # =========================

    total = len(df)

    unique_companies = df["Company_Name"].nunique()
    unique_locations = df["Location"].nunique()
    unique_sources = df["Source_Website"].nunique()

    # =========================
    # PAGINATION
    # =========================

    total_pages = math.ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page

    paginated_df = df.iloc[start:end]

    # =========================
    # RESPONSE
    # =========================

    jobs = paginated_df.to_dict(orient="records")

    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,

        "unique_companies": int(unique_companies),
        "unique_locations": int(unique_locations),
        "unique_sources": int(unique_sources),

        "jobs": jobs
    })


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True)