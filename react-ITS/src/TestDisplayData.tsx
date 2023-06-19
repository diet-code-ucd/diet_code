import { useEffect, useState } from "react";

interface Employee {
  userId: string;
  jobTitle: string;
  firstName: string;
  lastName: string;
  employeeCode: string;
  region: string;
  phoneNumber: string;
  emailAddress: string;
}

function Display() {
  const [employees, setEmployees] = useState<Employee[]>([]);

  useEffect(() => {
    fetchData()
      .then((res) => {
        setEmployees(res);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  function fetchData(): Promise<Employee[]> {
    return fetch("/Sample-employee-JSON-data.json")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Request failed");
        }
        return res.json();
      })
      .then((res) => {
        return res.Employees as Employee[];
      });
  }

  return (
    <div>
      <h1>Employee List:</h1>
      {employees.map((employee) => (
        <div key={employee.userId}>
          <p>
            Name: {employee.firstName} {employee.lastName}
          </p>
          <p>Job Title: {employee.jobTitle}</p>
          <p>Employee Code: {employee.employeeCode}</p>
          <p>Region: {employee.region}</p>
          <p>Phone Number: {employee.phoneNumber}</p>
          <p>Email Address: {employee.emailAddress}</p>
          <hr />
        </div>
      ))}
    </div>
  );
}

export default Display;
