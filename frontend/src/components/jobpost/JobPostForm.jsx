"use client";

import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";


const API_URL = import.meta.env.VITE_API_URL;

// Rich text editor component
const RichTextEditor = ({ value, onChange, placeholder }) => {
  return (
    <div className="border border-gray-700 rounded overflow-hidden">
      <div className="flex bg-gray-800 p-2 border-b border-gray-700"></div>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full min-h-[200px] p-4 bg-gray-900 text-gray-200 border-none resize-y"
      />
    </div>
  );
};

const JobPostForm = () => {
  const navigate = useNavigate();

  // Form state
  const [formData, setFormData] = useState({
    // Job details
    job_url: "",
    title: "",
    location: "",
    is_worldwide: false,
    category: "",
    job_type: "",
    salary: "",
    description: "",
    short_description: "",

    // Company details
    company: "", // This will be the company ID if selected from existing
    companyName: "",
    companyLogo: null,
    companyDescription: "",
    contact_name: "",
    contact_email: "",

    // For company search
    isExistingCompany: false,
    searchTerm: "",
  });


  // Reference states
  const [categories, setCategories] = useState([]);
  const [jobTypes, setJobTypes] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [filteredCompanies, setFilteredCompanies] = useState([]);
  const [showCompanyDropdown, setShowCompanyDropdown] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const companyDropdownRef = useRef(null);

  // Fetch reference data on component mount
  useEffect(() => {
    const fetchReferenceData = async () => {
      try {
        setIsLoading(true);
        const [categoriesRes, jobTypesRes, companiesRes] = await Promise.all([
          axios.get(`${API_URL}categories/`),
          axios.get(`${API_URL}jobtypes/`),
          axios.get(`${API_URL}companies/`),
        ]);

        console.log(categoriesRes.data)
        console.log(jobTypesRes.data)

        // Extract data from response, handling both array and {results: []} formats
        const extractData = (response) => {
          if (response.data && Array.isArray(response.data)) {
            return response.data;
          } else if (response.data && Array.isArray(response.data.results)) {
            return response.data.results;
          }
          return [];
        };

        setCategories(extractData(categoriesRes));
        setJobTypes(extractData(jobTypesRes));
        setCompanies(extractData(companiesRes));
      } catch (error) {
        console.error("Error fetching reference data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchReferenceData();
  }, []);

  // Close company dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        companyDropdownRef.current &&
        !companyDropdownRef.current.contains(event.target)
      ) {
        setShowCompanyDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value, type, checked, files } = e.target;

    if (type === "checkbox") {
      setFormData({ ...formData, [name]: checked });
    } else if (type === "file") {
      setFormData({ ...formData, [name]: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }

    // Clear errors for this field
    if (errors[name]) {
      setErrors({ ...errors, [name]: null });
    }
  };

  // Handle rich text editor changes
  const handleEditorChange = (name, value) => {
    setFormData({ ...formData, [name]: value });

    // Clear errors for this field
    if (errors[name]) {
      setErrors({ ...errors, [name]: null });
    }
  };

  // Handle company search
  const handleCompanySearch = (e) => {
    const searchTerm = e.target.value;
    setFormData({ ...formData, searchTerm });

    if (searchTerm.length > 2) {
      const filtered = companies.filter((company) =>
        company.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredCompanies(filtered);
      setShowCompanyDropdown(true);
    } else {
      setFilteredCompanies([]);
      setShowCompanyDropdown(false);
    }
  };

  // Select existing company
  const selectCompany = (company) => {
    setFormData({
      ...formData,
      company: company.id,
      companyName: company.name,
      companyDescription: company.description || "",
      contact_name: company.contact_name || formData.contact_name,
      contact_email: company.contact_email || formData.contact_email,
      isExistingCompany: true,
      searchTerm: company.name,
    });
    setShowCompanyDropdown(false);
  };

  // Clear selected company
  const clearSelectedCompany = () => {
    setFormData({
      ...formData,
      company: "",
      companyName: "",
      companyDescription: "",
      isExistingCompany: false,
      searchTerm: "",
    });
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};

    // Job validation
    if (!formData.job_url) newErrors.job_url = "Job URL is required";
    if (!formData.title) newErrors.title = "Job title is required";
    if (!formData.location && !formData.is_worldwide)
      newErrors.location = "Location is required if not worldwide";
    if (!formData.category) newErrors.category = "Category is required";
    if (!formData.job_type) newErrors.job_type = "Job type is required";
    if (!formData.description)
      newErrors.description = "Job description is required";
    if (!formData.short_description)
      newErrors.short_description = "Short description is required";
    if (formData.short_description && formData.short_description.length > 200) {
      newErrors.short_description =
        "Short description must be less than 200 characters";
    }

    // Company validation
    if (!formData.isExistingCompany) {
      if (!formData.companyName)
        newErrors.companyName = "Company name is required";
      if (!formData.contact_name)
        newErrors.contact_name = "Contact name is required";
      if (!formData.contact_email)
        newErrors.contact_email = "Contact email is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      // Scroll to the first error
      const firstError = document.querySelector(".text-red-500");
      if (firstError) {
        firstError.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      return;
    }

    try {
      setIsLoading(true);

      let companyId = formData.company;

      // If not using an existing company, create a new one
      if (!formData.isExistingCompany) {
        const companyFormData = new FormData();
        companyFormData.append("name", formData.companyName);
        companyFormData.append("description", formData.companyDescription);
        companyFormData.append("contact_name", formData.contact_name);
        companyFormData.append("contact_email", formData.contact_email);

        if (formData.companyLogo) {
          companyFormData.append("logo", formData.companyLogo);
        }

        const companyResponse = await axios.post(
          `${API_URL}companies/`,
          companyFormData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        companyId = companyResponse.data.id;
      }

      // Create job post
      const jobPostData = {
        job_url: formData.job_url,
        title: formData.title,
        location: formData.location,
        is_worldwide: formData.is_worldwide,
        category: `${API_URL}categories/${formData.category}/`,
        job_type: `${API_URL}jobtypes/${formData.job_type}/`,
        salary: formData.salary,
        description: formData.description,
        short_description: formData.short_description,
        company: `${API_URL}companies/${companyId}/`,
      };
      console.log(jobPostData)

      // The job post creation will redirect to payment page
      const response = await axios.post(
        `${API_URL}jobposts/`,
        jobPostData
      );

      // If we get here, it means the redirect didn't happen automatically
      // We can manually redirect to the payment URL if it's in the response
      if (response.data && response.data.checkout_url) {
        window.location.href = response.data.checkout_url;
      }
    } catch (error) {
      console.error("Error submitting form:", error);

      // Handle validation errors from the server
      if (error.response && error.response.data) {
        setErrors({ ...errors, ...error.response.data });
      } else {
        alert("An error occurred while submitting the form. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full mx-auto px-4 py-8 bg-gray-950 text-gray-200">
      <div className="text-center mb-8">
        <h1 className="text-4xl md:text-5xl font-bold text-orange-500 mb-2">
          Post a Job Today for $20.
        </h1>
        <h2 className="text-2xl md:text-3xl font-normal text-orange-500">
          Reach Thousands of Remote Candidates!
        </h2>
      </div>

      <form
        onSubmit={handleSubmit}
        className="bg-black bg-opacity-30 border border-gray-800 rounded-lg overflow-hidden"
      >
        {/* Job Details Section */}
        <div className="p-6 border-b border-gray-800">
          <h2 className="text-xl font-semibold mb-6">Job Details</h2>

          <div className="mb-6">
            <label htmlFor="job_url" className="block mb-2 font-medium">
              Job URL <span className="text-orange-500">*</span>
            </label>
            <input
              type="url"
              id="job_url"
              name="job_url"
              value={formData.job_url}
              onChange={handleChange}
              placeholder="https://company-name.com/jobs/your-job-title"
              className={`w-full p-3 bg-gray-900 border ${
                errors.job_url ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
            />
            {errors.job_url && (
              <div className="mt-1 text-red-500 text-sm">{errors.job_url}</div>
            )}
          </div>

          <div className="mb-6">
            <label htmlFor="title" className="block mb-2 font-medium">
              Job Title <span className="text-orange-500">*</span>
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="eg: Software Engineer, Virtual Assistant"
              className={`w-full p-3 bg-gray-900 border ${
                errors.title ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
            />
            {errors.title && (
              <div className="mt-1 text-red-500 text-sm">{errors.title}</div>
            )}
          </div>

          <div className="mb-6">
            <label htmlFor="location" className="block mb-2 font-medium">
              Location <span className="text-orange-500">*</span>
            </label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="eg: USA, Egypt"
              disabled={formData.is_worldwide}
              className={`w-full p-3 bg-gray-900 border ${
                errors.location ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500 ${
                formData.is_worldwide ? "opacity-50" : ""
              }`}
            />
            {errors.location && (
              <div className="mt-1 text-red-500 text-sm">{errors.location}</div>
            )}

            <div className="flex items-center mt-2">
              <input
                type="checkbox"
                id="is_worldwide"
                name="is_worldwide"
                checked={formData.is_worldwide}
                onChange={handleChange}
                className="mr-2 h-4 w-4"
              />
              <label htmlFor="is_worldwide" className="text-gray-300">
                Worldwide
              </label>
            </div>
          </div>

          <div className="mb-6">
            <label htmlFor="category" className="block mb-2 font-medium">
              Category <span className="text-orange-500">*</span>
            </label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              className={`w-full p-3 bg-gray-900 border ${
                errors.category ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
            >
              <option value="">Select a Category</option>
              {Array.isArray(categories) &&
                categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
            </select>
            {errors.category && (
              <div className="mt-1 text-red-500 text-sm">{errors.category}</div>
            )}
          </div>

          <div className="mb-6">
            <label htmlFor="job_type" className="block mb-2 font-medium">
              Job Type <span className="text-orange-500">*</span>
            </label>
            <select
              id="job_type"
              name="job_type"
              value={formData.job_type}
              onChange={handleChange}
              className={`w-full p-3 bg-gray-900 border ${
                errors.job_type ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
            >
              <option value="">Select Job Type</option>
              {Array.isArray(jobTypes) &&
                jobTypes.map((jobType) => (
                  <option key={jobType.id} value={jobType.id}>
                    {jobType.name}
                  </option>
                ))}
            </select>
            {errors.job_type && (
              <div className="mt-1 text-red-500 text-sm">{errors.job_type}</div>
            )}
          </div>

          <div className="mb-6">
            <label htmlFor="salary" className="block mb-2 font-medium">
              Salary{" "}
              <span className="text-gray-500 text-sm font-normal">
                (Optional)
              </span>
            </label>
            <input
              type="text"
              id="salary"
              name="salary"
              value={formData.salary}
              onChange={handleChange}
              placeholder="Preferred format: $USD per year, eg: $60K - $80K"
              className="w-full p-3 bg-gray-900 border border-gray-700 rounded-md text-gray-200 focus:outline-none focus:border-orange-500"
            />
          </div>

          <div className="mb-6">
            <label htmlFor="description" className="block mb-2 font-medium">
              Description <span className="text-orange-500">*</span>
            </label>
            <RichTextEditor
              value={formData.description}
              onChange={(value) => handleEditorChange("description", value)}
              placeholder="Type your Job Description either in normal mode or HTML mode..."
            />
            {errors.description && (
              <div className="mt-1 text-red-500 text-sm">
                {errors.description}
              </div>
            )}
          </div>

          <div className="mb-6">
            <label
              htmlFor="short_description"
              className="block mb-2 font-medium"
            >
              Short Description <span className="text-orange-500">*</span>
            </label>
            <input
              type="text"
              id="short_description"
              name="short_description"
              value={formData.short_description}
              onChange={handleChange}
              placeholder="Enter a brief one-sentence job description"
              maxLength={200}
              className={`w-full p-3 bg-gray-900 border ${
                errors.short_description ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
            />
            <div className="mt-1 text-right text-xs text-gray-500">
              {formData.short_description.length}/200 characters
            </div>
            {errors.short_description && (
              <div className="mt-1 text-red-500 text-sm">
                {errors.short_description}
              </div>
            )}
          </div>
        </div>

        {/* Company Details Section */}
        <div className="p-6 border-b border-gray-800">
          <h2 className="text-xl font-semibold mb-6">Company Details</h2>

          <div className="mb-6 relative" ref={companyDropdownRef}>
            <label htmlFor="searchTerm" className="block mb-2 font-medium">
              Search for existing company or create new
            </label>
            <input
              type="text"
              id="searchTerm"
              name="searchTerm"
              value={formData.searchTerm}
              onChange={handleCompanySearch}
              placeholder="Search for company name..."
              disabled={formData.isExistingCompany}
              className={`w-full p-3 bg-gray-900 border border-gray-700 rounded-md text-gray-200 focus:outline-none focus:border-orange-500 ${
                formData.isExistingCompany ? "opacity-50" : ""
              }`}
            />

            {showCompanyDropdown && filteredCompanies.length > 0 && (
              <div className="absolute z-10 mt-1 w-full bg-gray-900 border border-gray-700 rounded-md max-h-48 overflow-y-auto">
                {filteredCompanies.map((company) => (
                  <div
                    key={company.id}
                    className="p-3 hover:bg-gray-800 cursor-pointer"
                    onClick={() => selectCompany(company)}
                  >
                    {company.name}
                  </div>
                ))}
              </div>
            )}

            {formData.isExistingCompany && (
              <div className="mt-2 p-3 bg-orange-900 bg-opacity-20 border border-orange-800 border-opacity-30 rounded-md flex justify-between items-center">
                <span>
                  Using existing company:{" "}
                  <strong>{formData.companyName}</strong>
                </span>
                <button
                  type="button"
                  onClick={clearSelectedCompany}
                  className="text-orange-500 text-sm underline"
                >
                  Change
                </button>
              </div>
            )}
          </div>

          {!formData.isExistingCompany && (
            <>
              <div className="mb-6">
                <label htmlFor="companyName" className="block mb-2 font-medium">
                  Name <span className="text-orange-500">*</span>
                </label>
                <input
                  type="text"
                  id="companyName"
                  name="companyName"
                  value={formData.companyName}
                  onChange={handleChange}
                  placeholder="Your Company Name"
                  className={`w-full p-3 bg-gray-900 border ${
                    errors.companyName ? "border-red-500" : "border-gray-700"
                  } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
                />
                {errors.companyName && (
                  <div className="mt-1 text-red-500 text-sm">
                    {errors.companyName}
                  </div>
                )}
              </div>

              <div className="mb-6">
                <label htmlFor="companyLogo" className="block mb-2 font-medium">
                  Company Logo{" "}
                  <span className="text-gray-500 text-sm font-normal">
                    (Optional)
                  </span>
                </label>
                <div className="flex items-center">
                  <label className="flex-1 cursor-pointer p-3 bg-gray-900 border border-gray-700 rounded-md text-gray-400 hover:border-gray-600">
                    {formData.companyLogo
                      ? formData.companyLogo.name
                      : "Choose File"}
                    <input
                      type="file"
                      id="companyLogo"
                      name="companyLogo"
                      onChange={handleChange}
                      accept="image/*"
                      className="hidden"
                    />
                  </label>
                </div>
              </div>

              <div className="mb-6">
                <label
                  htmlFor="companyDescription"
                  className="block mb-2 font-medium"
                >
                  Company Description{" "}
                  <span className="text-gray-500 text-sm font-normal">
                    (Optional)
                  </span>
                </label>
                <RichTextEditor
                  value={formData.companyDescription}
                  onChange={(value) =>
                    handleEditorChange("companyDescription", value)
                  }
                  placeholder="Type your Company Description either in normal mode or HTML mode..."
                />
              </div>
            </>
          )}
        </div>

        {/* Contact Information Section */}
        <div className="p-6 border-b border-gray-800">
          <h2 className="text-xl font-semibold mb-6">Contact Information</h2>

          <div className="mb-6">
            <label htmlFor="contact_name" className="block mb-2 font-medium">
              Name <span className="text-orange-500">*</span>
            </label>
            <input
              type="text"
              id="contact_name"
              name="contact_name"
              value={formData.contact_name}
              onChange={handleChange}
              placeholder="Your Full Name"
              className={`w-full p-3 bg-gray-900 border ${
                errors.contact_name ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
            />
            {errors.contact_name && (
              <div className="mt-1 text-red-500 text-sm">
                {errors.contact_name}
              </div>
            )}
          </div>

          <div className="mb-6">
            <label htmlFor="contact_email" className="block mb-2 font-medium">
              Email <span className="text-orange-500">*</span>
            </label>
            <input
              type="email"
              id="contact_email"
              name="contact_email"
              value={formData.contact_email}
              onChange={handleChange}
              placeholder="Your Email"
              className={`w-full p-3 bg-gray-900 border ${
                errors.contact_email ? "border-red-500" : "border-gray-700"
              } rounded-md text-gray-200 focus:outline-none focus:border-orange-500`}
            />
            {errors.contact_email && (
              <div className="mt-1 text-red-500 text-sm">
                {errors.contact_email}
              </div>
            )}
          </div>
        </div>

        {/* Terms and Submit */}
        <div className="p-6">
          <ul className="list-disc pl-5 mb-6 text-sm text-gray-400">
            <li className="mb-2">
              Your job post will begive top priority
            </li>
            <li className="mb-2">
              You can only post one job at a time for $20 each.
            </li>
            <li className="mb-2">
              If you need to edit anything about your job post, please email us
              directly at{" "}
              <a
                href="mailto:realtimejobs@gmail.com"
                className="text-green-500"
              >
                team@realtimejobs.com
              </a>
              .
            </li>
          </ul>

          <button
            type="submit"
            className={`w-full py-4 px-6 rounded-md text-white font-semibold text-lg ${
              isLoading
                ? "bg-gray-600 cursor-not-allowed"
                : "bg-orange-600 hover:bg-orange-500"
            }`}
            disabled={isLoading}
          >
            {isLoading ? "Processing..." : "Pay Now ($20)"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default JobPostForm;
