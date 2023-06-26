import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

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
  const [submitDifficulty, setSubmitDifficulty] = useState<number>(0);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get("http://localhost:5057/api/Course");
      console.log(response);
      setCourses(response.data);
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
      setSelectedCourseId(courseId);
    } else {
      setSelectedCourseId(1);
    }
  };

  const handleDifficultyChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const difficulty = event.target.value;
    setSelectedDifficulty(difficulty);
    if (difficulty === "easy") {
      setSubmitDifficulty(0);
    } else if (difficulty === "medium") {
      setSubmitDifficulty(1);
    } else if (difficulty === "hard") {
      setSubmitDifficulty(2);
    }
  };

  const handleTestStart = (event: React.FormEvent) => {
    event.preventDefault();
    if (selectedCourseId && submitDifficulty) {
      onSelectCourses(selectedCourseId, submitDifficulty);
    }
    navigate("/test"); //Navigate to the DisplayTest.tsx
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
          type="submit"
          disabled={selectedCourseId === undefined || selectedDifficulty === ""}
        >
          Start Test
        </button>
      </div>
    </form>
  );
};

export default CourseSelection;
