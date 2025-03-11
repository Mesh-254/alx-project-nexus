from realtimejobs.queries.base_query import BaseQuery


class JobPostQueries(BaseQuery):
    """
    Handles queries related to the realtimejobs_jobpost table.
    """

    def fetch_filtered_jobs(self, categories=None, locations=None, job_types=None, page=1, page_size=15):
        """Fetch job posts based on multiple filters with pagination."""
        query = """
            SELECT 
                jp.id, 
                jp.title, 
                jp.slug, 
                jp.location, 
                jp.is_worldwide, 
                c.name AS category,  -- Fetch category name
                jt.name AS job_type,  -- Fetch job type name
                comp.name AS company_name,  -- Fetch company name
                jp.salary, 
                jp.short_description, 
                jp.created_at
            FROM realtimejobs_jobpost jp
            LEFT JOIN realtimejobs_category c ON jp.category_id = c.id  -- Join categories table
            LEFT JOIN realtimejobs_jobtype jt ON jp.job_type_id = jt.id  -- Join job types table
            LEFT JOIN realtimejobs_company comp ON jp.company_id = comp.id  -- Join company table
            WHERE jp.status = 'published'
        """
        params = []

        if categories:
            query += " AND jp.category_id IN %s"
            params.append(tuple(categories))

        if locations:
            query += " AND jp.location IN %s"
            params.append(tuple(locations))

        if job_types:
            query += " AND jp.job_type_id IN %s"
            params.append(tuple(job_types))

        query += " ORDER BY jp.created_at DESC LIMIT %s OFFSET %s;"
        params.extend([page_size, (page - 1) * page_size])

        return self.fetch_all(query, tuple(params))
