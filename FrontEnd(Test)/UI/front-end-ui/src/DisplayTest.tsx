import React, { useEffect, useState } from "react";
import axios from "axios";

interface TestQuestion {
  questionId: number;
  question: string;
  answer: string;
}

interface TestPageProps {
  userId: number;
  courseId: number;
  numberOfQuestions: number;
  difficulty: number;
}

const TestPage: React.FC<TestPageProps> = ({
  userId,
  courseId,
  numberOfQuestions,
  difficulty,
}) => {
  const [testId, setTestId] = useState<number>(0);
  const [questions, setQuestions] = useState<TestQuestion[]>([]);

  // Function to generate the test
  const generateTest = async () => {
    try {
      const requestBody = {
        userId,
        courseId,
        numberOfQuestions,
        difficulty,
      };

      const response = await axios.post(
        "http://localhost:5057/api/Test/generate",
        requestBody
      );
      console.log(response);
      const { testId, questions } = response.data;
      setTestId(testId);
      setQuestions(
        questions.map((question: any) => ({
          questionId: question.questionId,
          question: question.question,
          answer: "",
        }))
      );
    } catch (error) {
      console.error("Error generating test:", error);
    }
  };

  // Function to handle answer input change
  const handleAnswerChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    questionId: number
  ) => {
    const answer = event.target.value;

    setQuestions((prevQuestions) =>
      prevQuestions.map((question) =>
        question.questionId === questionId ? { ...question, answer } : question
      )
    );
  };

  // Function to handle form submission
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      // Prepare the answers data
      const answers = questions.map((question) => ({
        questionId: question.questionId,
        answer: question.answer,
      }));

      // Make the API request to submit the answers
      const response = await axios.post(
        `http://localhost:5057/api/Test/submit/${testId}`,
        answers
      );

      // Handle the response as needed
      console.log("Submit response:", response.data);
    } catch (error) {
      console.error("Error submitting answers:", error);
    }
  };

  return (
    <div>
      <h2>Test Page</h2>
      <button onClick={generateTest}>Generate Test</button>

      <div onSubmit={handleSubmit}>
        {questions.map((question) => (
          <div key={question.questionId}>
            <p>{question.question}</p>
            <input
              type="text"
              value={question.answer}
              onChange={(event) =>
                handleAnswerChange(event, question.questionId)
              }
            />
          </div>
        ))}
        <button type="submit">Submit</button>
      </div>
    </div>
  );
};

export default TestPage;
