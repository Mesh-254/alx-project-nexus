from base_query import BaseQuery

class CategoryQueries(BaseQuery):
    """
    Handles queries related to the realtimejobs_category table.
    Inherits from BaseQuery to use MySQL database connection and caching.
    """

    def fetch_all_categories(self):
        """Retrieve all categories."""
        query = "SELECT id, name, slug FROM realtimejobs_category;"
        print("[INFO] Fetching all categories")
        return self.fetch_all(query)

    def find_category_by_id(self, category_id):
        """Find a category by its ID."""
        query = "SELECT id, name, slug FROM realtimejobs_category WHERE id = %s LIMIT 1;"
        print(f"[INFO] Searching for category with ID: {category_id}")
        return self.fetch_one(query, (category_id,))

    def find_category_by_name(self, name):
        """Find a category by its name."""
        query = "SELECT id, name, slug FROM realtimejobs_category WHERE name = %s LIMIT 1;"
        print(f"[INFO] Searching for category with name: {name}")
        return self.fetch_one(query, (name,))

    def find_category_by_slug(self, slug):
        """Find a category by its slug."""
        query = "SELECT id, name, slug FROM realtimejobs_category WHERE slug = %s LIMIT 1;"
        print(f"[INFO] Searching for category with slug: {slug}")
        return self.fetch_one(query, (slug,))

    def add_category(self, name, slug):
        """Insert a new category."""
        query = "INSERT INTO realtimejobs_category (name, slug) VALUES (%s, %s);"
        print(f"[INFO] Adding new category: {name}")
        self.execute_query(query, (name, slug))

    def update_category(self, category_id, name=None, slug=None):
        """Update category details dynamically."""
        update_fields = []
        params = []

        if name:
            update_fields.append("name = %s")
            params.append(name)
        if slug:
            update_fields.append("slug = %s")
            params.append(slug)

        params.append(category_id)
        query = f"UPDATE realtimejobs_category SET {', '.join(update_fields)} WHERE id = %s;"
        print(f"[INFO] Updating category ID: {category_id}")
        self.execute_query(query, tuple(params))

    def delete_category(self, category_id):
        """Delete a category by ID."""
        query = "DELETE FROM realtimejobs_category WHERE id = %s;"
        print(f"[INFO] Deleting category with ID: {category_id}")
        self.execute_query(query, (category_id,))

    def fetch_jobs_by_category(self, category_id):
        """Fetch all job postings under a given category."""
        query = """
            SELECT j.id, j.title, j.company_id, j.description, j.job_url, j.posted_at
            FROM realtimejobs_jobpost j
            WHERE j.category_id = %s
            ORDER BY j.posted_at DESC;
        """
        print(f"[INFO] Fetching jobs for category ID: {category_id}")
        return self.fetch_all(query, (category_id,))

    def fetch_categories_with_job_count(self):
        """Fetch categories along with the number of jobs posted under each."""
        query = """
            SELECT c.id, c.name, c.slug, COUNT(j.id) AS job_count
            FROM realtimejobs_category c
            LEFT JOIN realtimejobs_jobpost j ON c.id = j.category_id
            GROUP BY c.id, c.name, c.slug
            ORDER BY job_count DESC;
        """
        print("[INFO] Fetching categories with job counts")
        return self.fetch_all(query)

    def fetch_popular_categories(self, limit=5):
        """Fetch the most popular categories based on job postings count."""
        query = """
            SELECT c.id, c.name, c.slug, COUNT(j.id) AS job_count
            FROM realtimejobs_category c
            LEFT JOIN realtimejobs_jobpost j ON c.id = j.category_id
            GROUP BY c.id, c.name, c.slug
            ORDER BY job_count DESC
            LIMIT %s;
        """
        print(f"[INFO] Fetching top {limit} popular categories")
        return self.fetch_all(query, (limit,))

    def fetch_recently_active_categories(self, days=30):
        """Fetch categories where job postings were added in the last `days` days."""
        query = """
            SELECT DISTINCT c.id, c.name, c.slug
            FROM realtimejobs_category c
            JOIN realtimejobs_jobpost j ON c.id = j.category_id
            WHERE j.posted_at >= NOW() - INTERVAL %s DAY;
        """
        print(f"[INFO] Fetching categories with job postings in the last {days} days")
        return self.fetch_all(query, (days,))
if __name__ == "__main__":
    category_queries = CategoryQueries()

    # Fetch all categories
    all_categories = category_queries.fetch_all_categories()
    print(all_categories)

    # Find a category by ID
    category = category_queries.find_category_by_id("some-uuid")
    print(category)

    # Fetch jobs under a specific category
    jobs = category_queries.fetch_jobs_by_category("some-uuid")
    print(jobs)

    # Fetch popular categories
    popular_categories = category_queries.fetch_popular_categories(5)
    print(popular_categories)
