from base_query import BaseQuery

class CompanyQueries(BaseQuery):
    """
    Handles queries related to the Company table.
    Inherits from BaseQuery to use MySQL database connection and caching.
    """

    def fetch_all_companies(self):
        """Retrieve all companies."""
        query = "SELECT id, name, logo, description, updated_at, contact_name, contact_email FROM realtimejobs_company;"
        print("[INFO] Fetching all companies")
        return self.fetch_all(query)

    def find_company_by_id(self, company_id):
        """Find a company by its ID."""
        query = """
            SELECT id, name, logo, description, updated_at, contact_name, contact_email
            FROM realtimejobs_company
            WHERE id = %s
            LIMIT 1;
        """
        print(f"[INFO] Searching for company with ID: {company_id}")
        return self.fetch_one(query, (company_id,))

    def find_company_by_name(self, name):
        """Find a company by its name."""
        query = """
            SELECT id, name, logo, description, updated_at, contact_name, contact_email
            FROM realtimejobs_company
            WHERE name = %s
            LIMIT 1;
        """
        print(f"[INFO] Searching for company with name: {name}")
        return self.fetch_one(query, (name,))

    def get_recent_companies(self, limit=10):
        """Get the most recently updated companies."""
        query = """
            SELECT id, name, logo, description, updated_at, contact_name, contact_email
            FROM realtimejobs_company
            ORDER BY updated_at DESC
            LIMIT %s;
        """
        print(f"[INFO] Fetching latest {limit} updated companies")
        return self.fetch_all(query, (limit,))

    def fetch_companies_with_jobs(self):
        """Fetch companies along with their job postings."""
        query = """
            SELECT c.id, c.name, c.logo, c.description, c.contact_name, c.contact_email, 
                   j.id AS job_id, j.title AS job_title, j.job_url
            FROM realtimejobs_company c
            LEFT JOIN job_post j ON c.id = j.company_id;
        """
        print("[INFO] Fetching companies with their job postings")
        return self.fetch_all(query)
    

    def update_company_details(self, company_id, name=None, logo=None, description=None, contact_name=None, contact_email=None):
        """Update company details dynamically."""
        update_fields = []
        params = []

        if name:
            update_fields.append("name = %s")
            params.append(name)
        if logo:
            update_fields.append("logo = %s")
            params.append(logo)
        if description:
            update_fields.append("description = %s")
            params.append(description)
        if contact_name:
            update_fields.append("contact_name = %s")
            params.append(contact_name)
        if contact_email:
            update_fields.append("contact_email = %s")
            params.append(contact_email)

        params.append(company_id)
        query = f"""
            UPDATE realtimejobs_company
            SET {", ".join(update_fields)}
            WHERE id = %s;
        """
        print(f"[INFO] Updating company ID: {company_id}")
        self.execute_query(query, tuple(params))

    def delete_company(self, company_id):
        """Delete a company by ID."""
        query = "DELETE FROM realtimejobs_company WHERE id = %s;"
        print(f"[INFO] Deleting company with ID: {company_id}")
        self.execute_query(query, (company_id,))

if __name__ == "__main__":
    company_queries = CompanyQueries()

    # Fetch all companies
    all_companies = company_queries.fetch_all_companies()
    print(all_companies)

    # Find a company by ID
    company = company_queries.find_company_by_id("some-uuid")
    print(company)

    # Find a company by name
    company = company_queries.find_company_by_name("TechCorp")
    print(company)

    # Get latest 5 companies
    latest_companies = company_queries.get_recent_companies(5)
    print(latest_companies)

    # Fetch companies with jobs
    companies_with_jobs = company_queries.fetch_companies_with_jobs()
    print(companies_with_jobs)


    # Update a company
    company_queries.update_company_details("some-uuid", name="UpdatedTech", description="Updated description")

    # Delete a company
    company_queries.delete_company("some-uuid")
