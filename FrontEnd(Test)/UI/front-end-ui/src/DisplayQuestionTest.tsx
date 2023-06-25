import React, { useEffect, useState } from "react";
import axios from "axios";

interface Question {
  questionId: number;
  question: string;
}

interface Test {
  testId: number;
  questions: Question[];
}

const DisplayQuestionTest = () => {
  const [tests, setTests] = useState<Test[]>([]);

  useEffect(() => {
    fetchTests();
  }, []);

  const fetchTests = async () => {
    try {
      const response = await axios.get("http://localhost:5057/api/Test");
      setTests(response.data);
      console.log(response);
    } catch (error) {
      console.error("Error fetching tests:", error);
    }
  };

  return (
    <div>
      <h2>Test Questions</h2>
      {tests.map((test) => (
        <div key={test.testId}>
          <h3>Test ID: {test.testId}</h3>
          {test.questions.map((question) => (
            <div key={question.questionId}>
              <p>Question ID: {question.questionId}</p>
              <p>Question: {question.question}</p>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default DisplayQuestionTest;
