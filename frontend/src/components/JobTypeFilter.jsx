"use client";

import { useState, useRef, useEffect } from "react";
import axios from "axios";

export function JobTypeFilter({ selectedJobTypes, setSelectedJobTypes }) {
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [jobTypes, setJobTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const dropdownRef = useRef(null);
  const API_URL = import.meta.env.VITE_API_URL;

  // Fetch job types from the backend
  useEffect(() => {
    const fetchJobTypes = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}jobtypes/`);

        // Check the structure of the response and extract job types accordingly
        let jobTypesData = [];

        if (Array.isArray(response.data)) {
          // If response.data is already an array
          jobTypesData = response.data;
        } else if (response.data && typeof response.data === "object") {
          // If response.data is an object, look for common properties that might contain the job types
          if (Array.isArray(response.data.job_types)) {
            jobTypesData = response.data.job_types;
          } else if (Array.isArray(response.data.results)) {
            jobTypesData = response.data.results;
          } else if (Array.isArray(response.data.data)) {
            jobTypesData = response.data.data;
          } else {
            // If we can't find a job types array, log an error
            console.error("Unexpected API response structure:", response.data);
            setError("Unexpected API response format");
            setJobTypes([]);
            setLoading(false);
            return;
          }
        } else {
          console.error("Unexpected API response type:", typeof response.data);
          setError("Invalid API response");
          setJobTypes([]);
          setLoading(false);
          return;
        }

        // Transform the job types data to match the expected format
        const formattedJobTypes = jobTypesData.map((jobType) => ({
          value: jobType.id || jobType._id || jobType.value,
          label: jobType.name || jobType.title || jobType.label,
        }));

        setJobTypes(formattedJobTypes);
        setError(null);
      } catch (err) {
        console.error("Error fetching job types:", err);
        setError("Failed to load job types");
        // Fallback to hardcoded job types if API fails
        setJobTypes([
          { value: "Full-time", label: "Full-time" },
          { value: "Part-time", label: "Part-time" },
          { value: "Contract", label: "Contract" },
          { value: "Freelance", label: "Freelance" },
          { value: "Internship", label: "Internship" },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchJobTypes();
  }, []);

  const toggleJobType = (jobType) => {
    // Get the job type label instead of the value
    const jobTypeLabel = jobTypes.find((t) => t.value === jobType)?.label;

    if (selectedJobTypes.includes(jobTypeLabel)) {
      setSelectedJobTypes(selectedJobTypes.filter((t) => t !== jobTypeLabel));
    } else {
      setSelectedJobTypes([...selectedJobTypes, jobTypeLabel]);
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownRef]);

  const filteredJobTypes = jobTypes.filter((jobType) =>
    jobType.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="relative w-full" ref={dropdownRef}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center px-4 py-2 text-left text-white border border-gray-300 rounded-md bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-orange-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:bg-gray-700"
      >
        {selectedJobTypes.length > 0
          ? `${selectedJobTypes.length} job types selected`
          : "📄 Select Job Type..."}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="ml-2 h-4 w-4 shrink-0 opacity-50"
        >
          <path d="m7 15 5 5 5-5" />
          <path d="m7 9 5-5 5 5" />
        </svg>
      </button>

      {open && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg dark:bg-gray-800 dark:border-gray-700">
          {selectedJobTypes.length > 0 && (
            <div className="flex flex-wrap gap-1 p-2 border-b dark:border-gray-700">
              {selectedJobTypes.map((jobType) => (
                <span
                  key={jobType}
                  className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-semibold text-gray-800 cursor-pointer dark:bg-gray-700 dark:text-gray-200"
                  onClick={() =>
                    setSelectedJobTypes(
                      selectedJobTypes.filter((t) => t !== jobType)
                    )
                  }
                >
                  {jobType}
                  <span className="ml-1">×</span>
                </span>
              ))}
              {selectedJobTypes.length > 0 && (
                <span
                  className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold cursor-pointer dark:border-gray-600"
                  onClick={() => setSelectedJobTypes([])}
                >
                  Clear all
                </span>
              )}
            </div>
          )}

          <div className="p-2">
            <input
              type="text"
              placeholder="Search job types..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="max-h-64 overflow-y-auto">
            {loading ? (
              <div className="px-3 py-4 text-center">
                <div className="inline-block animate-spin rounded-full h-5 w-5 border-b-2 border-orange-500"></div>
                <p className="mt-2 text-sm text-gray-500">
                  Loading job types...
                </p>
              </div>
            ) : error ? (
              <div className="px-3 py-4 text-center text-red-500">
                <p>{error}</p>
                <button
                  onClick={() => window.location.reload()}
                  className="mt-2 text-sm text-orange-500 hover:underline"
                >
                  Try again
                </button>
              </div>
            ) : filteredJobTypes.length === 0 ? (
              <div className="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">
                No job type found.
              </div>
            ) : (
              <ul>
                {filteredJobTypes.map((jobType) => (
                  <li
                    key={jobType.value}
                    className="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center dark:hover:bg-gray-700"
                    onClick={() => toggleJobType(jobType.value)}
                  >
                    <div
                      className={`mr-2 h-4 w-4 flex items-center justify-center ${
                        selectedJobTypes.includes(jobType.label)
                          ? "text-orange-500"
                          : "text-transparent"
                      }`}
                    >
                      {selectedJobTypes.includes(jobType.label) && (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                    </div>
                    {jobType.label}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
