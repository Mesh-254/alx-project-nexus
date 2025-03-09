from realtimejobs.queries.base_query import BaseQuery

class JobPostQueries(BaseQuery):
    """
    Handles queries related to the realtimejobs_jobpost table.
    """

    def fetch_filtered_jobs(self, categories=None, locations=None, job_types=None, page=1, page_size=15):
        """Fetch job posts based on multiple filters with pagination."""
        query = """
            SELECT id, title, slug, location, is_worldwide, category_id, company_id, job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            WHERE 1=1
        """
        params = []

        if categories:
            query += " AND category_id IN %s"
            params.append(tuple(categories))

        if locations:
            query += " AND location IN %s"
            params.append(tuple(locations))

        if job_types:
            query += " AND job_type_id IN %s"
            params.append(tuple(job_types))

        query += " ORDER BY created_at DESC LIMIT %s OFFSET %s;"
        params.extend([page_size, (page - 1) * page_size])

        return self.fetch_all(query, tuple(params))
