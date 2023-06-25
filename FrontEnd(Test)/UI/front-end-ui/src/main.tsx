import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import CourseSelection from "./CourseSelection.tsx";
import DisplayQuestionTest from "./DisplayQuestionTest.tsx";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <CourseSelection
      courses={[]}
      onSelectCourses={function (courseIds: number, difficulty: number): void {
        throw new Error("Function not implemented.");
      }}
    />
    {/* <DisplayQuestionTest /> */}
  </React.StrictMode>
);
