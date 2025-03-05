from base_query import BaseQuery

class JobPostQueries(BaseQuery):
    """
    Handles queries related to the realtimejobs_jobpost table.
    """

    def fetch_all_jobs(self):
        """Retrieve all job posts."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            ORDER BY created_at DESC;
        """
        print("[INFO] Fetching all job posts")
        return self.fetch_all(query)

    def find_job_by_id(self, job_id):
        """Find a job by its ID."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, description, created_at
            FROM realtimejobs_jobpost
            WHERE id = %s
            LIMIT 1;
        """
        print(f"[INFO] Searching for job with ID: {job_id}")
        return self.fetch_one(query, (job_id,))

    def find_job_by_slug(self, slug):
        """Find a job by its slug."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, description, created_at
            FROM realtimejobs_jobpost
            WHERE slug = %s
            LIMIT 1;
        """
        print(f"[INFO] Searching for job with slug: {slug}")
        return self.fetch_one(query, (slug,))

    def fetch_jobs_by_category(self, category_id):
        """Fetch jobs under a specific category."""
        query = """
            SELECT id, title, slug, location, is_worldwide, company_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            WHERE category_id = %s
            ORDER BY created_at DESC;
        """
        print(f"[INFO] Fetching jobs for category ID: {category_id}")
        return self.fetch_all(query, (category_id,))

    def fetch_jobs_by_company(self, company_id):
        """Fetch all jobs posted by a specific company."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            WHERE company_id = %s
            ORDER BY created_at DESC;
        """
        print(f"[INFO] Fetching jobs for company ID: {company_id}")
        return self.fetch_all(query, (company_id,))

    def fetch_recent_jobs(self, limit=10):
        """Fetch the most recent job posts."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            ORDER BY created_at DESC
            LIMIT %s;
        """
        print(f"[INFO] Fetching {limit} most recent jobs")
        return self.fetch_all(query, (limit,))

    def search_jobs(self, search_term):
        """Search jobs by title, description, or tags."""
        query = """
            SELECT j.id, j.title, j.slug, j.location, j.is_worldwide, j.company_id, j.job_type_id, j.salary, j.short_description, j.created_at
            FROM realtimejobs_jobpost j
            LEFT JOIN realtimejobs_tag_jobpost tj ON j.id = tj.jobpost_id
            LEFT JOIN realtimejobs_tag t ON tj.tag_id = t.id
            WHERE j.title LIKE %s OR j.short_description LIKE %s OR t.name LIKE %s
            ORDER BY j.created_at DESC;
        """
        like_term = f"%{search_term}%"
        print(f"[INFO] Searching jobs for term: {search_term}")
        return self.fetch_all(query, (like_term, like_term, like_term))

    def fetch_remote_jobs(self):
        """Fetch jobs that are fully remote (worldwide)."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            WHERE is_worldwide = TRUE
            ORDER BY created_at DESC;
        """
        print("[INFO] Fetching worldwide remote jobs")
        return self.fetch_all(query)

    def fetch_jobs_by_location(self, location):
        """Fetch jobs based on a specific location."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            WHERE location = %s
            ORDER BY created_at DESC;
        """
        print(f"[INFO] Fetching jobs for location: {location}")
        return self.fetch_all(query, (location,))

    def fetch_jobs_by_salary_range(self, min_salary, max_salary):
        """Fetch jobs within a salary range."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            WHERE salary BETWEEN %s AND %s
            ORDER BY created_at DESC;
        """
        print(f"[INFO] Fetching jobs with salary range: {min_salary} - {max_salary}")
        return self.fetch_all(query, (min_salary, max_salary))

    def fetch_jobs_by_job_type(self, job_type_id):
        """Fetch jobs based on job type (e.g., Full-time, Part-time, Contract)."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            WHERE job_type_id = %s
            ORDER BY created_at DESC;
        """
        print(f"[INFO] Fetching jobs for job type ID: {job_type_id}")
        return self.fetch_all(query, (job_type_id,))

    def fetch_jobs_with_tag(self, tag_name):
        """Fetch jobs that have a specific tag."""
        query = """
            SELECT j.id, j.title, j.slug, j.location, j.is_worldwide, j.company_id, j.job_type_id, j.salary, j.short_description, j.created_at
            FROM realtimejobs_jobpost j
            JOIN realtimejobs_tag_jobpost tj ON j.id = tj.jobpost_id
            JOIN realtimejobs_tag t ON tj.tag_id = t.id
            WHERE t.name = %s
            ORDER BY j.created_at DESC;
        """
        print(f"[INFO] Fetching jobs with tag: {tag_name}")
        return self.fetch_all(query, (tag_name,))

    def add_job_post(self, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, description, job_url, user_id):
        """Insert a new job post."""
        query = """
            INSERT INTO realtimejobs_jobpost (title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, description, job_url, user_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW());
        """
        print(f"[INFO] Adding new job post: {title}")
        self.execute_query(query, (title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, description, job_url, user_id))

    def update_job_post(self, job_id, **kwargs):
        """Update job post details dynamically."""
        update_fields = []
        params = []

        for key, value in kwargs.items():
            update_fields.append(f"{key} = %s")
            params.append(value)

        params.append(job_id)
        query = f"UPDATE realtimejobs_jobpost SET {', '.join(update_fields)}, updated_at = NOW() WHERE id = %s;"
        print(f"[INFO] Updating job post ID: {job_id}")
        self.execute_query(query, tuple(params))

    def delete_job_post(self, job_id):
        """Delete a job post by ID."""
        query = "DELETE FROM realtimejobs_jobpost WHERE id = %s;"
        print(f"[INFO] Deleting job post with ID: {job_id}")
        self.execute_query(query, (job_id,))

if __name__ == "__main__":
    job_queries = JobPostQueries()

    # Fetch all jobs
    print("\n=== Fetching All Job Posts ===")
    all_jobs = job_queries.fetch_all_jobs()
    for job in all_jobs:
        print(job)

    # Find a job by ID (replace with an actual job ID)
    job_id = "your-job-id-here"
    if job_id:
        print(f"\n=== Fetching Job with ID: {job_id} ===")
        job = job_queries.find_job_by_id(job_id)
        print(job)

    # Find a job by Slug
    job_slug = "your-job-slug-here"
    if job_slug:
        print(f"\n=== Fetching Job with Slug: {job_slug} ===")
        job_by_slug = job_queries.find_job_by_slug(job_slug)
        print(job_by_slug)

    # Fetch jobs by category
    category_id = "your-category-id-here"
    if category_id:
        print(f"\n=== Fetching Jobs in Category ID: {category_id} ===")
        category_jobs = job_queries.fetch_jobs_by_category(category_id)
        for job in category_jobs:
            print(job)

    # Fetch jobs by company
    company_id = "your-company-id-here"
    if company_id:
        print(f"\n=== Fetching Jobs for Company ID: {company_id} ===")
        company_jobs = job_queries.fetch_jobs_by_company(company_id)
        for job in company_jobs:
            print(job)

    # Search jobs by keyword
    search_keyword = "developer"
    if search_keyword:
        print(f"\n=== Searching Jobs with Keyword: {search_keyword} ===")
        search_results = job_queries.search_jobs(search_keyword)
        for job in search_results:
            print(job)

    # Fetch remote jobs
    print("\n=== Fetching Remote Jobs ===")
    remote_jobs = job_queries.fetch_remote_jobs()
    for job in remote_jobs:
        print(job)

    # Fetch jobs by location
    location = "New York"
    if location:
        print(f"\n=== Fetching Jobs in Location: {location} ===")
        location_jobs = job_queries.fetch_jobs_by_location(location)
        for job in location_jobs:
            print(job)

    # Fetch jobs by salary range
    min_salary = "50000"
    max_salary = "100000"
    print(f"\n=== Fetching Jobs with Salary Range {min_salary} - {max_salary} ===")
    salary_jobs = job_queries.fetch_jobs_by_salary_range(min_salary, max_salary)
    for job in salary_jobs:
        print(job)

    # Add a new job post
    print("\n=== Adding a New Job Post ===")
    job_queries.add_job_post(
        title="Software Engineer",
        slug="software-engineer",
        location="Remote",
        is_worldwide=True,
        category_id="your-category-id-here",
        company_id="your-company-id-here",
        job_type_id="your-job-type-id-here",
        salary="$80K - $120K",
        short_description="Exciting software engineer position",
        description="We are looking for a skilled software engineer...",
        job_url="https://example.com/job/software-engineer",
        user_id="your-user-id-here"
    )
    print("Job added successfully.")

    # Update a job post (replace job_id with a valid ID)
    job_id = "your-job-id-here"
    if job_id:
        print("\n=== Updating a Job Post ===")
        job_queries.update_job_post(
            job_id=job_id,
            salary="$90K - $130K",
            location="San Francisco"
        )
        print("Job updated successfully.")

    # Delete a job post (replace job_id with a valid ID)
    job_id = "your-job-id-here"
    if job_id:
        print("\n=== Deleting a Job Post ===")
        job_queries.delete_job_post(job_id)
        print("Job deleted successfully.")

    
