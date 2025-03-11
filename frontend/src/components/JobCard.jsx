export function JobCard({ job }) {
    return (
      <div
        className={`overflow-hidden rounded-xl border bg-white shadow-md hover:cursor-pointer hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700/50 ${job.featured ? "border-orange-300 dark:border-orange-700" : ""}`}
      >
        <div className="p-4 sm:p-6 space-y-4">
          <div className="flex md:items-center flex-col md:flex-row">
            <div className="grow md:max-w-[54%] lg:max-w-[65%] xl:max-w-[74%]">
              <div className="flex gap-4">
                {job.companyLogo ? (
                  <img
                    src={job.companyLogo || "/placeholder.svg"}
                    alt={`${job.company} logo`}
                    className="rounded-full bg-white h-[64px] object-contain min-w-[64px]"
                    width={64}
                    height={64}
                  />
                ) : (
                  <div className="text-lg font-bold text-center overflow-clip flex items-center justify-center rounded-full text-black bg-white h-[64px] object-contain min-w-[64px] max-w-[64px]">
                    <p className="break-words w-[95%]">{job.companyInitials || job.company.substring(0, 2)}</p>
                  </div>
                )}
  
                <div className="grow">
                  <h3 className="font-semibold tracking-tight text-lg">{job.title}</h3>
                  <p className="md:hidden text-sm text-gray-500 dark:text-gray-400">{job.company}</p>
  
                  <div className="flex justify-start md:hidden items-center text-sm text-gray-500 dark:text-gray-400 md:mt-0 mt-2">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-1 h-3 w-3 flex-shrink-0"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="12 6 12 12 16 14" />
                    </svg>
                    <span className="truncate">{job.postedTime}</span>
                  </div>
  
                  <div className="mt-1 gap-2 hidden md:flex flex-wrap">
                    <p className="text-sm text-gray-500 dark:text-gray-400 mr-4">{job.company}</p>
                    {job.tags.slice(0, 4).map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors bg-white/40 dark:bg-black/40 cursor-pointer hover:bg-orange-500 hover:text-white dark:hover:bg-orange-500 dark:hover:text-white"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
  
              <p className="mt-2 ml-20 text-sm text-gray-500 dark:text-gray-400">{job.description}</p>
  
              <div className="mt-4 flex gap-2 flex-wrap md:hidden">
                {job.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors cursor-pointer hover:bg-orange-500 hover:text-white dark:hover:bg-orange-500 dark:hover:text-white"
                  >
                    {tag}
                  </span>
                ))}
              </div>
  
              <div className="flex gap-4 mt-2 md:mt-4 flex-wrap">
                <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="12"
                    height="12"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="mr-1 h-3 w-3 flex-shrink-0"
                  >
                    <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg>
                  <span className="truncate">{job.location}</span>
                </div>
  
                <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="12"
                    height="12"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="mr-1 h-3 w-3 flex-shrink-0"
                  >
                    <rect width="20" height="14" x="2" y="7" rx="2" ry="2" />
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                  </svg>
                  <span className="truncate">{job.jobType}</span>
                </div>
  
                <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="12"
                    height="12"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="mr-1 h-3 w-3 flex-shrink-0"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <circle cx="12" cy="12" r="6" />
                    <circle cx="12" cy="12" r="2" />
                  </svg>
                  <span className="truncate">{job.category}</span>
                </div>
  
                {job.salary && (
                  <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-1 h-3 w-3 flex-shrink-0"
                    >
                      <rect width="20" height="14" x="2" y="5" rx="2" />
                      <line x1="2" x2="22" y1="10" y2="10" />
                    </svg>
                    <span className="truncate">{job.salary}</span>
                  </div>
                )}
              </div>
            </div>
  
            <div className="flex md:flex-row flex-col gap-2 md:gap-16 md:ml-auto">
              <div className="hidden md:flex items-center text-sm text-gray-500 dark:text-gray-400 md:mt-0 mt-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="12"
                  height="12"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="mr-1 h-3 w-3 flex-shrink-0"
                >
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
                <span className="truncate">{job.postedTime}</span>
              </div>
  
              <button className="w-full md:w-auto md:mt-0 mt-2 px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }
  
  