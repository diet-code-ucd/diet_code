import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import CourseSelection from "./CourseSelection.tsx";
import DisplayQuestionTest from "./DisplayQuestionTest.tsx";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TestPage from "./DisplayTest.tsx";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <Router>
    <Routes>
      <Route path="/CourseSelection" Component={CourseSelection} />
      <Route path="/test" Component={TestPage} />
    </Routes>
    <React.StrictMode>
      <CourseSelection
        courses={[]}
        onSelectCourses={function (
          courseIds: number,
          difficulty: number
        ): void {
          throw new Error("Function not implemented.");
        }}
      />
    </React.StrictMode>
  </Router>
);
