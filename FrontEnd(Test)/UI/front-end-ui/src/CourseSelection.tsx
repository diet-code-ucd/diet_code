import React, { useEffect, useState } from "react";
import axios from "axios";
import TestPage from "./DisplayTest";

interface Course {
  id: number;
  name: string;
  questions: number[];
}

interface CourseSelectionProps {
  courses: Course[]; // Add the 'courses' prop
  onSelectCourses: (courseIds: number, difficulty: number) => void;
}

const CourseSelection: React.FC<CourseSelectionProps> = ({
  onSelectCourses,
}) => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<number>();
  const [selectedDifficulty, setSelectedDifficulty] = useState("");
  const [submitDifficulty, setsubmitDifficulty] = useState<number>(0);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get("http://localhost:5057/api/Course");
      setCourses(response.data);
      console.log(response);
    } catch (error) {
      console.error("Error fetching courses:", error);
    }
  };

  const handleCourseChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    courseId: number
  ) => {
    const isChecked = event.target.checked;
    if (isChecked) {
      setSelectedCourseId(courseId); // Set the selected course ID directly
    } else {
      setSelectedCourseId(1); // Clear the selected course ID
    }
  };

  const handleDifficultyChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const difficulty = event.target.value;
    setSelectedDifficulty(difficulty);
    if (difficulty === "Easy") {
      setsubmitDifficulty(0);
    }
    if (difficulty === "Medium") {
      setsubmitDifficulty(1);
    }
    if (difficulty === "Hard") {
      setsubmitDifficulty(2);
    }
  };

  const handleTestStart = (event: React.FormEvent) => {
    event.preventDefault();
    if (selectedCourseId && submitDifficulty) {
      onSelectCourses(selectedCourseId, submitDifficulty); // Pass the selected course ID and difficulty to the parent component
    }
  };

  const handleTestSubmit = (courseIds: number, difficulty: number) => {
    // Handle the test submission
    console.log("Selected courses:", courseIds);
    console.log("Difficulty:", difficulty);
  };

  return (
    <form onSubmit={handleTestStart}>
      <div>
        <h3>Select Course:</h3>
        {courses.map((course) => (
          <div key={course.id}>
            <input
              type="radio"
              id={`course-${course.id}`}
              name="selectedCourse"
              value={course.id}
              checked={selectedCourseId === course.id}
              onChange={(event) => handleCourseChange(event, course.id)}
            />
            <label htmlFor={`course-${course.id}`}>{course.name}</label>
          </div>
        ))}
      </div>

      <div>
        <h3>Select Difficulty:</h3>
        <select value={selectedDifficulty} onChange={handleDifficultyChange}>
          <option value="">-- Select Difficulty --</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
        <button
          onClick={() => handleTestSubmit(selectedCourseId, submitDifficulty)}
          disabled={selectedCourseId === null || submitDifficulty === null}
        >
          Start Test
        </button>

        {/* Render the TestPage component */}
        <TestPage
          userId={1} // Replace with the appropriate user ID
          courseId={3} // Replace with the appropriate course ID
          numberOfQuestions={5} // Replace with the desired number of questions
          difficulty={0} // Replace with the desired difficulty level
        />
      </div>
    </form>
  );
};

export default CourseSelection;
