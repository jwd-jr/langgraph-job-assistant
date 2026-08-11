import { useState } from 'react'
import './App.css'

function App() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchJobs = async () => {
    setLoading(true)
    const response = await fetch("http://localhost:8000/search-jobs")
    const data = await response.json()
    setJobs(data.tracked_jobs)
    setLoading(false)
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

  const updateStatus = async (jobId, newStatus) => {
    await fetch(`http://localhost:8000/update-status?job_id=${jobId}&new_status=${newStatus}`, {
      method: "POST"
    })

    setJobs((prevJobs) =>
      prevJobs.map((job) =>
        job.job_id === jobId ? { ...job, status: newStatus } : job
      )
    )
  }

  const scoreColor = (score) => {
    if (score >= 7) return "score-high"
    if (score >= 4) return "score-mid"
    return "score-low"
  }

  return (
    <div className="container">
      <h1>Job Assistant</h1>

      <input type="file" onChange={uploadResume} accept=".pdf,.docx,.txt" />

      <button className="search-btn" onClick={fetchJobs}>
        {loading ? "Searching..." : "Search Jobs"}
      </button>

      {jobs.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Company</th>
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
                <td className={scoreColor(job.score)}>{job.score}</td>
                <td>{job.reason}</td>
                <td>{job.status}</td>
                <td>
                  <button onClick={() => updateStatus(job.job_id, "applied")}>Apply</button>
                  <button onClick={() => updateStatus(job.job_id, "rejected")}>Reject</button>
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