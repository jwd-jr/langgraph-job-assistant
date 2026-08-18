import { useState } from 'react'
import './App.css'

function App() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const fetchJobs = async () => {
    setLoading(true)
    const response = await fetch("http://localhost:8000/search-jobs")
    const data = await response.json()
    setJobs(data.tracked_jobs)
    setLoading(false)
    setSearched(true)
  }

  const uploadResume = async (event) => {
    const file = event.target.files[0]
    const formData = new FormData()
    formData.append("file", file)

    const response = await fetch("http://localhost:8000/upload-resume", {
      method: "POST",
      body: formData
    })

    const data = await response.json()
    alert(data.message)
  }

  const updateStatus = async (jobTitle, employerName, newStatus) => {
    await fetch(`http://localhost:8000/update-status?job_title=${encodeURIComponent(jobTitle)}&employer_name=${encodeURIComponent(employerName)}&new_status=${newStatus}`, {
      method: "POST"
    })

    setJobs((prevJobs) =>
      prevJobs.map((job) =>
        job.job_title === jobTitle && job.employer_name === employerName
          ? { ...job, status: newStatus }
          : job
      )
    )
  }

  const scoreColor = (score) => {
    if (score >= 7) return "score-high"
    if (score >= 4) return "score-mid"
    return "score-low"
  }

  const statusBadgeClass = (status) => {
    if (status === "applied") return "badge badge-applied"
    if (status === "rejected") return "badge badge-rejected"
    return "badge badge-pending"
  }

  const appliedCount = jobs.filter((j) => j.status === "applied").length
  const rejectedCount = jobs.filter((j) => j.status === "rejected").length

  return (
    <div className="container">
      <h1>Job Assistant</h1>

      <input type="file" onChange={uploadResume} accept=".pdf,.docx,.txt" />

      <button className="search-btn" onClick={fetchJobs} disabled={loading}>
        {loading ? "Searching..." : "Search Jobs"}
      </button>

      {jobs.length > 0 && (
        <div className="stats-bar">
          <div className="stat">
            <span className="stat-number">{jobs.length}</span>
            <span className="stat-label">Total Jobs</span>
          </div>
          <div className="stat">
            <span className="stat-number stat-applied">{appliedCount}</span>
            <span className="stat-label">Applied</span>
          </div>
          <div className="stat">
            <span className="stat-number stat-rejected">{rejectedCount}</span>
            <span className="stat-label">Rejected</span>
          </div>
        </div>
      )}

      {!searched && !loading && (
        <p className="empty-state">Upload your resume and click "Search Jobs" to get started.</p>
      )}

      {jobs.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Company</th>
              <th>Location</th>
              <th>Posted</th>
              <th>Score</th>
              <th>Reason</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.job_id}>
                <td>{job.job_title}</td>
                <td>{job.employer_name}</td>
                <td>{job.job_location || "N/A"}</td>
                <td>{job.job_posted_at || "N/A"}</td>
                <td className={scoreColor(job.score)}>{job.score}</td>
                <td>{job.reason}</td>
                <td><span className={statusBadgeClass(job.status)}>{job.status}</span></td>
                <td>
                  <button className="apply-btn" onClick={() => updateStatus(job.job_title, job.employer_name, "applied")}>Apply</button>
                  <button className="reject-btn" onClick={() => updateStatus(job.job_title, job.employer_name, "rejected")}>Reject</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default App